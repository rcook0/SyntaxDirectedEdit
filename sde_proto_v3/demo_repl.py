
from sde.incremental import parse_text, incremental_edit
from sde.attrib import compute_value

def show(root, src):
    print("Source:", src)
    print(root.pretty())
    print("Value:", compute_value(root))

def main():
    src = input("Enter initial expression (e.g., 1+2*3): ").strip() or "1+2*3"
    root = parse_text(src)
    show(root, src)
    while True:
        cmd = input("\nedit <start> <end> <text> | q > ").strip()
        if cmd in ("q","quit","exit"):
            break
        if cmd.startswith("edit "):
            try:
                _, s, e, *text = cmd.split(" ")
                s = int(s); e = int(e); text = " ".join(text)
                root, src = incremental_edit(root, src, (s, e, text))
                show(root, src)
            except Exception as ex:
                print("Error:", ex)
        else:
            print("Unknown command.")
    print("Bye.")

if __name__ == "__main__":
    main()
