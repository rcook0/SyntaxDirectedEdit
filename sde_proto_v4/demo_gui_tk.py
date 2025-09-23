
import tkinter as tk
from tkinter import ttk, messagebox
from sde.incremental import parse_text, incremental_edit
from sde.attrib import compute_value

class SDEGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SDE Dual-View Demo (Tk)")
        self.geometry("900x500")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        paned = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        paned.grid(row=0, column=0, sticky="nsew")

        # Left: Text editor
        left = ttk.Frame(paned); left.columnconfigure(0, weight=1); left.rowconfigure(0, weight=1)
        self.text = tk.Text(left, wrap="none", font=("Consolas", 12))
        self.text.grid(row=0, column=0, sticky="nsew")
        self.text.insert("1.0", "1+2*3")
        paned.add(left, weight=3)

        # Right: AST tree
        right = ttk.Frame(paned); right.columnconfigure(0, weight=1); right.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(right, columns=("span","val","reused"), show="tree headings")
        self.tree.heading("#0", text="Node")
        self.tree.heading("span", text="[start,end)")
        self.tree.heading("val", text="attr(value)")
        self.tree.heading("reused", text="reused")
        self.tree.grid(row=0, column=0, sticky="nsew")
        paned.add(right, weight=2)

        # Status bar
        self.status = tk.StringVar(value="Ready")
        statusbar = ttk.Label(self, textvariable=self.status, anchor="w")
        statusbar.grid(row=1, column=0, sticky="ew")

        # Model
        self.src = self.text.get("1.0", "end-1c")
        self.root = parse_text(self.src)
        compute_value(self.root)
        self.refresh_tree()

        # Bindings
        self.text.bind("<KeyRelease>", self.on_key_release)

    def on_key_release(self, event):
        new_src = self.text.get("1.0", "end-1c")
        # compute edit diff (simple: find first mismatch)
        s = 0
        old, new = self.src, new_src
        while s < len(old) and s < len(new) and old[s] == new[s]:
            s += 1
        if old == new:
            return
        # find end
        e_old, e_new = len(old), len(new)
        while e_old > s and e_new > s and old[e_old-1] == new[e_new-1]:
            e_old -= 1; e_new -= 1
        insert_text = new[s:e_new]
        try:
            self.root, self.src = incremental_edit(self.root, self.src, (s, e_old, insert_text))
            val = compute_value(self.root)
            self.status.set(f"OK | value={val}")
            self.refresh_tree()
        except Exception as ex:
            self.status.set(f"Parse error: {ex}")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        def add(node, parent=""):
            label = f"{node.kind}"
            if node.kind in ("NUM","ID","PLUS","STAR","LP","RP") and node.value is not None:
                label += f":{node.value}"
            span = f"[{node.start},{node.end})"
            val = getattr(node, "_val", "")
            reused = "✓" if node.reused else ""
            item = self.tree.insert(parent, "end", text=label, values=(span, val, reused))
            for c in node.children:
                add(c, item)
        add(self.root)

if __name__ == "__main__":
    app = SDEGui()
    app.mainloop()
