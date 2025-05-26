import unittest
from src.textnode import TextNode, TextType


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
        node = TextNode("One of the others text nodes", TextType.NORMAL)
        node2 = TextNode("One of another text nodes", TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
