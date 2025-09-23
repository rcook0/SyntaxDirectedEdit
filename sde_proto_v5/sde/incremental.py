
from __future__ import annotations
from typing import Tuple, List
from bisect import bisect_left
from .lexer import lex, Token
from .ttlr import LRParser
from .astnodes import ASTNode

def parse_text(src: str) -> ASTNode:
    toks = lex(src)
    root = LRParser(toks).parse()
    return root

def _leaf_positions(root: ASTNode) -> List[int]:
    leaves = getattr(root, "_shift_nodes", None)
    if not leaves:
        # fallback: collect from preorder
        leaves = [n for n in root.preorder() if not n.children]
    return [n.start for n in leaves], leaves

def fast_covering(root: ASTNode, start: int, end: int) -> ASTNode:
    # Use shift-node positions to pick the nearest leaf to 'start', then climb to covering ancestor.
    starts, leaves = _leaf_positions(root)
    if not leaves:
        return root
    idx = bisect_left(starts, start)
    cand = None
    if idx < len(leaves):
        cand = leaves[idx]
    elif idx > 0:
        cand = leaves[idx-1]
    else:
        cand = leaves[0]
    # climb to minimal covering ancestor
    n = cand
    while n and not (n.start <= start and end <= n.end):
        n = n.parent
    return n or root

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
    cover = fast_covering(root, s, e)

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
