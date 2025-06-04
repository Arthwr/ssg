import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_list = []
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown: delimiter was not closed")

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


def partition_nodes_by_media(old_nodes, media_asset_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text_content = node.text

        if media_asset_type == TextType.IMAGE:
            asset_list = extract_markdown_images(text_content)
        elif media_asset_type == TextType.LINK:
            asset_list = extract_markdown_links(text_content)
        else:
            raise ValueError("Invalid asset type: non image or link")

        if len(asset_list) == 0:
            new_nodes.append(node)
            continue

        for asset_node in asset_list:
            alt_text = asset_node[0]
            link = asset_node[1]

            if media_asset_type == TextType.IMAGE:
                delimiter = f"![{alt_text}]({link})"
            elif media_asset_type == TextType.LINK:
                delimiter = f"[{alt_text}]({link})"

            sections = text_content.split(delimiter, 1)

            if len(sections[0]) != 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, media_asset_type, link))
            text_content = sections[1]

        if len(text_content) != 0:
            new_nodes.append(TextNode(text_content, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    return partition_nodes_by_media(old_nodes, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return partition_nodes_by_media(old_nodes, TextType.LINK)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
