
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type:str; value:str; start:int; end:int

def lex(src:str)->List[Token]:
    i,n=0,len(src); out=[]
    while i<n:
        ch=src[i]
        if ch.isspace(): i+=1; continue
        if ch.isdigit():
            j=i
            while j<n and src[j].isdigit(): j+=1
            out.append(Token("NUM",src[i:j],i,j)); i=j; continue
        if ch.isalpha() or ch=="_":
            j=i
            while j<n and (src[j].isalnum() or src[j]=="_"): j+=1
            out.append(Token("ID",src[i:j],i,j)); i=j; continue
        if ch in "+*()":
            typ={"+":"PLUS","*":"STAR","(":"LP",")":"RP"}[ch]
            out.append(Token(typ,ch,i,i+1)); i+=1; continue
        out.append(Token("UNK",ch,i,i+1)); i+=1
    out.append(Token("EOF","",n,n)); return out
