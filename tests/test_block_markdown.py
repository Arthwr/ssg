import unittest
from src.block_markdown import BlockType, markdown_to_blocks, block_to_block_type


class TestBlockMarkdownSplit(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_heading1(self):
        text_block = "# This is a heading"
        block_type = block_to_block_type(text_block)

        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_heading2(self):
        text_block = "## This is a heading"
        block_type = block_to_block_type(text_block)

        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_heading6(self):
        text_block = "###### This is a heading"
        block_type = block_to_block_type(text_block)

        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_wrong_heading(self):
        text_block = "####### This is a heading"
        block_type = block_to_block_type(text_block)

        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_wrong_nospace__heading(self):
        text_block = "#This is a heading"
        block_type = block_to_block_type(text_block)

        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_code(self):
        text_block = """```js
console.log("Hello world")
```"""
        block_type = block_to_block_type(text_block)

        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_code_single(self):
        text_block = """```
code
```"""
        block_type = block_to_block_type(text_block)

        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_quote_multiple(self):
        text_block = """> Hello
> This is a quote
> This one as well"""

        block_type = block_to_block_type(text_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_unordered_list(self):
        text_block = """- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        block_type = block_to_block_type(text_block)

        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_ordered_list(self):
        text_block = """1. This is the first list item in a list block
2. This is a list item
3. This is another list item
"""
        block_type = block_to_block_type(text_block)

        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_invalid_starting_ordered_list(self):
        text_block = """2. This is the first list item in a list block
3. This is a list item
4. This is another list item
"""
        block_type = block_to_block_type(text_block)

        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_misordered_list(self):
        text_block = """1. This is the first list item in a list block
3. This is a list item
5. This is another list item
"""
        block_type = block_to_block_type(text_block)

        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
