# Optic Nerve: Upgrade Plan (v3.0 -> v4.0)

## 1. Current State (The v3.0 Core)

You currently have `optic_nerve.py` (v3.0) from `ANTIGRAVITY_COMPLETE_v3.zip`.

### capabilities:

- **The Eyeball (Basic)**:
  - Uses `user32.GetForegroundWindow` to see the **one** active window.
  - Returns: Window Title + Process ID.
  - _Limitation_: Blind to background windows, multi-monitor setups, and occluded apps.
- **The Finger (Interrogation)**:
  - Uses `UIAutomation` to get the focused element (Button, Text Field) within that active window.
  - _Status_: Functional. Keeping as is.
- **The Ear (Keylogger)**:
  - Detects `Enter`, `Esc`, `Ctrl+S`, `Ctrl+Z`.
  - _Status_: Functional. Keeping as is.
- **Wait State Optimization**:
  - Dials down CPU usage when the mouse stops moving.
  - _Status_: Functional. Keeping as is.

---

## 2. The Upgrade Logic (Road to v4.0)

We are upgrading two core systems: **Vision** (Gap 2) and **Memory** (Gap 3).

### A. The Vision Upgrade (Gap 2: Multi-Monitor & Occlusion)

**What is changing?**
We are **replacing** the simple `get_active_window_info()` function with a new **`WindowMap` Engine**.

| Feature       | Old Logic (v3.0)            | New Logic (v4.0)                                                                                           |
| :------------ | :-------------------------- | :--------------------------------------------------------------------------------------------------------- |
| **Scope**     | Sees 1 Window (Foreground). | Sees **All** Windows.                                                                                      |
| **Filtering** | None.                       | **Occlusion Check**: Compares window rectangles. If Window A covers Window B, Window B is marked `HIDDEN`. |
| **Staleness** | None.                       | **Decay Timer**: Tracks `LastInteractionTime`. "Dormant" windows (unused > 1hr) are ignored.               |
| **Monitors**  | Blind.                      | **Monitor Tagging**: Identifies if a window is on Observer-Left (Screen 1) or Observer-Right (Screen 2).   |

**How it works:**

1. Calls `EnumWindows` to get the full Z-Order list (Top to Bottom).
2. Calculates which windows are actually visible to you vs. which are covered by others (like your Arc Browser behind Antigravity).
3. Returns a `DesktopState` object describing your full environment.

---

### B. The Memory Upgrade (Gap 3: Clipboard & Context)

**What is changing?**
We are **adding** a `ClipboardScribe` class. This is new code; it does not replace existing features.

| Feature         | Old Logic (v3.0)        | New Logic (v4.0)                                                                                                             |
| :-------------- | :---------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Tracking**    | Blind to data movement. | **Sequence Listener**: Checks `GetClipboardSequenceNumber` every 1.0s.                                                       |
| **Content**     | N/A                     | **Metadata Only**: Logs "Copied 3 Files from Explorer" or "Copied Image (800x600)". **No heavy data storage.**               |
| **Drag & Drop** | Invisible.              | **Inference Engine**: Detects `DragStart` (Explorer) -> `DragEnd` (SolidWorks) based on mouse state and window focus shifts. |

---

## 3. Summary of Files Touched

1.  **`optic_nerve.py`**:

    - **MODIFY**: `get_active_window_info()` -> Replaced by `get_desktop_state()`.
    - **ADD**: `ClipboardScribe` class.
    - **ADD**: `WindowMap` class (for occlusion logic).
    - **UPDATE**: `translate_to_human()` to handle multiple visible windows (e.g., "Focus: SolidWorks | Periheral: Ref_Image").

2.  **No other files** (`thalamus_engine.py`, `brain_server.py`) will be touched in this specific update cycle.
