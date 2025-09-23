
from __future__ import annotations
from typing import Tuple
from .lexer import lex,Token
from .astnodes import ASTNode,make_leaf,make_node

def parse_text(src:str)->ASTNode:
    toks=lex(src); nodes=[]
    for t in toks:
        if t.type in ("NUM","ID"):
            nodes.append(make_leaf(t.type,t.value,t.start,t.end))
        elif t.type=="UNK":
            err=ASTNode("ERROR",start=t.start,end=t.end); err.disposable=True; nodes.append(err)
    root=make_node("ROOT",nodes); root._shift_nodes=nodes; return root

def incremental_edit(root:ASTNode,src_before:str,edit:Tuple[int,int,str]):
    s,e,text=edit; new_src=src_before[:s]+text+src_before[e:]
    return parse_text(new_src),new_src
