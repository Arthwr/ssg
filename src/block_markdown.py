import re

from enum import Enum


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
