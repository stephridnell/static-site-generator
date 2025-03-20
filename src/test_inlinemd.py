import unittest

from inlinemd import (extract_markdown_images, extract_markdown_links,
                      split_nodes_delimiter, split_nodes_image,
                      split_nodes_link, text_to_text_nodes)
from textnode import TextNode, TextType


class TestUtil(unittest.TestCase):
    def test_split_nodes_delimiter_text(self):
        node = TextNode("Hello **world**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD)
        ])

    def test_split_nodes_delimiter_empty_sections(self):
        node = TextNode("Hello ****world", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD)
        ])

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("Hello **world**", TextType.TEXT)
        node2 = TextNode("Another **text**", TextType.TEXT)
        nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("Another ", TextType.TEXT),
            TextNode("text", TextType.BOLD)
        ])

    def test_split_nodes_delimiter_non_text_node(self):
        node = TextNode("Hello world", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(nodes, [
            TextNode("Hello world", TextType.BOLD)
        ])

    def test_split_nodes_delimiter_unclosed_delimiter(self):
        node = TextNode("Hello **world", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("Hello *italic* text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_code(self):
        node = TextNode("Hello `code` text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_empty_sections(self):
        node = TextNode("**bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(nodes, [
            TextNode("bold", TextType.BOLD)
        ])

    def test_split_nodes_delimiter_multiple_empty_sections(self):
        node = TextNode("**bold****more**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(nodes, [
            TextNode("bold", TextType.BOLD),
            TextNode("more", TextType.BOLD)
        ])

    def test_split_nodes_delimiter_empty_input(self):
        nodes = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 0)

    def test_split_nodes_delimiter_empty_text(self):
        node = TextNode("", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 0)

    def test_split_nodes_delimiter_multiple_delimiters_in_text(self):
        node = TextNode("***italic and bold***", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "***", TextType.BOLD)
        self.assertListEqual(nodes, [
            TextNode("italic and bold", TextType.BOLD)
        ])

    def test_extract_markdown_links_single(self):
        text = "This is a [link](https://www.boot.dev) in text"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [
            ("link", "https://www.boot.dev")
        ])

    def test_extract_markdown_links_multiple(self):
        text = "[link1](url1) and [link2](url2)"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [
            ("link1", "url1"),
            ("link2", "url2")
        ])

    def test_extract_markdown_links_none(self):
        text = "This text has no links"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    def test_extract_markdown_links_with_image(self):
        text = "![image](img.jpg) and [link](url)"
        links = extract_markdown_links(text)
        self.assertListEqual(links, [
            ("link", "url")
        ])

    def test_extract_markdown_images_single(self):
        text = "This is an ![image](https://i.imgur.com/zjjcJKZ.png) in text"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ])

    def test_extract_markdown_images_multiple(self):
        text = "![img1](url1.jpg) and ![img2](url2.png)"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [
            ("img1", "url1.jpg"),
            ("img2", "url2.png")
        ])

    def test_extract_markdown_images_none(self):
        text = "This text has no images"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)

    def test_extract_markdown_images_with_link(self):
        text = "[link](url) and ![image](img.jpg)"
        images = extract_markdown_images(text)
        self.assertListEqual(images, [
            ("image", "img.jpg")
        ])

    def test_split_nodes_image_single(self):
        node = TextNode(
            "This is an ![image](https://example.com/img.jpg) in text", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertListEqual(nodes, [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" in text", TextType.TEXT)
        ])

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "![img1](url1.jpg) and ![img2](url2.jpg)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertListEqual(nodes, [
            TextNode("img1", TextType.IMAGE, "url1.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2.jpg")
        ])

    def test_split_nodes_image_non_text_node(self):
        node = TextNode("![img](url.jpg)", TextType.BOLD)
        nodes = split_nodes_image([node])
        self.assertListEqual(nodes, [
            TextNode("![img](url.jpg)", TextType.BOLD)
        ])

    def test_split_nodes_link_single(self):
        node = TextNode(
            "This is a [link](https://example.com) in text", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertListEqual(nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in text", TextType.TEXT)
        ])

    def test_split_nodes_link_multiple(self):
        node = TextNode("[link1](url1) and [link2](url2)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertListEqual(nodes, [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2")
        ])

    def test_split_nodes_link_non_text_node(self):
        node = TextNode("[link](url)", TextType.BOLD)
        nodes = split_nodes_link([node])
        self.assertListEqual(nodes, [
            TextNode("[link](url)", TextType.BOLD)
        ])

    def test_text_to_text_nodes_simple(self):
        text = "Hello world"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(nodes, [
            TextNode("Hello world", TextType.TEXT)
        ])

    def test_text_to_text_nodes_bold(self):
        text = "Hello **world**"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD)
        ])

    def test_text_to_text_nodes_italic(self):
        text = "Hello _world_"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.ITALIC)
        ])

    def test_text_to_text_nodes_code(self):
        text = "Hello `world`"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.CODE)
        ])

    def test_text_to_text_nodes_link(self):
        text = "Hello [world](https://example.com)"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.LINK, "https://example.com")
        ])

    def test_text_to_text_nodes_image(self):
        text = "Hello ![world](image.jpg)"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.IMAGE, "image.jpg")
        ])

    def test_text_to_text_nodes_mixed(self):
        text = "This is **bold** and _italic_ with `code` and a [link](url) and ![image](img.jpg)"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.jpg")
        ])


if __name__ == "__main__":
    unittest.main()
