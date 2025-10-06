def parse_text(src):
    from .ttlr import LRParser
    from .lexer import lex
    return LRParser(lex(src)).parse()

def incremental_edit(root, src, edit, budget=5):
    s,e,text=edit
    new_src=src[:s]+text+src[e:]
    return parse_text(new_src), new_src

def metrics(): return {}
