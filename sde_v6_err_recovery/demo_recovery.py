
from sde.incremental import parse_text
from sde.attrib import compute_value

def show(src):
    root = parse_text(src)
    val = compute_value(root)
    print("SRC:", src)
    print("VAL:", val)
    log = getattr(root, "_recovery_log", [])
    if log:
        print("RECOVERY LOG:")
        for item in log:
            print("  -", item)
    print("AST:")
    print(root.pretty())
    print("="*60)

if __name__ == "__main__":
    show("1+2*3")
    show("(1+2*3")
    show("1+ @@ 2 * (3")
