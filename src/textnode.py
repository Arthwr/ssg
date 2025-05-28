from enum import Enum
from src.htmlnode import LeafNode


class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid conversion of text node: wrong TextType passed")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        raise Exception("Invalid or empty list of nodes")

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_list = []
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown: delimiter was not closed")

        for i in range(len(parts)):
            if len(parts[i]) == 0:
                continue

            if i % 2 == 0:
                current_type = TextType.TEXT
            else:
                current_type = text_type

            current_list.append(TextNode(parts[i], current_type))

        new_nodes.extend(current_list)

    return new_nodes
