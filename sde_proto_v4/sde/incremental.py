
from __future__ import annotations
from typing import Tuple
from .lexer import lex, Token
from .ttlr import LRParser
from .astnodes import ASTNode

def parse_text(src: str) -> ASTNode:
    toks = lex(src)
    root = LRParser(toks).parse()
    return root

def find_covering(node: ASTNode, start: int, end: int) -> ASTNode:
    best = None
    for n in node.preorder():
        if n.start <= start and end <= n.end:
            if best is None or (n.end - n.start) < (best.end - best.start):
                best = n
    return best or node

def replace_child(parent: ASTNode, old_child: ASTNode, new_child: ASTNode):
    for i, c in enumerate(parent.children):
        if c is old_child:
            parent.children[i] = new_child
            new_child.parent = parent
            break
    parent.relabel_spans_up()

def incremental_edit(root: ASTNode, src_before: str, edit: Tuple[int,int,str]):
    s, e, text = edit
    new_src = src_before[:s] + text + src_before[e:]
    cover = find_covering(root, s, e)

    delta = len(text) - (e - s)
    new_cover_end = cover.end + delta if cover.end >= e else cover.end
    slice_start = cover.start
    slice_end = max(new_cover_end, s + len(text))
    slice_start = max(0, slice_start)
    slice_end = min(len(new_src), slice_end)

    tokens = lex(new_src[slice_start:slice_end])
    tokens = [Token(t.type, t.value, t.start + slice_start, t.end + slice_start) for t in tokens]
    frag = LRParser(tokens).parse_fragment()

    parent = cover.parent or root
    replace_child(parent, cover, frag)

    while parent.parent:
        parent = parent.parent
    root = parent
    while root.parent:
        root = root.parent
    if root.kind != "ROOT":
        root = parse_text(new_src)
    else:
        root.rebuild_threads()

    old_spans = set((n.start, n.end, n.kind) for n in (parent.preorder() if parent else []))
    for n in root.preorder():
        n.reused = (n.start, n.end, n.kind) in old_spans

    return root, new_src
