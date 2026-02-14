import Foundation

/**
 # UserState.swift
 # Project Antigravity — Phase 3.5
 
 Tracks the user's conversational state on the iPhone.
 This state is maintained locally and sent alongside
 QUERY/ANALYZE messages to inform the Orchestrator's
 response behavior.
 
 Based on: 05_user_state_design.md
 
 Dimensions tracked:
   1. Conversation History (last N turns)
   2. Emotional Tone (valence, arousal)
   3. Expertise Level (per topic)
   4. Engagement & Pace
   5. Prophetic Communication Principles (Receptivity, Horizon, Generosity)
 */

// MARK: - Core State Model

class UserState: ObservableObject {
    
    // ─────────────────────────────────────────────
    // Published Dimensions
    // ─────────────────────────────────────────────
    
    /// Emotional state of the user.
    @Published var emotion: EmotionalState = EmotionalState()
    
    /// Current engagement level.
    @Published var engagement: EngagementLevel = .casual
    
    /// Current topic context.
    @Published var currentTopic: String = ""
    
    /// Overall expert level for the current topic (0.0 - 1.0).
    @Published var expertiseLevel: Double = 0.5
    
    // ─────────────────────────────────────────────
    // History
    // ─────────────────────────────────────────────
    
    /// Last N conversation turns (working memory).
    private(set) var turns: [Turn] = []
    
    /// Maximum turns to keep in working memory.
    private let maxTurns: Int = 10
    
    /// Topic expertise map: topic → expertise score.
    private var topicExpertise: [String: Double] = [:]
    
    /// Timestamps of recent queries (for pace detection).
    private var queryTimestamps: [Date] = []
    
    // ─────────────────────────────────────────────
    // Constants
    // ─────────────────────────────────────────────
    
    /// Frustration indicators in user text.
    private let frustrationWords = Set(["wrong", "no", "not", "why", "broken", "doesn't", "can't", "useless", "stupid", "repeat"])
    
    /// Curiosity indicators.
    private let curiosityWords = Set(["why", "how", "what if", "explain", "tell me more", "elaborate", "interesting"])
    
    /// Satisfaction indicators.
    private let satisfactionWords = Set(["thanks", "thank you", "perfect", "great", "good", "nice", "finally", "awesome"])
    
    // MARK: - Turn Recording
    
    /// Records a user turn and updates all state dimensions.
    func recordUserTurn(_ text: String) {
        let turn = Turn(
            speaker: .user,
            text: text,
            timestamp: Date()
        )
        
        appendTurn(turn)
        updateEmotion(from: text)
        updateEngagement()
        updateTopic(from: text)
        updateExpertise(from: text)
    }
    
    /// Records a system response turn.
    func recordSystemTurn(_ text: String, verdict: String? = nil) {
        let turn = Turn(
            speaker: .system,
            text: text,
            timestamp: Date(),
            verdict: verdict
        )
        
        appendTurn(turn)
    }
    
    // MARK: - Prophetic Principles
    
    /// The Uhud Principle: Do not burden a heavy heart.
    /// Returns 0.0 (do NOT deliver heavy content) to 1.0 (user is open).
    var receptivity: Double {
        let valenceComponent = (emotion.valence + 1.0) / 2.0  // Normalize -1..1 to 0..1
        let arousalPenalty = emotion.arousal                    // High arousal = less receptive
        return max(0.0, min(1.0, valenceComponent * (1.0 - arousalPenalty)))
    }
    
    /// The Ibrahim Principle: How generous should the response be?
    /// Returns 0.0 (be brief) to 1.0 (elaborate freely).
    var generosity: Double {
        switch engagement {
        case .deepFocus:
            return emotion.valence > 0 ? 0.8 : 0.5
        case .casual:
            return 0.6
        case .disengaged:
            return 0.2
        }
    }
    
    // MARK: - Serialization (for WebSocket payload)
    
    /// Produces the JSON payload to include in QUERY messages.
    func toPayload() -> [String: Any] {
        return [
            "emotion": emotion.currentLabel,
            "valence": emotion.valence,
            "arousal": emotion.arousal,
            "expertise": expertiseLevel,
            "engagement": engagement.rawValue,
            "receptivity": receptivity,
            "generosity": generosity,
            "topic": currentTopic,
            "turnCount": turns.count
        ]
    }
    
    // MARK: - Internal Updates
    
    private func appendTurn(_ turn: Turn) {
        turns.append(turn)
        if turns.count > maxTurns {
            turns.removeFirst()
        }
        queryTimestamps.append(turn.timestamp)
        if queryTimestamps.count > 20 {
            queryTimestamps.removeFirst()
        }
    }
    
    private func updateEmotion(from text: String) {
        let words = Set(text.lowercased().split(separator: " ").map(String.init))
        
        let frustrationCount = words.intersection(frustrationWords).count
        let curiosityCount = words.intersection(curiosityWords).count
        let satisfactionCount = words.intersection(satisfactionWords).count
        
        // Simple weighted scoring
        if frustrationCount > 1 {
            emotion.valence = max(-1.0, emotion.valence - 0.3)
            emotion.arousal = min(1.0, emotion.arousal + 0.2)
            emotion.currentLabel = "FRUSTRATED"
        } else if satisfactionCount > 0 {
            emotion.valence = min(1.0, emotion.valence + 0.2)
            emotion.arousal = max(0.0, emotion.arousal - 0.1)
            emotion.currentLabel = "HAPPY"
        } else if curiosityCount > 0 {
            emotion.valence = min(1.0, emotion.valence + 0.1)
            emotion.arousal = min(1.0, emotion.arousal + 0.1)
            emotion.currentLabel = "CURIOUS"
        } else {
            // Decay toward neutral
            emotion.valence *= 0.9
            emotion.arousal *= 0.8
            emotion.currentLabel = "NEUTRAL"
        }
        
        // Check for ALL CAPS (frustration signal)
        let uppercaseRatio = Double(text.filter { $0.isUppercase }.count) / max(1.0, Double(text.count))
        if uppercaseRatio > 0.7 && text.count > 5 {
            emotion.arousal = min(1.0, emotion.arousal + 0.3)
            emotion.valence = max(-1.0, emotion.valence - 0.2)
            emotion.currentLabel = "FRUSTRATED"
        }
    }
    
    private func updateEngagement() {
        // Pace detection: queries per minute
        let recentQueries = queryTimestamps.filter {
            Date().timeIntervalSince($0) < 120  // Last 2 minutes
        }
        
        if recentQueries.count >= 5 {
            engagement = .deepFocus
        } else if recentQueries.count <= 1 {
            engagement = .disengaged
        } else {
            engagement = .casual
        }
    }
    
    private func updateTopic(from text: String) {
        // Simple topic extraction: longest capitalized word or noun phrase
        // In production, this would use NLP
        let words = text.split(separator: " ").map(String.init)
        let candidates = words.filter { $0.first?.isUppercase == true && $0.count > 2 }
        
        if let topic = candidates.first {
            currentTopic = topic
        }
    }
    
    private func updateExpertise(from text: String) {
        // Heuristic: longer, more technical queries = higher expertise
        let wordCount = text.split(separator: " ").count
        let hasJargon = text.contains("algorithm") || text.contains("protocol") ||
                        text.contains("architecture") || text.contains("implementation")
        
        if wordCount > 15 && hasJargon {
            expertiseLevel = min(1.0, expertiseLevel + 0.1)
        } else if wordCount < 5 {
            expertiseLevel = max(0.0, expertiseLevel - 0.05)
        }
    }
}

// MARK: - Supporting Types

struct EmotionalState {
    var valence: Double = 0.0      // -1.0 (negative) to 1.0 (positive)
    var arousal: Double = 0.0      // 0.0 (calm) to 1.0 (excited/angry)
    var dominance: Double = 0.5    // 0.0 (submissive) to 1.0 (dominant)
    var currentLabel: String = "NEUTRAL"
}

enum EngagementLevel: String {
    case deepFocus   = "DEEP_FOCUS"
    case casual      = "CASUAL"
    case disengaged  = "DISENGAGED"
}

struct Turn {
    let speaker: Speaker
    let text: String
    let timestamp: Date
    var verdict: String? = nil
    
    enum Speaker {
        case user
        case system
    }
}
