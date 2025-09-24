
# SDE v6 — FIRST/FOLLOW-Guided Error Recovery

- Sync set: {PLUS, STAR, RP, EOF}
- Actions:
  * synthesize `RP` when group likely open
  * skip unexpected tokens until sync
  * force-close T/F when stuck before sync
  * last resort: consume sync as ERROR
- ERROR nodes flagged with ⚠

Run:
  python demo_recovery.py
