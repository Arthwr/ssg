from enum import Enum

from src.htmlnode import HTMLNode, ParentNode, LeafNode
from src.textnode import TextNode, TextType
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = (block.strip() for block in markdown.split("\n\n"))
    return [block for block in blocks if block]


def block_to_block_type(markdown_block):
    lines = markdown_block.strip().split("\n")

    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines if line.strip()):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines if line.strip()):
        return BlockType.UNORDERED_LIST

    for idx, line in enumerate(lines):
        if not line.startswith(f"{idx+1}. "):
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    converted_block_nodes = []

    for markdown_block in blocks:
        block_type = block_to_block_type(markdown_block)
        block_html_node = block_to_html_node(markdown_block, block_type)
        converted_block_nodes.append(block_html_node)

    return ParentNode("div", converted_block_nodes, None)


def text_to_children(block):
    text_nodes = text_to_textnodes(block)
    return list(map(text_node_to_html_node, text_nodes))


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise Exception(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)

    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])

    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)

    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", html_items)


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ol", html_items)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)

    return ParentNode("p", children)


def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.HEADING:
            return heading_to_html_node(block)

        case BlockType.CODE:
            return code_to_html_node(block)

        case BlockType.QUOTE:
            return quote_to_html_node(block)

        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)

        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)

        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)

        case _:
            raise ValueError("invalid block type")
