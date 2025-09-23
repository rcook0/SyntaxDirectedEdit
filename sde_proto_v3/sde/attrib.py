
from __future__ import annotations
from collections import deque
from typing import Dict
from .astnodes import ASTNode

def compute_value(root: ASTNode, env: Dict[str,int]|None=None) -> int:
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

def eval_node(n: ASTNode, env: Dict[str,int]):
    if n.kind == "NUM":
        return n.value
    if n.kind == "ID":
        return env.get(n.value, 0)
    if n.kind == "GROUP":
        return getattr(n.children[1], "_val", None) if len(n.children) >= 2 else None
    if n.kind == "BINOP":
        left, op, right = n.children
        lv = getattr(left, "_val", None)
        rv = getattr(right, "_val", None)
        if lv is None or rv is None:
            return None
        return lv + rv if op.value == "+" else (lv * rv if op.value == "*" else None)
    if n.children:
        return getattr(n.children[0], "_val", None)
    return None
