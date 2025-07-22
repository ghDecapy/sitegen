from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            node_text_split = node.text.split(delimiter)
            if len(node_text_split) % 2 != 1:
                raise SyntaxError("Syntax Error, text has unmatched markdown delimiter")
            for i in range(len(node_text_split)):
                if i % 2 != 0:
                    node_with_type = TextNode(node_text_split[i], text_type)
                    new_nodes.append(node_with_type)
                else:
                    node_without_type = TextNode(node_text_split[i], TextType.PLAIN_TEXT)
                    new_nodes.append(node_without_type)
    return new_nodes

