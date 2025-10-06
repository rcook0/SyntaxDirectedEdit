# Syntax-Directed Editor — v7

## Overview
An incremental, syntax-directed editor core with deterministic LR parsing, robust error recovery,
and confined reparses with an ancestor budget. Dual-view GUI and micro-benchmark harness included.

## Release Notes (from v1 to v7)
- v1–v2: LR skeleton, AST, attributes.
- v3: Dual-view GUI.
- v4: Stack-thread integration (shift-order terminals).
- v5: Ancestor budget hooks + metrics.
- v6a: Budgeted climb metrics + delta prints.
- v6b: Error productions (ERROR⚠ nodes).
- v6 (Unified): Budget + error-tolerant parsing together.
- v6 (FIRST/FOLLOW): Guided recovery tactics (synthesize `RP`, skip, force-close T/F, consume sync).
- v6 (Token-boundary): Slice expansion to token boundaries.
- v7: Paren-aware widening + benchmark harness + polished GUI.

## Usage
GUI:   python demo_gui_v7.py
Bench: python bench_typing.py

## Roadmap
- Rich FIRST/FOLLOW generation, better sync sets.
- Attribute delta graph, dependency pruning.
- Token cache/piece table for large buffers.
- LSP/VSCode integration.