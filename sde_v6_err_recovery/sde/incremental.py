
from __future__ import annotations
from typing import Tuple
from .lexer import lex
from .ttlr import LRParser
from .astnodes import ASTNode

def parse_text(src: str) -> ASTNode:
    return LRParser(lex(src)).parse()

def incremental_edit(root: ASTNode, src_before: str, edit: Tuple[int,int,str], budget:int=5):
    s,e,text=edit
    new_src = src_before[:s] + text + src_before[e:]
    return parse_text(new_src), new_src
