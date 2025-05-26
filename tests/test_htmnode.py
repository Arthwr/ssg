import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_node_repr(self):
        node_repr = HTMLNode(
            "p", "hello world", None, {"class": "paragraph"}
        ).__repr__()
        node_str = "HTMLNode(p, hello world, None, {'class': 'paragraph'})"
        self.assertEqual(node_repr, node_str)

    def test_node_props_to_html(self):
        node = HTMLNode(
            "a",
            "example link",
            None,
            {"href": "https://example.com", "target": "_blank"},
        )
        html_str = ' href="https://example.com" target="_blank"'

        self.assertEqual(node.props_to_html(), html_str)

    def test_node_none_props(self):
        node = HTMLNode("span", "lorem ipsum", None, None)
        html_str = ""

        self.assertEqual(node.props_to_html(), html_str)

    def test_node_empty_props(self):
        node = HTMLNode("h1", "dorem ipsulum", None, {})
        html_str = ""

        self.assertEqual(node.props_to_html(), html_str)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_params(self):
        node = LeafNode("a", "my website", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">my website</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("b", None, {"class": "text-semibold"})
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no value")

    def test_parentnode_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parentnode_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_parentnode_to_html_with_multiple_children(self):
        grandchild_node1 = LeafNode("li", "list one of node1")
        grandchild_node2 = LeafNode("li", "list two of node1")
        grandchild_node3 = LeafNode("li", "list one of node2")
        grandchild_node4 = LeafNode("li", "list two of node2")
        parent_node1 = ParentNode("ul", [grandchild_node1, grandchild_node2])
        parent_node2 = ParentNode("ul", [grandchild_node3, grandchild_node4])
        grandparent_node = ParentNode("section", [parent_node1, parent_node2])
        self.assertEqual(
            grandparent_node.to_html(),
            "<section>"
            "<ul><li>list one of node1</li><li>list two of node1</li></ul>"
            "<ul><li>list one of node2</li><li>list two of node2</li></ul>"
            "</section>",
        )

    def test_parentnode_to_html_with_children_props(self):
        grandchild_node1 = LeafNode("a", "about", {"href": "https://example.com/about"})
        grandchild_node2 = LeafNode(
            "a", "works", {"href": "https://example.com/work", "class": "active-link"}
        )
        parent_node = ParentNode(
            "div",
            [grandchild_node1, grandchild_node2],
            {"class": "flex flex-col gap-2"},
        )
        grandparent_node = ParentNode("main", [parent_node])
        self.assertEqual(
            grandparent_node.to_html(),
            "<main>"
            '<div class="flex flex-col gap-2">'
            '<a href="https://example.com/about">about</a>'
            '<a href="https://example.com/work" class="active-link">works</a>'
            "</div>"
            "</main>",
        )

    def test_parentnode_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "Invaild HMTL: no children passed")


if __name__ == "__main__":
    unittest.main()
