import re

from src.textnode import TextNode, TextType


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


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
