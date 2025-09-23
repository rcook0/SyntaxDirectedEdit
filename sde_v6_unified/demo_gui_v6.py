
import tkinter as tk
from tkinter import ttk
from sde.incremental import parse_text, incremental_edit, metrics
from sde.attrib import compute_value

class SDEGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SDE v6 Unified — Budget + Error Recovery")
        self.geometry("980x560")

        paned = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        left = ttk.Frame(paned); left.columnconfigure(0, weight=1); left.rowconfigure(0, weight=1)
        self.text = tk.Text(left, wrap="none", font=("Consolas", 12))
        self.text.grid(row=0, column=0, sticky="nsew")
        self.text.insert("1.0", "1+2*3")
        paned.add(left, weight=3)

        right = ttk.Frame(paned); right.columnconfigure(0, weight=1); right.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(right, columns=("span","val","reused"), show="tree headings")
        self.tree.heading("#0", text="Node")
        self.tree.heading("span", text="[start,end)")
        self.tree.heading("val", text="value")
        self.tree.heading("reused", text="reused")
        self.tree.grid(row=0, column=0, sticky="nsew")
        paned.add(right, weight=2)

        # Controls
        ctrl = ttk.Frame(self)
        ctrl.pack(fill="x")
        ttk.Label(ctrl, text="Ancestor budget:").pack(side="left", padx=6)
        self.budget_var = tk.IntVar(value=5)
        ttk.Spinbox(ctrl, from_=0, to=50, textvariable=self.budget_var, width=5).pack(side="left")
        self.metrics_var = tk.StringVar(value="metrics: n/a")
        ttk.Label(ctrl, textvariable=self.metrics_var).pack(side="right", padx=6)

        # Status
        self.status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status, anchor="w").pack(fill="x")

        # Model
        self.src = self.text.get("1.0", "end-1c")
        self.root = parse_text(self.src)
        compute_value(self.root)
        self.refresh_tree()

        # Bind
        self.text.bind("<KeyRelease>", self.on_key)

    def on_key(self, event):
        new_src = self.text.get("1.0", "end-1c")
        if new_src == self.src:
            return
        # crude diff to form (s,e,text)
        s = 0; old, new = self.src, new_src
        while s < len(old) and s < len(new) and old[s] == new[s]:
            s += 1
        e_old, e_new = len(old), len(new)
        while e_old > s and e_new > s and old[e_old-1] == new[e_new-1]:
            e_old -= 1; e_new -= 1
        text = new[s:e_new]

        try:
            self.root, self.src = incremental_edit(self.root, self.src, (s, e_old, text), budget=self.budget_var.get())
            val = compute_value(self.root)
            m = metrics()
            avg = (m["climb_total"]/m["climb_count"]) if m["climb_count"] else 0
            self.metrics_var.set(f"avgDepth={avg:.2f}  maxDepth={m['max_depth']}  fallbacks={m['fallbacks']}")
            self.status.set(f"OK | value={val}")
            self.refresh_tree()
        except Exception as ex:
            self.status.set(f"Error: {ex}")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        def add(node, parent=""):
            label = f"{node.kind}"
            if node.kind in ("NUM","ID","PLUS","STAR","LP","RP") and node.value is not None:
                label += f":{node.value}"
            if getattr(node, "disposable", False):
                label += "⚠"
            span = f"[{node.start},{node.end})"
            val = getattr(node, "_val", "")
            reused = "✓" if node.reused else ""
            item = self.tree.insert(parent, "end", text=label, values=(span, val, reused))
            for c in node.children:
                add(c, item)
        add(self.root)

if __name__ == "__main__":
    SDEGui().mainloop()
