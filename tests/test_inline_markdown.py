import unittest

from src.textnode import TextNode, TextType
from src.inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)


class TestTextSplitNodes(unittest.TestCase):
    def test_single_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_first_bold_long_split(self):
        node = TextNode(
            "**Lorem** ipsum dolor sit amet, consectetur adipiscing elit. Praesent. Neque porro quisquam est",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Lorem", TextType.BOLD),
            TextNode(
                " ipsum dolor sit amet, consectetur adipiscing elit. Praesent. Neque porro quisquam est",
                TextType.TEXT,
            ),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_mulptiple_italic_split_join(self):
        node1 = TextNode(
            "Donec condimentum elit quis _purus_ faucibus, _viverra_ fringilla leo congue.",
            TextType.TEXT,
        )
        node2 = TextNode(
            "Aenean _vitae_ condimentum nisi. Aenean et est _libero_.", TextType.TEXT
        )

        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)

        expected_nodes = [
            TextNode("Donec condimentum elit quis ", TextType.TEXT),
            TextNode("purus", TextType.ITALIC),
            TextNode(" faucibus, ", TextType.TEXT),
            TextNode("viverra", TextType.ITALIC),
            TextNode(" fringilla leo congue.", TextType.TEXT),
            TextNode("Aenean ", TextType.TEXT),
            TextNode("vitae", TextType.ITALIC),
            TextNode(" condimentum nisi. Aenean et est ", TextType.TEXT),
            TextNode("libero", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_wrong_node_split_with_none(self):
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(None, "**", TextType.BOLD)

        self.assertEqual(str(context.exception), "Invalid or empty list of nodes")

    def test_wrong_node_split_with_empty_list(self):
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([], "_", TextType.ITALIC)

        self.assertEqual(str(context.exception), "Invalid or empty list of nodes")

    def test_non_closed_delimiter(self):
        node = TextNode("This is **bold text", TextType.TEXT)

        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.TEXT)

        self.assertEqual(
            str(context.exception), "Invalid markdown: delimiter was not closed"
        )

    def test_not_text_textype(self):
        node1 = TextNode("Lorem ipsum dominem", TextType.CODE)
        node2 = TextNode("Faruum `eptilum`", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)

        expected_nodes = [
            TextNode("Lorem ipsum dominem", TextType.CODE),
            TextNode("Faruum ", TextType.TEXT),
            TextNode("eptilum", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected_nodes)


class TestInlineMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_wrong_image(self):
        matches = extract_markdown_images(
            "This is text with wrong [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertEqual([("link", "https://example.com")], matches)

    def test_extract_wrong_link(self):
        matches = extract_markdown_links(
            "This is text with a wrong ![image](https://example.com/image.png)"
        )
        self.assertEqual([], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![image](https://example.com/cat.jpg) and ![another image](https://google.com/dog.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://example.com/cat.jpg"),
                ("another image", "https://google.com/dog.png"),
            ],
            matches,
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://google.com) and [another link](https://blog.example.com)"
        )
        self.assertListEqual(
            [
                ("link", "https://google.com"),
                ("another link", "https://blog.example.com"),
            ],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
