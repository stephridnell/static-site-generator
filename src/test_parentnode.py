import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_init_with_tag_and_children(self):
        child = LeafNode("p", "Hello")
        node = ParentNode("div", [child])
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [child])
        self.assertIsNone(node.props)

    def test_init_with_props(self):
        props = {"class": "my-class"}
        child = LeafNode("p", "Hello")
        node = ParentNode("div", [child], props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, props)

    def test_to_html_basic(self):
        child = LeafNode("p", "Hello")
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_to_html_with_props(self):
        props = {"class": "my-class"}
        child = LeafNode("p", "Hello")
        node = ParentNode("div", [child], props)
        self.assertEqual(
            node.to_html(), "<div class=\"my-class\"><p>Hello</p></div>")

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "Hello")
        child2 = LeafNode("p", "World")
        node = ParentNode("div", [child1, child2])
        self.assertEqual(node.to_html(), "<div><p>Hello</p><p>World</p></div>")

    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        child = LeafNode("p", "Hello")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
