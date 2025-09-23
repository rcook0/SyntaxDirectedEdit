
# SDE Prototype v5 — Stack-Thread Integration Hooks

What's new:
- LR parser now records **shift (terminal) nodes** in source order and attaches them to the root as `_shift_nodes`.
- Incremental edit uses these leaves to compute a **fast covering node** near the edit span, reducing search overhead.
- Tk dual-view demo updated (v5 banner).

Run:
  python demo_gui_tk.py
