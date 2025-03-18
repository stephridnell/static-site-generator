import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init_with_tag_and_value(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.props)

    def test_init_with_props(self):
        props = {"class": "my-class"}
        node = LeafNode("p", "Hello", props)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, props)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html_with_tag(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_to_html_with_props(self):
        props = {"class": "my-class"}
        node = LeafNode("p", "Hello", props)
        self.assertEqual(node.to_html(), "<p class=\"my-class\">Hello</p>")

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
