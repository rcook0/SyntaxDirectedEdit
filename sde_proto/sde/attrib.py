
from __future__ import annotations
from collections import deque
from typing import Dict, Set
from .astnodes import ASTNode

def compute_value(root: ASTNode, env: Dict[str,int]|None=None) -> int:
    """
    Recompute 'val' attribute for all nodes reachable from root using a worklist.
    Returns the value for the expression at root (ROOT->expr).
    """
    env = env or {}
    q = deque(n for n in root.preorder())

    while q:
        n = q.popleft()
        old = getattr(n, "_val", None)
        new = eval_node(n, env)
        if new != old:
            n._val = new
            if n.parent:
                q.append(n.parent)

    if root.children:
        return getattr(root.children[0], "_val", None)
    return None

def eval_node(n: ASTNode, env: Dict[str,int]|None=None):
    env = env or {}
    if n.kind == "NUM":
        return n.value
    if n.kind == "ID":
        return env.get(n.value, 0)
    if n.kind == "GROUP":
        if len(n.children) >= 2:
            return getattr(n.children[1], "_val", None)
        return None
    if n.kind == "BINOP":
        left, op, right = n.children
        lv = getattr(left, "_val", None)
        rv = getattr(right, "_val", None)
        if lv is None or rv is None:
            return None
        if op.value == "+":
            return lv + rv
        if op.value == "*":
            return lv * rv
        return None
    if n.children:
        return getattr(n.children[0], "_val", None)
    return None
