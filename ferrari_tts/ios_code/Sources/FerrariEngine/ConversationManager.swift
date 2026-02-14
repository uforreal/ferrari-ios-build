import Foundation
import Combine

/**
 # ConversationManager.swift (Antigravity Edition)
 # The Sovereign Captain — Split-Brain Architecture
 
 This manager now routes queries through the WebSocket link
 to the PC Orchestrator, instead of reasoning locally.
 
 Flow:
   User Speaks → TalkerClient.sendQuery() → WebSocket → Orchestrator → Brain
   Brain VKP → WebSocket → TalkerClient → formatResponse() → vocalize()
 
 The CortexReasoner is retained as a LOCAL FALLBACK for:
   - Offline mode (no WebSocket connection)
   - System tools (clock, calculator) that don't need the Brain
 */
class ConversationManager: ObservableObject, TalkerClientDelegate {
    
    // ─────────────────────────────────────────────
    // Published State (UI binds to these)
    // ─────────────────────────────────────────────
    
    @Published var state: String = "Idle"
    @Published var aiResponse: String = ""
    @Published var isConnected: Bool = false
    @Published var serverState: String = "OFFLINE"
    
    // ─────────────────────────────────────────────
    // Components
    // ─────────────────────────────────────────────
    
    private let talker: TalkerClient
    private let cortex = CortexReasoner()      // Local fallback
    private let engine: FerrariEngine
    private let streamer: FerrariAudioStreamer
    private let tokenizer: KokoroTokenizer
    private let g2p = G2PProvider()
    private let router = ThalamusRouter()       // Local intent routing
    private let userState = UserState()         // Tracks user dimensions
    
    // ─────────────────────────────────────────────
    // Configuration
    // ─────────────────────────────────────────────
    
    /// Set this to the PC's local IP address.
    /// In production, this would be discovered via Bonjour/mDNS.
    static let orchestratorHost = "192.168.1.100"
    static let orchestratorPort = 9000
    
    // ─────────────────────────────────────────────
    // Lifecycle
    // ─────────────────────────────────────────────
    
    init() throws {
        self.engine = try FerrariEngine()
        self.streamer = FerrariAudioStreamer()
        self.tokenizer = KokoroTokenizer()
        self.talker = TalkerClient(
            host: ConversationManager.orchestratorHost,
            port: ConversationManager.orchestratorPort
        )
        self.talker.delegate = self
        
        // Auto-connect on launch
        talker.connect()
    }
    
    // MARK: - User Input Entry Point
    
    func userSpoke(text: String) {
        // Route locally for system tools (no network needed)
        let intent = router.routeIntent(text: text)
        
        switch intent {
        case .systemClock, .calculator:
            // Handle locally — no Brain needed
            self.state = "Thinking (Local)..."
            router.executeSystemTool(tool: intent) { [weak self] response in
                DispatchQueue.main.async {
                    self?.aiResponse = response
                    self?.vocalize(response)
                }
            }
            return
            
        default:
            break
        }
        
        // Route to Orchestrator via WebSocket
        if talker.isConnected {
            self.state = "Sending to Brain..."
            userState.recordUserTurn(text)
            talker.sendQuery(text, userState: userState.toPayload())
        } else {
            // Fallback to local CORTEX (offline mode)
            self.state = "Thinking (Offline)..."
            cortex.process(input: text) { [weak self] response in
                DispatchQueue.main.async {
                    self?.aiResponse = response
                    self?.vocalize(response)
                }
            }
        }
    }
    
    // MARK: - VKP → Natural Language Formatting
    
    /// Transforms a raw VKP response into natural language for speech.
    /// This is the Talker's core responsibility — the Brain sends data,
    /// the Talker makes it human.
    ///
    /// Each verdict type has 3+ template variations to avoid repetition.
    /// Trust score modulates confidence of delivery.
    private func formatVKPResponse(_ vkp: VKPResponse) -> String {
        let verdict = vkp.payload.verdict
        let trust = vkp.payload.trust_score
        let query = vkp.payload.query
        let root = vkp.payload.root
        
        // Extract proof chain as strings
        let proofStrings = vkp.payload.proof.compactMap { proof -> String? in
            if let str = proof.value as? String { return str }
            if let dict = proof.value as? [String: Any] {
                return dict.description
            }
            return String(describing: proof.value)
        }
        
        // Build the evidence summary
        let evidence = formatEvidenceSummary(proofStrings, root: root)
        
        // Trust-based confidence qualifier
        let qualifier = trustQualifier(trust)
        
        switch verdict {
        // ─────────────────────────────────────────
        // CONFIRMED / PROVEN — confident, direct
        // ─────────────────────────────────────────
        case "PROVEN", "CONFIRMED":
            let templates = [
                "\(qualifier)\(evidence)",
                "Yes. \(evidence) I'm quite confident about this.",
                "\(evidence) The data backs this up clearly."
            ]
            return templates.randomElement()!
            
        // ─────────────────────────────────────────
        // PROBABLE — mostly sure, slight hedge
        // ─────────────────────────────────────────
        case "PROBABLE":
            let templates = [
                "From what I can tell, \(evidence.lowercasedFirst()) This looks solid, though I'd note my confidence is around \(Int(trust * 100)) percent.",
                "Based on available evidence, \(evidence.lowercasedFirst()) I'm fairly confident in this.",
                "It appears that \(evidence.lowercasedFirst()) The evidence is strong but not conclusive."
            ]
            return templates.randomElement()!
            
        // ─────────────────────────────────────────
        // SPECULATIVE — hedged, "based on what I know..."
        // ─────────────────────────────────────────
        case "SPECULATIVE":
            let templates = [
                "Based on what I know, \(evidence.lowercasedFirst()) But I should be honest, my confidence here is only about \(Int(trust * 100)) percent.",
                "Here's what I can piece together. \(evidence) Take this with some caution though, the evidence is thin.",
                "I have some information related to that. \(evidence) But this is more of an educated guess than a firm answer."
            ]
            return templates.randomElement()!
            
        // ─────────────────────────────────────────
        // REFUTED — clear correction
        // ─────────────────────────────────────────
        case "REFUTED":
            let templates = [
                "Actually, that's not quite right. \(evidence) The evidence points in a different direction.",
                "I have to push back on that. \(evidence) The data contradicts that claim.",
                "Not exactly. Based on what I've verified, \(evidence.lowercasedFirst())"
            ]
            return templates.randomElement()!
            
        // ─────────────────────────────────────────
        // UNKNOWN / UNDETERMINED — honest admission
        // ─────────────────────────────────────────
        case "UNDETERMINED", "UNKNOWN":
            let templates = [
                "I don't have enough reliable information about \"\(query)\" to give you a solid answer. Would you like me to dig deeper?",
                "That's a gap in my knowledge right now. I couldn't find enough verified information about \"\(query)\" to speak confidently.",
                "Honestly, I don't have a good answer for that yet. My knowledge on \"\(query)\" is too thin to say anything meaningful."
            ]
            return templates.randomElement()!
            
        // ─────────────────────────────────────────
        // NOVEL — curious, discovery tone
        // ─────────────────────────────────────────
        case "NOVEL":
            let templates = [
                "That's interesting. This is new territory for me. \(evidence) I'll remember this for next time.",
                "I haven't encountered that before, but here's what I can piece together. \(evidence)",
                "This is a fresh one. \(evidence) My certainty is about \(Int(trust * 100)) percent, but I find this genuinely intriguing."
            ]
            return templates.randomElement()!
            
        default:
            return evidence.isEmpty
                ? "I received a result, but I'm not sure how to interpret it."
                : "Here's what I found: \(evidence)"
        }
    }
    
    /// Builds a natural language summary from proof chain entries.
    private func formatEvidenceSummary(_ proofs: [String], root: String) -> String {
        if proofs.isEmpty {
            return ""
        }
        
        // Check for special cases
        let firstProof = proofs.first ?? ""
        
        // Time query — "SystemClock(Local) -> 3:45:22 PM"
        if firstProof.contains("SystemClock") {
            let parts = firstProof.components(separatedBy: " -> ")
            if parts.count >= 2 {
                return "The time is \(parts[1])."
            }
        }
        
        // Standard knowledge triple — "Subject -Predicate-> Object"
        var sentences: [String] = []
        for proof in proofs.prefix(3) {
            sentences.append(formatTripleAsNaturalLanguage(proof))
        }
        
        let result = sentences.joined(separator: " ")
        
        if proofs.count > 3 {
            return "\(result) And there's more I could share."
        }
        
        return result
    }
    
    /// Converts a single proof triple into a natural sentence.
    private func formatTripleAsNaturalLanguage(_ proof: String) -> String {
        // Format: "subject -predicate-> object"
        let cleaned = proof
            .replacingOccurrences(of: "_", with: " ")
        
        // Try to parse as triple
        if let dashIndex = cleaned.range(of: " -"),
           let arrowIndex = cleaned.range(of: "-> ") {
            let subject = String(cleaned[cleaned.startIndex..<dashIndex.lowerBound]).capitalized
            let predicate = String(cleaned[dashIndex.upperBound..<arrowIndex.lowerBound])
                .trimmingCharacters(in: .whitespaces)
                .lowercased()
            let object = String(cleaned[arrowIndex.upperBound...])
                .trimmingCharacters(in: .whitespaces)
            
            // Generate natural phrasing based on predicate
            switch predicate {
            case "isa", "is a":
                return "\(subject) is a \(object)."
            case "hasproperty", "has property":
                return "\(subject) has the property of \(object)."
            case "locatedin", "located in":
                return "\(subject) is located in \(object)."
            case "partof", "part of":
                return "\(subject) is part of \(object)."
            case "causedby", "caused by":
                return "\(subject) is caused by \(object)."
            case "causes":
                return "\(subject) causes \(object)."
            default:
                return "\(subject) \(predicate) \(object)."
            }
        }
        
        // Fallback: return as-is
        return cleaned
    }
    
    /// Returns a confidence qualifier based on trust score.
    private func trustQualifier(_ trust: Double) -> String {
        if trust > 0.9 {
            return "I can say with high confidence: "
        } else if trust > 0.7 {
            return "With good confidence, "
        } else if trust > 0.5 {
            return ""  // No qualifier for moderate trust
        } else {
            return "I'm not fully certain, but "
        }
    }
    

    
    // MARK: - Voice Output
    
    private func vocalize(_ text: String) {
        // Step 1: Phonemize
        let phonemes = g2p.getPhonemes(for: text)
        
        // Step 2: Tokenize (114-token map)
        let tokenIds = tokenizer.tokenize(phonemes)
        
        // Step 3: Speak via Ferrari Engine (ONNX)
        engine.speak64(tokenIds) { [weak self] audioBuffer in
            self?.streamer.pushAudio(audioBuffer)
            DispatchQueue.main.async {
                self?.state = "Speaking..."
            }
        }
    }
    
    // MARK: - TalkerClientDelegate
    
    func talkerDidConnect(_ client: TalkerClient, welcome: WelcomePayload) {
        self.isConnected = true
        self.serverState = welcome.serverState
        self.state = welcome.brainLoaded ? "Connected (Brain Ready)" : "Connected (Brain Loading...)"
        print("🏗️ [ConversationManager] Orchestrator online. v\(welcome.serverVersion)")
    }
    
    func talkerDidReceiveACK(_ client: TalkerClient, ack: ACKPayload) {
        self.serverState = ack.status
        
        switch ack.status {
        case "THINKING":
            self.state = "Brain is thinking..."
        case "READING":
            self.state = "Analyzing document..."
        case "HUNTING":
            self.state = "Searching the web..."
        default:
            self.state = "Processing..."
        }
    }
    
    func talkerDidReceiveVKP(_ client: TalkerClient, vkp: VKPResponse) {
        // THIS IS THE CORE LOOP:
        // Brain data → Natural language → Voice
        let response = formatVKPResponse(vkp)
        userState.recordSystemTurn(response, verdict: vkp.payload.verdict)
        self.aiResponse = response
        self.state = "Formatting response..."
        
        // Speak it
        vocalize(response)
    }
    
    func talkerDidReceiveConceptMap(_ client: TalkerClient, map: ConceptMapResponse) {
        let summary = "I've analyzed the document. The core idea is: \(map.core_idea)"
        self.aiResponse = summary
        vocalize(summary)
    }
    
    func talkerDidReceiveStatus(_ client: TalkerClient, status: StatusPayload) {
        let pct = Int(status.progress * 100)
        self.state = "\(status.phase) (\(pct)%)..."
    }
    
    func talkerDidReceiveError(_ client: TalkerClient, error: ErrorPayload) {
        self.state = "Error: \(error.code)"
        self.aiResponse = error.message
        
        if error.retryable {
            self.aiResponse += " I'll try again shortly."
        }
        
        // Speak the error naturally
        vocalize("I encountered an issue. \(error.message)")
    }
    
    func talkerDidDisconnect(_ client: TalkerClient, reason: String) {
        self.isConnected = false
        self.serverState = "OFFLINE"
        self.state = "Disconnected (Offline Mode)"
        print("🔌 [ConversationManager] Disconnected: \(reason)")
    }
}

// MARK: - String Extension

private extension String {
    /// Returns a copy with the first character lowercased.
    /// Useful for embedding evidence into sentence continuations.
    func lowercasedFirst() -> String {
        guard let first = self.first else { return self }
        return first.lowercased() + self.dropFirst()
    }
}
