
# SDE v6 (Unified) — Budgeted Incrementality + Error Recovery

This package integrates:
- **Configurable ancestor budget** for confined reparse (with metrics: avg/max depth, fallbacks).
- **Error-tolerant LR parser** that creates `ERROR⚠` nodes rather than hard-failing.
- **Tk GUI** with a budget spinner, live metrics, AST view, and computed value.

Run:
  python demo_gui_v6.py
