import unittest
from markdown.block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


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


class TestMarkdownBlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
