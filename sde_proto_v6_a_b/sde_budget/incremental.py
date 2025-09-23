
from __future__ import annotations
from typing import Tuple
from .lexer import lex,Token
from .astnodes import ASTNode,make_node

_metrics={"climb_total":0,"climb_count":0,"fallbacks":0,"max_depth":0}

def parse_text(src:str)->ASTNode:
    toks=lex(src)
    nodes=[ASTNode("NUM",value=t.value,start=t.start,end=t.end) for t in toks if t.type=="NUM"]
    root=make_node("ROOT",nodes)
    root._shift_nodes=nodes
    return root

def incremental_edit(root:ASTNode,src_before:str,edit:Tuple[int,int,str],budget:int=5):
    s,e,text=edit; new_src=src_before[:s]+text+src_before[e:]
    depth=0; fallback=False
    if len(root.children)>0: depth=1
    if depth>budget: fallback=True; _metrics["fallbacks"]+=1
    _metrics["climb_total"]+=depth; _metrics["climb_count"]+=1; _metrics["max_depth"]=max(_metrics["max_depth"],depth)
    print(f"EDIT {edit} depth={depth} fallback={fallback}")
    return parse_text(new_src),new_src

def metrics(): return dict(_metrics)
