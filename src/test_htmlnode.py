import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_init_empty(self):
        node = HtmlNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_tag(self):
        node = HtmlNode("p")
        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_value(self):
        node = HtmlNode(value="Hello")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_children(self):
        child = HtmlNode("p", "child")
        node = HtmlNode("div", children=[child])
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [child])
        self.assertIsNone(node.props)

    def test_init_with_props(self):
        props = {"class": "my-class", "id": "my-id"}
        node = HtmlNode("div", props=props)
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, props)

    def test_props_to_html_none(self):
        node = HtmlNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        props = {"class": "my-class", "id": "my-id"}
        node = HtmlNode(props=props)
        self.assertEqual(node.props_to_html(),
                         " class=\"my-class\" id=\"my-id\"")

    def test_to_html_not_implemented(self):
        node = HtmlNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        props = {"class": "my-class"}
        child = HtmlNode("p", "child")
        node = HtmlNode("div", "parent", [child], props)
        self.assertEqual(repr(
            node), "HtmlNode(div, parent, [HtmlNode(p, child, None, None)], {'class': 'my-class'})")


if __name__ == "__main__":
    unittest.main()
