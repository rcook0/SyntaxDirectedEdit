
# SDE Prototype v3 — LR Core

This revision replaces the Pratt delegate with a **real shift–reduce LR core** for the classic grammar:

  1) E -> E + T
  2) E -> T
  3) T -> T * F
  4) T -> F
  5) F -> ( E )
  6) F -> NUM
  7) F -> ID

- Hardcoded ACTION/GOTO tables for 13 states, with precedence ( * over + ) and left-assoc.
- Reductions build AST: BINOP('+'), BINOP('*'), GROUP('(', E, ')').
- **Confined reparse + graft** retained from v2.

Run:
  python demo_script.py
  python demo_repl.py
