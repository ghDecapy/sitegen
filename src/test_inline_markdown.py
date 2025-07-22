import unittest

from textnode import *
from htmlnode import *
from inline_markdown import *

class TestSplitNode(unittest.TestCase):
    def test_split_code_delim_one(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes[1].text, "code block")

    def test_split_code_delim_two(self):
        node = TextNode("Hey this is `one` delimiter and this is `two` hehe", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[3].text, "two")

    def test_split_bold_delim(self):
        node = TextNode("This is **text** with some **bold** words **here** and an ignored _italic_", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[3].text, "bold")
