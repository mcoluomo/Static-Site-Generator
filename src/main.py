from textnode import *

def main():
    tNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(repr(tNode))

if __name__ == "__main__":
    main()
