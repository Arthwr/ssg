from src.textnode import TextNode, TextType, split_nodes_delimiter
from src.htmlnode import HTMLNode, ParentNode


def main():
    new_textnode = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(new_textnode)

    new_htmlnode = HTMLNode("a", "https://google.com", None, {})
    new_parentnode = ParentNode("b", [new_htmlnode])
    print(new_parentnode.__repr__())

    node = TextNode(
        "**Lorem** ipsum dolor sit amet, consectetur adipiscing elit. Praesent. Neque porro quisquam est",
        TextType.TEXT,
    )

    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    print(new_nodes)


main()
