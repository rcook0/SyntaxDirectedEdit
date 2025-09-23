
from sde.incremental import parse_text, incremental_edit
from sde.attrib import compute_value

def main():
    src = "1+2*3"
    root = parse_text(src)
    print("Initial AST:\n", root.pretty())
    print("Value:", compute_value(root))

    # Edit '2' -> '5'
    start = src.index("2"); end = start+1
    root, src = incremental_edit(root, src, (start, end, "5"))
    print("\nAfter edit:", src)
    print(root.pretty())
    print("Value:", compute_value(root))

if __name__ == "__main__":
    main()
