
from sde.incremental import parse_text, incremental_edit
from sde.attrib import compute_value

def main():
    src = "1+2*3"
    root = parse_text(src)
    val = compute_value(root)
    print("Initial source:", src)
    print("AST:\n", root.pretty())
    print("Value:", val)

    start = src.index("2")
    end = start + 1
    root, src = incremental_edit(root, src, (start, end, "5"))
    val = compute_value(root)
    print("\nAfter edit (2 -> 5):", src)
    print("AST:\n", root.pretty())
    print("Value:", val)

if __name__ == "__main__":
    main()
