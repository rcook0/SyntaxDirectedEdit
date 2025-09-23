
"""
Threaded-Tree LR (TTLR) scaffold.

This module defines a table-driven LR parser interface and threaded-tree hooks,
but delegates to the Pratt parser for the toy grammar to keep Phase 1 velocity.
The public API is stable: swap the Pratt delegate with real LR ACTION/GOTO tables
without changing callers.

TODO (Phase 1.2):
- Populate ACTION/GOTO for the classic E->E+T|T, T->T*F|F, F->(E)|NUM|ID grammar
  and resolve conflicts via precedence (STAR > PLUS).
- Maintain a parse stack with tree nodes; store thread pointers from the stack.
"""
from __future__ import annotations
from typing import List
from .lexer import Token
from .astnodes import ASTNode
from .parser_pratt import PrattParser

class LRParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def parse(self) -> ASTNode:
        # Delegate to Pratt for now; returns ROOT-wrapped AST
        return PrattParser(self.tokens).parse()

    def parse_fragment(self) -> ASTNode:
        # Return an expression node (no ROOT wrapper)
        return PrattParser(self.tokens).parse_fragment()
