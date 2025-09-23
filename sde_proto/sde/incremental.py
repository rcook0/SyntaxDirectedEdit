
from __future__ import annotations
from typing import Tuple
from .lexer import lex
from .parser import Parser
from .astnodes import ASTNode

def parse_text(src: str) -> ASTNode:
    toks = lex(src)
    root = Parser(toks).parse()
    return root

def find_covering(node: ASTNode, start: int, end: int) -> ASTNode:
    best = None
    for n in node.preorder():
        if n.start <= start and end <= n.end:
            if best is None or (n.end - n.start) < (best.end - best.start):
                best = n
    return best or node

def incremental_edit(root: ASTNode, src_before: str, edit: Tuple[int,int,str]):
    s, e, text = edit
    new_src = src_before[:s] + text + src_before[e:]
    new_root = parse_text(new_src)

    old_spans = {(n.start, n.end, n.kind) for n in root.preorder()}
    for n in new_root.preorder():
        n.reused = (n.start, n.end, n.kind) in old_spans
    return new_root, new_src
