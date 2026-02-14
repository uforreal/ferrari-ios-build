import Foundation

/**
 # TalkerClient.swift
 # Project Antigravity — Phase 3.5
 
 WebSocket connection manager for the iPhone ↔ Orchestrator link.
 
 Responsibilities:
 - Maintains persistent WebSocket connection to the PC Orchestrator
 - Sends QUERY and ANALYZE messages
 - Receives and decodes WELCOME, ACK, VKP, CONCEPT_MAP, ERROR, STATUS, PONG
 - Auto-reconnects on drop (iPhone sleep/wake recovery)
 - Heartbeat PING every 30 seconds
 
 Usage:
     let client = TalkerClient(host: "192.168.1.100", port: 9000)
     client.delegate = self
     client.connect()
     client.sendQuery("Who is Napoleon?")
 */

// MARK: - Delegate Protocol

protocol TalkerClientDelegate: AnyObject {
    /// Called when the Orchestrator connection is established.
    func talkerDidConnect(_ client: TalkerClient, welcome: WelcomePayload)
    
    /// Called when the Orchestrator acknowledges a request.
    func talkerDidReceiveACK(_ client: TalkerClient, ack: ACKPayload)
    
    /// Called when a VKP (factual answer) arrives from the Brain.
    func talkerDidReceiveVKP(_ client: TalkerClient, vkp: VKPResponse)
    
    /// Called when a ConceptMap arrives from the RAE.
    func talkerDidReceiveConceptMap(_ client: TalkerClient, map: ConceptMapResponse)
    
    /// Called on status updates during long operations.
    func talkerDidReceiveStatus(_ client: TalkerClient, status: StatusPayload)
    
    /// Called on error from the Orchestrator.
    func talkerDidReceiveError(_ client: TalkerClient, error: ErrorPayload)
    
    /// Called when the connection is lost.
    func talkerDidDisconnect(_ client: TalkerClient, reason: String)
}

// MARK: - TalkerClient

class TalkerClient {
    
    // ─────────────────────────────────────────────
    // Configuration
    // ─────────────────────────────────────────────
    
    private(set) var host: String
    private(set) var port: Int
    weak var delegate: TalkerClientDelegate?
    
    // ─────────────────────────────────────────────
    // State
    // ─────────────────────────────────────────────
    
    private(set) var isConnected: Bool = false
    private(set) var serverState: OrchestratorState = .idle
    private(set) var brainLoaded: Bool = false
    
    // ─────────────────────────────────────────────
    // Internals
    // ─────────────────────────────────────────────
    
    private var webSocketTask: URLSessionWebSocketTask?
    private var session: URLSession!
    private var pingTimer: Timer?
    private var reconnectTimer: Timer?
    private var messageCounter: Int = 0
    
    /// How long to wait before attempting reconnect (seconds).
    private let reconnectDelay: TimeInterval = 3.0
    
    /// Maximum reconnect attempts before giving up.
    private let maxReconnectAttempts: Int = 10
    private var reconnectAttempts: Int = 0
    
    /// Ping interval in seconds.
    private let pingInterval: TimeInterval = 30.0
    
    // ─────────────────────────────────────────────
    // Lifecycle
    // ─────────────────────────────────────────────
    
    init(host: String = "localhost", port: Int = 9000) {
        self.host = host
        self.port = port
        self.session = URLSession(configuration: .default)
    }
    
    /// Update the endpoint (called by ServiceDiscovery when
    /// the Orchestrator is discovered or its IP changes).
    func updateEndpoint(host: String, port: Int) {
        self.host = host
        self.port = port
        print("🔄 [TalkerClient] Endpoint updated: \(host):\(port)")
    }
    
    /// Disconnect from old endpoint and connect to new one.
    func reconnectToNewEndpoint(host: String, port: Int) {
        disconnect()
        updateEndpoint(host: host, port: port)
        reconnectAttempts = 0
        connect()
    }
    
    deinit {
        disconnect()
    }
    
    // MARK: - Connection Management
    
    /// Establish WebSocket connection to the Orchestrator.
    func connect() {
        guard !isConnected else {
            print("🔌 [TalkerClient] Already connected.")
            return
        }
        
        let urlString = "ws://\(host):\(port)"
        guard let url = URL(string: urlString) else {
            print("❌ [TalkerClient] Invalid URL: \(urlString)")
            return
        }
        
        print("🔌 [TalkerClient] Connecting to \(urlString)...")
        
        webSocketTask = session.webSocketTask(with: url)
        webSocketTask?.resume()
        
        // Start listening for messages
        listenForMessages()
    }
    
    /// Cleanly disconnect from the Orchestrator.
    func disconnect() {
        pingTimer?.invalidate()
        pingTimer = nil
        reconnectTimer?.invalidate()
        reconnectTimer = nil
        
        webSocketTask?.cancel(with: .goingAway, reason: "Client disconnect".data(using: .utf8))
        webSocketTask = nil
        isConnected = false
    }
    
    // MARK: - Sending Messages
    
    /// Send a QUERY to the Brain.
    /// Returns the message ID for correlation.
    @discardableResult
    func sendQuery(_ text: String, userState: [String: Any]? = nil) -> String {
        let id = nextMessageId("q")
        var payload: [String: Any] = ["text": text]
        if let state = userState {
            payload["userState"] = state
        }
        let msg: [String: Any] = [
            "type": "QUERY",
            "id": id,
            "timestamp": Date().timeIntervalSince1970 * 1000,
            "payload": payload
        ]
        send(msg)
        print("📤 [TalkerClient] QUERY sent: \"\(text)\" (id: \(id))")
        return id
    }
    
    /// Send an ANALYZE request to the RAE.
    @discardableResult
    func sendAnalyze(text: String, title: String, source: String = "manual_input") -> String {
        let id = nextMessageId("a")
        let msg: [String: Any] = [
            "type": "ANALYZE",
            "id": id,
            "timestamp": Date().timeIntervalSince1970 * 1000,
            "payload": [
                "text": text,
                "title": title,
                "source": source
            ]
        ]
        send(msg)
        print("📤 [TalkerClient] ANALYZE sent: \"\(title)\" (id: \(id))")
        return id
    }
    
    /// Send a PING heartbeat.
    private func sendPing() {
        let id = nextMessageId("p")
        let msg: [String: Any] = [
            "type": "PING",
            "id": id,
            "timestamp": Date().timeIntervalSince1970 * 1000,
            "payload": [String: Any]()
        ]
        send(msg)
    }
    
    // MARK: - Receiving Messages
    
    private func listenForMessages() {
        webSocketTask?.receive { [weak self] result in
            guard let self = self else { return }
            
            switch result {
            case .success(let message):
                switch message {
                case .string(let text):
                    self.handleRawMessage(text)
                case .data(let data):
                    if let text = String(data: data, encoding: .utf8) {
                        self.handleRawMessage(text)
                    }
                @unknown default:
                    break
                }
                
                // Continue listening
                self.listenForMessages()
                
            case .failure(let error):
                print("❌ [TalkerClient] Receive error: \(error.localizedDescription)")
                self.handleDisconnect(reason: error.localizedDescription)
            }
        }
    }
    
    private func handleRawMessage(_ text: String) {
        guard let data = text.data(using: .utf8) else { return }
        
        do {
            // First, decode the envelope to get the type
            let envelope = try JSONDecoder().decode(MessageEnvelope.self, from: data)
            
            switch envelope.type {
            case "WELCOME":
                handleWelcome(data)
                
            case "ACK":
                handleACK(data)
                
            case "VKP":
                handleVKP(data)
                
            case "CONCEPT_MAP":
                handleConceptMap(data)
                
            case "STATUS":
                handleStatus(data)
                
            case "ERROR":
                handleError(data)
                
            case "PONG":
                handlePong(data)
                
            default:
                print("⚠️ [TalkerClient] Unknown message type: \(envelope.type)")
            }
            
        } catch {
            print("❌ [TalkerClient] JSON decode error: \(error)")
        }
    }
    
    // ─────────────────────────────────────────────
    // Handlers
    // ─────────────────────────────────────────────
    
    private func handleWelcome(_ data: Data) {
        struct WelcomeMessage: Codable {
            let type: String
            let payload: WelcomePayload
        }
        
        guard let msg = try? JSONDecoder().decode(WelcomeMessage.self, from: data) else { return }
        
        isConnected = true
        reconnectAttempts = 0
        brainLoaded = msg.payload.brainLoaded
        serverState = OrchestratorState(rawValue: msg.payload.serverState) ?? .idle
        
        print("✅ [TalkerClient] Connected! Server v\(msg.payload.serverVersion), Brain: \(brainLoaded ? "LOADED" : "OFFLINE")")
        
        // Start heartbeat
        startPingTimer()
        
        DispatchQueue.main.async {
            self.delegate?.talkerDidConnect(self, welcome: msg.payload)
        }
    }
    
    private func handleACK(_ data: Data) {
        struct ACKMessage: Codable {
            let type: String
            let payload: ACKPayload
        }
        
        guard let msg = try? JSONDecoder().decode(ACKMessage.self, from: data) else { return }
        
        serverState = OrchestratorState(rawValue: msg.payload.status) ?? .thinking
        
        DispatchQueue.main.async {
            self.delegate?.talkerDidReceiveACK(self, ack: msg.payload)
        }
    }
    
    private func handleVKP(_ data: Data) {
        struct VKPMessage: Codable {
            let type: String
            let payload: VKPResponse
        }
        
        guard let msg = try? JSONDecoder().decode(VKPMessage.self, from: data) else {
            print("❌ [TalkerClient] Failed to decode VKP")
            return
        }
        
        serverState = .idle
        
        print("📦 [TalkerClient] VKP received: \(msg.payload.payload.verdict) (trust: \(msg.payload.payload.trust_score))")
        
        DispatchQueue.main.async {
            self.delegate?.talkerDidReceiveVKP(self, vkp: msg.payload)
        }
    }
    
    private func handleConceptMap(_ data: Data) {
        struct CMMessage: Codable {
            let type: String
            let payload: ConceptMapResponse
        }
        
        guard let msg = try? JSONDecoder().decode(CMMessage.self, from: data) else { return }
        
        serverState = .idle
        
        DispatchQueue.main.async {
            self.delegate?.talkerDidReceiveConceptMap(self, map: msg.payload)
        }
    }
    
    private func handleStatus(_ data: Data) {
        struct StatusMessage: Codable {
            let type: String
            let payload: StatusPayload
        }
        
        guard let msg = try? JSONDecoder().decode(StatusMessage.self, from: data) else { return }
        
        DispatchQueue.main.async {
            self.delegate?.talkerDidReceiveStatus(self, status: msg.payload)
        }
    }
    
    private func handleError(_ data: Data) {
        struct ErrorMessage: Codable {
            let type: String
            let payload: ErrorPayload
        }
        
        guard let msg = try? JSONDecoder().decode(ErrorMessage.self, from: data) else { return }
        
        print("❌ [TalkerClient] Error: \(msg.payload.code) — \(msg.payload.message)")
        
        DispatchQueue.main.async {
            self.delegate?.talkerDidReceiveError(self, error: msg.payload)
        }
    }
    
    private func handlePong(_ data: Data) {
        struct PongMessage: Codable {
            let type: String
            let payload: PongPayload
        }
        
        guard let msg = try? JSONDecoder().decode(PongMessage.self, from: data) else { return }
        
        serverState = OrchestratorState(rawValue: msg.payload.serverState) ?? .idle
        brainLoaded = msg.payload.brainLoaded
    }
    
    // MARK: - Reconnection Logic
    
    private func handleDisconnect(reason: String) {
        isConnected = false
        pingTimer?.invalidate()
        pingTimer = nil
        
        DispatchQueue.main.async {
            self.delegate?.talkerDidDisconnect(self, reason: reason)
        }
        
        // Auto-reconnect
        if reconnectAttempts < maxReconnectAttempts {
            reconnectAttempts += 1
            let delay = reconnectDelay * Double(reconnectAttempts)
            print("🔄 [TalkerClient] Reconnecting in \(delay)s (attempt \(reconnectAttempts)/\(maxReconnectAttempts))...")
            
            DispatchQueue.main.asyncAfter(deadline: .now() + delay) { [weak self] in
                self?.connect()
            }
        } else {
            print("💀 [TalkerClient] Max reconnect attempts reached. Giving up.")
        }
    }
    
    // MARK: - Heartbeat
    
    private func startPingTimer() {
        pingTimer?.invalidate()
        
        DispatchQueue.main.async {
            self.pingTimer = Timer.scheduledTimer(withTimeInterval: self.pingInterval, repeats: true) { [weak self] _ in
                self?.sendPing()
            }
        }
    }
    
    // MARK: - Utilities
    
    private func send(_ dict: [String: Any]) {
        guard let data = try? JSONSerialization.data(withJSONObject: dict, options: []),
              let text = String(data: data, encoding: .utf8) else {
            print("❌ [TalkerClient] Failed to serialize message.")
            return
        }
        
        webSocketTask?.send(.string(text)) { error in
            if let error = error {
                print("❌ [TalkerClient] Send error: \(error.localizedDescription)")
            }
        }
    }
    
    private func nextMessageId(_ prefix: String) -> String {
        messageCounter += 1
        return "\(prefix)_\(messageCounter)"
    }
}

// MARK: - Message Envelope (for type detection)

private struct MessageEnvelope: Codable {
    let type: String
}
