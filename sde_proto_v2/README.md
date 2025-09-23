
# SDE Prototype v2

This revision implements **confined reparse & graft** around the edit region, and introduces
a **Threaded-Tree LR (TTLR) scaffold** with a stable API. For now, the LR layer delegates to
a Pratt parser for the toy grammar so we can validate incrementality and the AST/attribute contracts.
In Phase 1.2, swap in real LR ACTION/GOTO tables without touching callers.

Run:
  python demo_script.py
  python demo_repl.py
