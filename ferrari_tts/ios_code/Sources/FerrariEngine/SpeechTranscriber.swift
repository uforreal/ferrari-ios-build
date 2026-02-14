import Foundation
import Speech
import AVFoundation

/**
 # SpeechTranscriber.swift
 # Project Antigravity — Phase 4
 
 Bridges BouncerVAD (speech detection) → SFSpeechRecognizer (transcription)
 → ConversationManager.userSpoke(text).
 
 Flow:
   1. Microphone audio feeds into BouncerVAD
   2. BouncerVAD detects human speech → starts recording
   3. Audio buffer accumulates while speech continues
   4. BouncerVAD detects silence → stops recording
   5. SFSpeechRecognizer transcribes the recorded buffer
   6. Transcribed text → ConversationManager.userSpoke()
 
 On-device only: requiresOnDeviceRecognition = true
 The network path is reserved for the Orchestrator WebSocket link.
 */

// MARK: - Delegate

protocol SpeechTranscriberDelegate: AnyObject {
    /// Called when transcription produces final text.
    func transcriber(_ transcriber: SpeechTranscriber, didTranscribe text: String)
    
    /// Called when listening state changes.
    func transcriber(_ transcriber: SpeechTranscriber, didChangeState state: SpeechTranscriber.State)
    
    /// Called on error.
    func transcriber(_ transcriber: SpeechTranscriber, didFailWithError error: Error)
}

// MARK: - SpeechTranscriber

class SpeechTranscriber: NSObject, ObservableObject {
    
    // ─────────────────────────────────────────────
    // State
    // ─────────────────────────────────────────────
    
    enum State: String {
        case idle           = "Idle"
        case listening      = "Listening..."
        case transcribing   = "Transcribing..."
        case unavailable    = "Speech Recognition Unavailable"
    }
    
    @Published var state: State = .idle
    @Published var isAuthorized: Bool = false
    @Published var partialTranscript: String = ""
    
    weak var delegate: SpeechTranscriberDelegate?
    
    // ─────────────────────────────────────────────
    // Audio Components
    // ─────────────────────────────────────────────
    
    private let audioEngine = AVAudioEngine()
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let speechRecognizer: SFSpeechRecognizer?
    
    // ─────────────────────────────────────────────
    // VAD Integration
    // ─────────────────────────────────────────────
    
    private var bouncer: BouncerVAD?
    private var isSpeechDetected: Bool = false
    private var silenceFrameCount: Int = 0
    
    /// Number of consecutive silent frames needed to end recording.
    /// At 16kHz with 512-sample frames, ~30 frames ≈ 1 second of silence.
    private let silenceThreshold: Int = 30
    
    /// Minimum speech frames required before we accept a recording.
    /// Prevents false positives from short noise bursts.
    private var speechFrameCount: Int = 0
    private let minimumSpeechFrames: Int = 10
    
    // ─────────────────────────────────────────────
    // Lifecycle
    // ─────────────────────────────────────────────
    
    override init() {
        self.speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
        super.init()
        
        // Initialize VAD
        do {
            self.bouncer = try BouncerVAD()
            print("🎤 [SpeechTranscriber] BouncerVAD initialized.")
        } catch {
            print("⚠️ [SpeechTranscriber] BouncerVAD unavailable: \(error). Will use continuous recognition only.")
        }
    }
    
    // MARK: - Authorization
    
    /// Request microphone + speech recognition permissions.
    func requestAuthorization(completion: @escaping (Bool) -> Void) {
        SFSpeechRecognizer.requestAuthorization { [weak self] authStatus in
            DispatchQueue.main.async {
                switch authStatus {
                case .authorized:
                    self?.isAuthorized = true
                    print("✅ [SpeechTranscriber] Speech recognition authorized.")
                    completion(true)
                    
                case .denied, .restricted:
                    self?.isAuthorized = false
                    self?.state = .unavailable
                    print("❌ [SpeechTranscriber] Speech recognition denied/restricted.")
                    completion(false)
                    
                case .notDetermined:
                    self?.isAuthorized = false
                    completion(false)
                    
                @unknown default:
                    completion(false)
                }
            }
        }
    }
    
    // MARK: - Start / Stop Listening
    
    /// Begin listening for speech via microphone.
    func startListening() throws {
        // Cancel any existing session
        stopListening()
        
        guard let recognizer = speechRecognizer, recognizer.isAvailable else {
            state = .unavailable
            throw TranscriberError.recognizerUnavailable
        }
        
        guard isAuthorized else {
            throw TranscriberError.notAuthorized
        }
        
        // Configure audio session
        let audioSession = AVAudioSession.sharedInstance()
        try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
        try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        
        // Create recognition request
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else {
            throw TranscriberError.requestCreationFailed
        }
        
        // On-device only — no network dependency for STT
        recognitionRequest.requiresOnDeviceRecognition = true
        recognitionRequest.shouldReportPartialResults = true
        
        // Start recognition task
        recognitionTask = recognizer.recognitionTask(with: recognitionRequest) { [weak self] result, error in
            guard let self = self else { return }
            
            var isFinal = false
            
            if let result = result {
                let transcript = result.bestTranscription.formattedString
                
                DispatchQueue.main.async {
                    self.partialTranscript = transcript
                }
                
                isFinal = result.isFinal
                
                if isFinal {
                    print("📝 [SpeechTranscriber] Final: \"\(transcript)\"")
                    DispatchQueue.main.async {
                        self.delegate?.transcriber(self, didTranscribe: transcript)
                        self.state = .idle
                    }
                }
            }
            
            if let error = error {
                // Don't report cancellation as error (expected on stop)
                if (error as NSError).code != 216 { // SFSpeechRecognizerError.operationCancelled
                    print("❌ [SpeechTranscriber] Error: \(error.localizedDescription)")
                    DispatchQueue.main.async {
                        self.delegate?.transcriber(self, didFailWithError: error)
                    }
                }
            }
            
            if error != nil || isFinal {
                self.audioEngine.stop()
                self.audioEngine.inputNode.removeTap(onBus: 0)
                self.recognitionRequest = nil
                self.recognitionTask = nil
                
                DispatchQueue.main.async {
                    if self.state != .unavailable {
                        self.state = .idle
                    }
                }
            }
        }
        
        // Install audio tap on microphone
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { [weak self] buffer, _ in
            guard let self = self else { return }
            
            // Feed audio to VAD for speech boundary detection
            if let bouncer = self.bouncer {
                let channelData = buffer.floatChannelData?[0]
                let frameCount = Int(buffer.frameLength)
                
                if let data = channelData {
                    let samples = Array(UnsafeBufferPointer(start: data, count: frameCount))
                    let isSpeech = bouncer.isHumanSpeaking(samples)
                    
                    if isSpeech {
                        self.isSpeechDetected = true
                        self.silenceFrameCount = 0
                        self.speechFrameCount += 1
                    } else if self.isSpeechDetected {
                        self.silenceFrameCount += 1
                        
                        // If enough silence after speech, finalize
                        if self.silenceFrameCount >= self.silenceThreshold &&
                           self.speechFrameCount >= self.minimumSpeechFrames {
                            // End of utterance detected
                            self.recognitionRequest?.endAudio()
                            self.isSpeechDetected = false
                            self.speechFrameCount = 0
                            self.silenceFrameCount = 0
                            return
                        }
                    }
                }
            }
            
            // Feed audio to speech recognizer
            self.recognitionRequest?.append(buffer)
        }
        
        // Start audio engine
        audioEngine.prepare()
        try audioEngine.start()
        
        state = .listening
        isSpeechDetected = false
        silenceFrameCount = 0
        speechFrameCount = 0
        partialTranscript = ""
        
        DispatchQueue.main.async {
            self.delegate?.transcriber(self, didChangeState: .listening)
        }
        
        print("🎤 [SpeechTranscriber] Listening...")
    }
    
    /// Stop listening and clean up.
    func stopListening() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        recognitionRequest?.endAudio()
        recognitionTask?.cancel()
        recognitionRequest = nil
        recognitionTask = nil
        
        state = .idle
        partialTranscript = ""
    }
    
    // MARK: - Continuous Mode
    
    /// Start listening and automatically restart after each utterance.
    /// This creates a continuous conversation loop.
    func startContinuousListening() {
        // After each transcription completes, start listening again
        // This is handled by the delegate callback chain:
        // SpeechTranscriber → delegate.didTranscribe() → ConversationManager.userSpoke()
        // → VKP response → voice output → startListening() again
        do {
            try startListening()
        } catch {
            print("❌ [SpeechTranscriber] Failed to start: \(error)")
            delegate?.transcriber(self, didFailWithError: error)
        }
    }
}

// MARK: - Errors

enum TranscriberError: LocalizedError {
    case recognizerUnavailable
    case notAuthorized
    case requestCreationFailed
    
    var errorDescription: String? {
        switch self {
        case .recognizerUnavailable:
            return "On-device speech recognition is not available on this device."
        case .notAuthorized:
            return "Speech recognition permission has not been granted."
        case .requestCreationFailed:
            return "Failed to create speech recognition request."
        }
    }
}
