
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any

@dataclass
class ASTNode:
    kind: str
    children: List["ASTNode"] = field(default_factory=list)
    value: Any = None
    start: int = 0
    end: int = 0
    parent: Optional["ASTNode"] = None
    thread_prev: Optional["ASTNode"] = None
    reused: bool = False
    disposable: bool = False

    def set_span(self, start: int, end: int):
        self.start, self.end = start, end

    def adopt(self, child: "ASTNode"):
        child.parent = self
        self.children.append(child)

    def preorder(self):
        yield self
        for c in self.children:
            yield from c.preorder()

    def rebuild_threads(self):
        prev = None
        for n in self.preorder():
            n.thread_prev = prev
            prev = n

    def pretty(self, depth=0):
        pad = "  " * depth
        info = f"{self.kind}[{self.start},{self.end}]"
        if self.value is not None and self.kind in ('NUM','ID'):
            info += f":{self.value}"
        lines = [pad + info]
        for c in self.children:
            lines.append(c.pretty(depth+1))
        return "\n".join(lines)

def make_leaf(kind: str, value, start: int, end: int) -> ASTNode:
    n = ASTNode(kind=kind, value=value, start=start, end=end)
    return n

def make_node(kind: str, children: List[ASTNode]) -> ASTNode:
    n = ASTNode(kind=kind)
    n.children = children
    for c in children:
        c.parent = n
    if children:
        n.start = children[0].start
        n.end = children[-1].end
    return n
