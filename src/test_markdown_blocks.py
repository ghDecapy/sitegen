import unittest

from markdown_blocks import *

class TestMarkdowntoBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_two(self):
        md = """
This is a heading with trailing empty space     




This is a paragraph of text. It has some **bold** and _italic_ words inside of it.


   - This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a heading with trailing empty space",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ]
        )

class TestBlocktoBlockType(unittest.TestCase):
    def test_heading(self):
        heading = "# Ello there"
        heading_two = "## Yeehaw"
        heading_three = "###### Easy"
        not_heading = "#Awno"
        self.assertListEqual([block_to_block_type(heading), block_to_block_type(heading_two), block_to_block_type(heading_three)], [BlockType.HEADING, BlockType.HEADING, BlockType.HEADING])
        self.assertEqual(block_to_block_type(not_heading), BlockType.PARAGRAPH)

    def test_code(self):
        code = "``` hackermans ```"
        not_code = "``` not hackermans"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        self.assertEqual(block_to_block_type(not_code), BlockType.PARAGRAPH)

    def test_quote(self):
        quote_block =""">There once was a man
>He lived
>and died"""
        not_quote_block = """>There once was a man
He lived
>and died"""
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
        self.assertRaises(Exception)

    def test_ordered(self):
        ordered_block = """1. Hehe here is some text
2. I am testing something good
3. This is interesting to me
4. I wonder if this will work"""
        self.assertEqual(block_to_block_type(ordered_block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
