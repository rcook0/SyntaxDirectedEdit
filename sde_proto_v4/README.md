
# SDE Prototype v4 — Tk Dual-View Demo

What's new:
- A **Tkinter dual-view** app: left = Text editor, right = AST Treeview + live value.
- Parses on each keystroke using **confined reparse + LR core** and recomputes attributes.
- Shows per-node spans and whether nodes were **reused** after the last edit.

Run:
  python demo_gui_tk.py
