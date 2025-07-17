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

if __name__ == "__main__":
    unittest.main()