# KNOWLEDGE PROTOCOL: The Living Library (Cortex)

## Philosophy

The AI system does not rely on constant API calls. It builds a **Local Library** of knowledge that grows over time. It only goes online to "Learn" (fetch/digest) new topics, then uses local files for "Recall" (latency-free, cost-free).

---

## 1. The Structure

The Library is divided into two strict tiers to prevent hoarding.

### Tier 1: Core Infrastructure (Heavy Cache)

- **Definition:** Tools, Professions, Identity.
- **Examples:** SolidWorks Manual, Python Syntax, Greeting Protocols, Project Axon Identity.
- **Retention:** Permanent (Unless uninstalled).
- **Refresh:** Checked monthly or on "Version Update" triggers.
- **Path:** `c:\antigravity\library\core\`

### Tier 2: Transient Context (Light Cache)

- **Definition:** Consumption, Pop-culture, One-off searches.
- **Examples:** Movie plots, News articles, Random website summaries.
- **Retention:** 24 Hours (Aggressive Decay).
- **Refresh:** None.
- **Path:** `c:\antigravity\library\transient\`

---

## 2. The Digester (PDF -> JSON)

AI cannot efficiently read PDFs in real-time. Knowledge must be "Digested" into AI-Native formats (JSON).

**Process:**

1.  **Ingest:** Download Human Format (PDF/HTML).
2.  **Extract:** API extracts key logic, actions, and errors.
3.  **Format:** Save as `Topic_Name.json`.
4.  **Discard:** Delete the original bulky file.

**JSON Structure Example (SolidWorks):**

```json
{
  "topic": "Extrude Boss",
  "trigger_keywords": ["extrude", "3d", "boss"],
  "action_path": ["Features", "Extrude Boss/Base"],
  "common_errors": {
    "Zero Thickness": "Geometry touches at a single point. Fix sketch.",
    "Open Contour": "Sketch is not closed."
  },
  "last_updated": "2025-12-31"
}
```

---

## 3. The Lifecycle

1.  **Thalamus Query:** "How do I extrude in Blender?"
2.  **Local Check:** `library\core\blender.json`? -> **MISSING.**
3.  **Librarian Trigger:**
    - Fetch "Blender Extrude Manual".
    - Digest to JSON.
    - Save to `library\core\blender.json`.
4.  **Response:** "Press 'E' to extrude." (Read from local).

---

## 4. Guardrails

- **API Limit:** Max 5 "Learns" per hour.
- **Storage Limit:** Max 100MB for Tier 2.
- **Privacy:** No personal user data (passwords/names) is ever written to the Library.

_Version 1.0_
