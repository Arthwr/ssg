import unittest

from markdown.textnode import TextNode, TextType
from markdown.inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_title,
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

        self.assertListEqual(new_nodes, expected_nodes)

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

        self.assertListEqual(new_nodes, expected_nodes)

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

        self.assertListEqual(new_nodes, expected_nodes)

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

        self.assertListEqual(new_nodes, expected_nodes)


class TestInlineMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_wrong_image(self):
        matches = extract_markdown_images(
            "This is text with wrong [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_wrong_link(self):
        matches = extract_markdown_links(
            "This is text with a wrong ![image](https://example.com/image.png)"
        )
        self.assertListEqual([], matches)

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

    def test_extract_title(self):
        markdown = "# Hello World"
        title = extract_title(markdown)

        self.assertEqual(title, "Hello World")

    def test_extract_title_from_bottom(self):
        markdown = "### Hello World\n ## Hi\n# Once upon a time"
        title = extract_title(markdown)

        self.assertEqual(title, "Once upon a time")

    def test_no_title_provided(self):
        markdown = "Some paragraph text\n also another one\n ## while no title provided"
        
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        
        self.assertEqual(str(context.exception), "No h1 title has been provided")

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_image_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_nodes(self):
        node = TextNode(
            "This is text with an awesome [google link](http://google.com) and another [example link](https://example.com), and some other funny text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an awesome ", TextType.TEXT),
                TextNode("google link", TextType.LINK, "http://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("example link", TextType.LINK, "https://example.com"),
                TextNode(", and some other funny text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_media_nodes(self):
        node1 = TextNode(
            "Here is an ![image](https://example.com/img1.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "Another ![pic](https://example.com/img2.png) follows here.", TextType.TEXT
        )

        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img1.png"),
                TextNode("Another ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://example.com/img2.png"),
                TextNode(" follows here.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_with_image_link(self):
        node = TextNode(
            "This is text with an example of ![image](https://example/image.png) we are parsing, but there is also an [about_link](https://example.com/about)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an example of ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example/image.png"),
                TextNode(
                    " we are parsing, but there is also an [about_link](https://example.com/about)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_with_repeated_images(self):
        node = TextNode(
            "This is an example of ![same picture](https://example.com/cat.png) and again ![same picture](https://example.com/cat.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an example of ", TextType.TEXT),
                TextNode("same picture", TextType.IMAGE, "https://example.com/cat.png"),
                TextNode(" and again ", TextType.TEXT),
                TextNode("same picture", TextType.IMAGE, "https://example.com/cat.png"),
            ],
            new_nodes,
        )

    def test_unclosed_markdown_link(self):
        node = TextNode(
            "This is an example of not closed markdown [picture](https://example.com/picture.jpg and some text on top of it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes(self):
        node_split = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )

        expected_split = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(node_split, expected_split)

    def test_text_to_textnodes_multiple_formats(self):
        node_split = text_to_textnodes(
            "**Bold** then _italic_, followed by `code`, then an image ![cat](https://example.com/cat.jpg), "
            "and a link [Google](https://google.com). More **bold _not italic_** and final `code`."
        )

        expected_split = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", followed by ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", then an image ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.jpg"),
            TextNode(", and a link ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(". More ", TextType.TEXT),
            TextNode("bold _not italic_", TextType.BOLD),
            TextNode(" and final ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]

        self.assertListEqual(node_split, expected_split)


if __name__ == "__main__":
    unittest.main()
