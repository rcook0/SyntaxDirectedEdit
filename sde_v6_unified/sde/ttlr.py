
from __future__ import annotations
from typing import List, Tuple, Dict
from .lexer import Token
from .astnodes import ASTNode, make_leaf, make_node

# Rules:
# 1: E -> E PLUS T
# 2: E -> T
# 3: T -> T STAR F
# 4: T -> F
# 5: F -> LP E RP
# 6: F -> NUM
# 7: F -> ID

ACTION: Dict[int, Dict[str, Tuple[str, int]]] = {
    0: {'LP':('s',4), 'ID':('s',5), 'NUM':('s',6)},
    1: {'PLUS':('s',7), 'EOF':('acc',0)},
    2: {'PLUS':('r',2), 'STAR':('s',8), 'RP':('r',2), 'EOF':('r',2)},
    3: {'PLUS':('r',4), 'STAR':('r',4), 'RP':('r',4), 'EOF':('r',4)},
    4: {'LP':('s',4), 'ID':('s',5), 'NUM':('s',6)},
    5: {'PLUS':('r',7), 'STAR':('r',7), 'RP':('r',7), 'EOF':('r',7)},
    6: {'PLUS':('r',6), 'STAR':('r',6), 'RP':('r',6), 'EOF':('r',6)},
    7: {'LP':('s',4), 'ID':('s',5), 'NUM':('s',6)},
    8: {'LP':('s',4), 'ID':('s',5), 'NUM':('s',6)},
    9: {'PLUS':('s',7), 'RP':('s',12)},
    10:{'PLUS':('r',1), 'STAR':('s',8), 'RP':('r',1), 'EOF':('r',1)},
    11:{'PLUS':('r',3), 'STAR':('r',3), 'RP':('r',3), 'EOF':('r',3)},
    12:{'PLUS':('r',5), 'STAR':('r',5), 'RP':('r',5), 'EOF':('r',5)},
}

GOTO: Dict[int, Dict[str, int]] = {
    0: {'E':1, 'T':2, 'F':3},
    4: {'E':9, 'T':2, 'F':3},
    7: {'T':10, 'F':3},
    8: {'F':11},
    9: {}, 10:{}, 11:{}, 12:{}
}

def reduce_build(rule: int, stack: List[Tuple[int, ASTNode]]):
    if rule == 1:
        sT, nodeT = stack[-1]
        sPLUS, nodePLUS = stack[-2]
        sE, nodeE = stack[-3]
        binop = make_node("BINOP", [nodeE, make_leaf("PLUS", "+", nodePLUS.start, nodePLUS.end), nodeT])
        return "E", binop, 3
    if rule == 2:
        return "E", stack[-1][1], 1
    if rule == 3:
        sF, nodeF = stack[-1]
        sSTAR, nodeSTAR = stack[-2]
        sT, nodeT = stack[-3]
        binop = make_node("BINOP", [nodeT, make_leaf("STAR", "*", nodeSTAR.start, nodeSTAR.end), nodeF])
        return "T", binop, 3
    if rule == 4:
        return "T", stack[-1][1], 1
    if rule == 5:
        sRP, nodeRP = stack[-1]
        sE, nodeE = stack[-2]
        sLP, nodeLP = stack[-3]
        group = make_node("GROUP", [make_leaf("LP","(", nodeLP.start, nodeLP.end), nodeE, make_leaf("RP",")", nodeRP.start, nodeRP.end)])
        return "F", group, 3
    if rule == 6:
        return "F", stack[-1][1], 1
    if rule == 7:
        return "F", stack[-1][1], 1
    raise ValueError(f"Unknown rule {rule}")

class LRParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.shift_nodes: List[ASTNode] = []

    def parse(self) -> ASTNode:
        stack: List[Tuple[int, ASTNode]] = [(0, ASTNode(kind='^', start=0, end=0))]
        i = 0
        while True:
            state = stack[-1][0]
            t = self.tokens[i]
            act = ACTION.get(state, {}).get(t.type)
            if act is None:
                # Error-tolerant behavior:
                # 1) If expecting RP at EOF, synthesize
                if t.type == 'EOF' and state in (9,):
                    fake = Token('RP', ')', t.start, t.end)
                    self.tokens.insert(i, fake)
                    continue
                # 2) Otherwise, create an ERROR node for this token and "shift" it to move on
                err = ASTNode(kind='ERROR', start=t.start, end=t.end, disposable=True)
                self.shift_nodes.append(err)
                # Thread it by pushing with same state (no state change) and consuming token
                stack.append((state, err))
                i += 1
                # If we hit EOF with error, accept a minimal root to keep AST connected
                if t.type == 'EOF':
                    root = make_node('ROOT', [err])
                    setattr(root, "_shift_nodes", self.shift_nodes)
                    root.rebuild_threads()
                    return root
                continue
            kind, arg = act
            if kind == 's':
                val = int(t.value) if t.type=='NUM' else t.value or t.type
                node = ASTNode(kind=t.type, value=val, start=t.start, end=t.end)
                self.shift_nodes.append(node)
                stack.append((arg, node))
                i += 1
            elif kind == 'r':
                lhs, node, popn = reduce_build(arg, stack)
                for _ in range(popn):
                    stack.pop()
                state2 = stack[-1][0]
                goto = GOTO.get(state2, {}).get(lhs)
                if goto is None:
                    # Turn this into an ERROR and continue
                    err = ASTNode(kind='ERROR', start=node.start, end=node.end, disposable=True)
                    stack.append((state2, err))
                    continue
                stack.append((goto, node))
            elif kind == 'acc':
                root = make_node('ROOT', [stack[-1][1]])
                setattr(root, "_shift_nodes", self.shift_nodes)
                root.rebuild_threads()
                return root

    def parse_fragment(self) -> ASTNode:
        r = self.parse()
        return r.children[0] if r.children else r
