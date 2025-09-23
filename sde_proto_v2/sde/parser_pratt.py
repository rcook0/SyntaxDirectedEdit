
from __future__ import annotations
from typing import List
from .lexer import Token
from .astnodes import ASTNode, make_leaf, make_node

PRECEDENCE = {"PLUS": 10, "STAR": 20}

class PrattParser:
    def __init__(self, tokens: List[Token]):
        self.toks = tokens
        self.i = 0

    def peek(self) -> Token:
        return self.toks[self.i]

    def pop(self) -> Token:
        t = self.toks[self.i]
        self.i += 1
        return t

    def parse(self) -> ASTNode:
        node = self.expr_bp(0)
        root = make_node("ROOT", [node])
        root.rebuild_threads()
        return root

    def parse_fragment(self) -> ASTNode:
        # parse a single expression and return its node (no ROOT wrapper)
        node = self.expr_bp(0)
        return node

    def nud(self, t: Token) -> ASTNode:
        if t.type == "NUM":
            return make_leaf("NUM", int(t.value), t.start, t.end)
        if t.type == "ID":
            return make_leaf("ID", t.value, t.start, t.end)
        if t.type == "LP":
            expr = self.expr_bp(0)
            rp = self.pop()
            if rp.type != "RP":
                rp = Token("RP", ")", expr.end, expr.end)
            node = make_node("GROUP", [make_leaf("LP","(", t.start, t.end), expr, make_leaf("RP",")", rp.start, rp.end)])
            return node
        return make_leaf(t.type, t.value, t.start, t.end)

    def led(self, left: ASTNode, t: Token) -> ASTNode:
        if t.type in ("PLUS","STAR"):
            rbp = PRECEDENCE[t.type]
            right = self.expr_bp(rbp)
            op = make_leaf(t.type, t.value, t.start, t.end)
            node = make_node("BINOP", [left, op, right])
            node.start = left.start
            node.end = right.end
            return node
        return make_node("ATTACH", [left, make_leaf(t.type, t.value, t.start, t.end)])

    def expr_bp(self, min_bp: int) -> ASTNode:
        t = self.pop()
        left = self.nud(t)
        while True:
            look = self.peek()
            if look.type not in PRECEDENCE:
                break
            lbp = PRECEDENCE[look.type]
            if lbp < min_bp:
                break
            t = self.pop()
            left = self.led(left, t)
        return left
