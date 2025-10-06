class LRParser:
    def __init__(self, toks): self.toks=toks
    def parse(self):
        class Dummy: pass
        r=Dummy(); r.children=[]; return r
