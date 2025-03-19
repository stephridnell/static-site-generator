import unittest

from textnode import TextNode, TextType
from util import (extract_markdown_images, extract_markdown_links,
                  split_nodes_delimiter)


class TestUtil(unittest.TestCase):
    def test_split_nodes_delimiter_text(self):
        node = TextNode("Hello **world**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_empty_sections(self):
        node = TextNode("Hello ****world", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("Hello **world**", TextType.TEXT)
        node2 = TextNode("Another **text**", TextType.TEXT)
        nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, "Another ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "text")
        self.assertEqual(nodes[3].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_non_text_node(self):
        node = TextNode("Hello world", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Hello world")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_unclosed_delimiter(self):
        node = TextNode("Hello **world", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("Hello *italic* text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("Hello `code` text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_empty_sections(self):
        node = TextNode("**bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "bold")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_multiple_empty_sections(self):
        node = TextNode("**bold****more**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "bold")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].text, "more")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

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
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "italic and bold")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_extract_markdown_links_single(self):
        text = "This is a [link](https://www.boot.dev) in text"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link", "https://www.boot.dev"))

    def test_extract_markdown_links_multiple(self):
        text = "[link1](url1) and [link2](url2)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("link1", "url1"))
        self.assertEqual(links[1], ("link2", "url2"))

    def test_extract_markdown_links_none(self):
        text = "This text has no links"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    def test_extract_markdown_links_with_image(self):
        text = "![image](img.jpg) and [link](url)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link", "url"))

    def test_extract_markdown_images_single(self):
        text = "This is an ![image](https://i.imgur.com/zjjcJKZ.png) in text"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(
            images[0], ("image", "https://i.imgur.com/zjjcJKZ.png"))

    def test_extract_markdown_images_multiple(self):
        text = "![img1](url1.jpg) and ![img2](url2.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("img1", "url1.jpg"))
        self.assertEqual(images[1], ("img2", "url2.png"))

    def test_extract_markdown_images_none(self):
        text = "This text has no images"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)

    def test_extract_markdown_images_with_link(self):
        text = "[link](url) and ![image](img.jpg)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("image", "img.jpg"))


if __name__ == "__main__":
    unittest.main()
