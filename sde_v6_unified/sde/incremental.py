
from __future__ import annotations
from typing import Tuple, List
from bisect import bisect_left
from .lexer import lex, Token
from .ttlr import LRParser
from .astnodes import ASTNode

_metrics = {"climb_total":0,"climb_count":0,"fallbacks":0,"max_depth":0}

def parse_text(src: str) -> ASTNode:
    toks = lex(src)
    return LRParser(toks).parse()

def _leaf_positions(root: ASTNode) -> (List[int], List[ASTNode]):
    leaves = getattr(root, "_shift_nodes", None)
    if not leaves:
        leaves = [n for n in root.preorder() if not n.children]
    return [n.start for n in leaves], leaves

def fast_covering(root: ASTNode, start: int, end: int, budget:int) -> (ASTNode,bool,int):
    starts, leaves = _leaf_positions(root)
    if not leaves:
        return root, False, 0
    idx = bisect_left(starts, start)
    cand = leaves[min(idx, len(leaves)-1)]
    depth = 0
    n = cand
    while n and not (n.start <= start and end <= n.end):
        depth += 1
        if depth > budget:
            _metrics["fallbacks"] += 1
            return root, True, depth
        n = n.parent
    _metrics["climb_total"] += depth
    _metrics["climb_count"] += 1
    _metrics["max_depth"] = max(_metrics["max_depth"], depth)
    return (n or root), False, depth

def replace_child(parent: ASTNode, old_child: ASTNode, new_child: ASTNode):
    for i, c in enumerate(parent.children):
        if c is old_child:
            parent.children[i] = new_child
            new_child.parent = parent
            break
    parent.relabel_spans_up()

def incremental_edit(root: ASTNode, src_before: str, edit: Tuple[int,int,str], budget:int=5):
    s, e, text = edit
    new_src = src_before[:s] + text + src_before[e:]

    cover, fallback, depth = fast_covering(root, s, e, budget)
    print(f"EDIT {edit} cover={cover.kind}[{cover.start},{cover.end}] depth={depth} budget={budget} fallback={fallback}")

    if fallback:
        # Reparse whole source as a safe fallback (could be enclosing production in a richer impl.)
        return parse_text(new_src), new_src

    # Confined reparse on cover span adjusted for edit
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

    # mark reuse (simple span+kind check)
    old_spans = set((n.start, n.end, n.kind) for n in (parent.preorder() if parent else []))
    for n in root.preorder():
        n.reused = (n.start, n.end, n.kind) in old_spans

    return root, new_src

def metrics():
    return dict(_metrics)
