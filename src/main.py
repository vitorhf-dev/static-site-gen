from textnode import TextNode, TextType
from copystatic import copystatic

from textnode import text_node_to_html_node

def main():
    copystatic("static", "public")

if __name__ == "__main__":
    main()