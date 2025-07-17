import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

atr_dict = {
    "href": "https://www.google.com",
    "target": "_blank",
}

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        hnode = HTMLNode("b","this would be bold text", None, atr_dict)
        self.assertEqual(hnode.props_to_html(),' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        hnode = HTMLNode("b","this would be bold text", None, atr_dict)
        self.assertEqual(hnode.__repr__(), f"HTMLNode({hnode.tag}, {hnode.value}, {hnode.children}, {hnode.props})")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_one_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_two_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("b","ello")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>ello</b></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_no_children(self):
        parent_node = ParentNode("h1", None)
        self.assertRaises(ValueError)

    def test_to_html_link_child(self):
        child_node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node2 = LeafNode("b","ello")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), '<div><a href="https://www.google.com">Click me!</a><b>ello</b></div>')

if __name__ == "__main__":
    unittest.main()