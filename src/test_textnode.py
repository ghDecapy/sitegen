import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("Italic Text Node", TextType.ITALIC_TEXT)
        node2 = TextNode("URL This time", TextType.LINK,"https://google.com")
        self.assertNotEqual(node, node2)

    def test_url_opt(self):
        node = TextNode("URL", TextType.LINK, None)
        node2 = TextNode("URL", TextType.LINK)
        self.assertEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_link(self):
        node = TextNode("Link goes heres", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link goes heres")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
                         

if __name__ == "__main__":
    unittest.main()