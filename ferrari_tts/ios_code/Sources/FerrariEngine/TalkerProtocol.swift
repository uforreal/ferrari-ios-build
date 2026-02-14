import Foundation

/**
 # TalkerProtocol.swift
 # Project Antigravity — Phase 3.5
 
 Defines all WebSocket message types exchanged between
 iPhone (TalkerClient) and PC (Orchestrator).
 
 This file is the Swift equivalent of protocol.js.
 Every type must match the Node.js server exactly.
 */

// MARK: - Base Message Envelope

/// Every WebSocket message conforms to this envelope.
struct WSMessage: Codable {
    let type: String
    let id: String
    let timestamp: Double
    let payload: [String: AnyCodable]
}

// MARK: - Client → Server Messages

/// QUERY: Ask the Brain a factual question.
struct QueryPayload: Codable {
    let text: String
}

/// ANALYZE: Send document text to the RAE.
struct AnalyzePayload: Codable {
    let text: String
    let title: String
    let source: String
}

// MARK: - Server → Client Messages

/// WELCOME payload received on connection.
struct WelcomePayload: Codable {
    let serverVersion: String
    let serverState: String
    let brainLoaded: Bool
    let raeAvailable: Bool
    let harvesterAvailable: Bool
    let constraints: ServerConstraints
}

struct ServerConstraints: Codable {
    let maxMessageSize: Int
    let serialExecution: Bool
    let pingInterval: Int
}

/// ACK payload — immediate acknowledgment.
struct ACKPayload: Codable {
    let refId: String
    let status: String  // THINKING | READING | HUNTING | QUEUED
}

/// VKP — Verified Knowledge Packet from Brain.
struct VKPHeader: Codable {
    let id: String
    let engine_version: String
    let timestamp: String
    let compliance: String
}

struct VKPPayloadInner: Codable {
    let query: String
    let verdict: String        // PROVEN | PROBABLE | SPECULATIVE | UNDETERMINED | REFUTED
    let root: String
    let proof: [AnyCodable]
    let trust_score: Double
    let constraints: [AnyCodable]
}

struct VKPResponse: Codable {
    let refId: String
    let header: VKPHeader
    let payload: VKPPayloadInner
    let verified: Bool
    let processingTime: Int?
}

/// CONCEPT_MAP — RAE document analysis result.
struct ConceptEntry: Codable {
    let label: String
    let centrality: Double
    let role: String
}

struct ConceptMapResponse: Codable {
    let refId: String
    let core_idea: String
    let concepts: [ConceptEntry]
    let processing_time_ms: Int?
}

/// ERROR payload.
struct ErrorPayload: Codable {
    let refId: String?
    let code: String           // RESOURCE_BUSY | TIMEOUT | OOM | BRAIN_ERROR | NOT_IMPLEMENTED
    let message: String
    let retryable: Bool
}

/// STATUS — progress update for long operations.
struct StatusPayload: Codable {
    let refId: String
    let phase: String          // LOADING | ANALYZING | CLUSTERING | COMPLETE
    let progress: Double       // 0.0 to 1.0
    let message: String
}

/// PONG — heartbeat response.
struct PongPayload: Codable {
    let refId: String?
    let serverState: String
    let uptime: Double
    let brainLoaded: Bool
    let raeLoaded: Bool
}

// MARK: - Orchestrator States (Mirror of Traffic Light)

enum OrchestratorState: String, Codable {
    case idle     = "IDLE"
    case thinking = "THINKING"
    case reading  = "READING"
    case hunting  = "HUNTING"
}

// MARK: - Verdict Enum

enum Verdict: String, Codable {
    case proven       = "PROVEN"
    case probable     = "PROBABLE"
    case speculative  = "SPECULATIVE"
    case undetermined = "UNDETERMINED"
    case refuted      = "REFUTED"
}

// MARK: - AnyCodable (Lightweight Type-Erased Codable)

/// Allows encoding/decoding heterogeneous JSON values.
/// Needed because VKP `proof` and `constraints` can be mixed types.
struct AnyCodable: Codable {
    let value: Any
    
    init(_ value: Any) {
        self.value = value
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        
        if container.decodeNil() {
            value = NSNull()
        } else if let bool = try? container.decode(Bool.self) {
            value = bool
        } else if let int = try? container.decode(Int.self) {
            value = int
        } else if let double = try? container.decode(Double.self) {
            value = double
        } else if let string = try? container.decode(String.self) {
            value = string
        } else if let array = try? container.decode([AnyCodable].self) {
            value = array.map { $0.value }
        } else if let dict = try? container.decode([String: AnyCodable].self) {
            value = dict.mapValues { $0.value }
        } else {
            throw DecodingError.typeMismatch(
                AnyCodable.self,
                DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Unsupported type")
            )
        }
    }
    
    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        
        switch value {
        case is NSNull:
            try container.encodeNil()
        case let bool as Bool:
            try container.encode(bool)
        case let int as Int:
            try container.encode(int)
        case let double as Double:
            try container.encode(double)
        case let string as String:
            try container.encode(string)
        case let array as [Any]:
            try container.encode(array.map { AnyCodable($0) })
        case let dict as [String: Any]:
            try container.encode(dict.mapValues { AnyCodable($0) })
        default:
            throw EncodingError.invalidValue(
                value,
                EncodingError.Context(codingPath: encoder.codingPath, debugDescription: "Unsupported type")
            )
        }
    }
}
