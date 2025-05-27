from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode, ParentNode


def main():
    new_textnode = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(new_textnode)

    new_htmlnode = HTMLNode("a", "https://google.com", None, {})
    new_parentnode = ParentNode("b", [new_htmlnode])
    print(new_parentnode.__repr__())


main()
