from textnode import TextNode, TextType

from textnode import text_node_to_html_node

def main():
    node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()