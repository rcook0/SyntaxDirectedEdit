
import tkinter as tk
from tkinter import ttk

USE_ERROR_ENGINE=False
if USE_ERROR_ENGINE:
    from sde_error.incremental import parse_text,incremental_edit
    from sde_error.attrib import compute_value
else:
    from sde_budget.incremental import parse_text,incremental_edit,metrics
    from sde_budget.attrib import compute_value

class Gui(tk.Tk):
    def __init__(self):
        super().__init__(); self.geometry("800x400"); self.title("Budget vs Error Engine")
        self.text=tk.Text(self); self.text.pack(side="left",fill="both",expand=True)
        self.tree=ttk.Treeview(self); self.tree.pack(side="right",fill="both",expand=True)
        self.src="1+2"; self.text.insert("1.0",self.src); self.root=parse_text(self.src); compute_value(self.root); self.refresh()
        self.text.bind("<KeyRelease>",self.on_key)

    def on_key(self,e):
        new=self.text.get("1.0","end-1c")
        self.root,self.src=incremental_edit(self.root,self.src,(0,len(self.src),new))
        compute_value(self.root); self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        def add(n,p=""):
            lbl=n.kind; span=f"[{n.start},{n.end}]"
            self.tree.insert(p,"end",text=lbl,values=(span,))
            for c in n.children: add(c)
        add(self.root)

if __name__=="__main__": Gui().mainloop()
