import unittest

from src.textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode(
            "This is a text node with link", TextType.LINK, "https://example.com"
        )
        node2 = TextNode(
            "This is a text node with link", TextType.LINK, "https://example.com"
        )
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("One of the others text nodes", TextType.TEXT)
        node2 = TextNode("One of another text nodes", TextType.ITALIC)
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://example.com", "alt": "This is an image"}
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


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


if __name__ == "__main__":
    unittest.main()
