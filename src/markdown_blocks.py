from enum import Enum
from textnode import *
from htmlnode import *
from inline_markdown import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    final_blocks = []
    split_blocks = markdown.split("\n\n")
    for block in split_blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            final_blocks.append(stripped_block)
    return final_blocks

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        block_list = block.splitlines()
        for i in range (0, len(block_list)):
            if not block_list[i].startswith(">"):
                raise Exception("Syntax Error. Not every line of this Quote Block starts with '>'")
        return BlockType.QUOTE
    elif block.startswith("- "):
        block_list = block.splitlines()
        for i in range (0, len(block_list)):
            if not block_list[i].startswith("- "):
                raise Exception("Syntax Error. Not every line of this Unordered List Block starts with '- '")
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        block_list = block.splitlines()
        for i in range(1, len(block_list)):
            if not block_list[i].startswith(f"{i+1}. "):
                raise Exception("Syntax Error. Ordered list increment or prefix syntax incorrect")
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        child_nodes.append(html_node)
    return ParentNode("div", child_nodes)

def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    raise ValueError("Block Type not supported")

def paragraph_to_html_node(block):
    lines = block.splitlines()
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    split = block.split(" ", maxsplit=1)
    level = split[0].count("#")
    children = text_to_children(block[level+1:])
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    text = block.lstrip("```\n").rstrip("```")
    text_node = TextNode(text, TextType.PLAIN_TEXT)
    child_node = text_node_to_html_node(text_node)
    code = ParentNode("code", [child_node])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    new_lines = []
    lines = block.splitlines()
    for line in lines:
        new_lines.append(line.removeprefix(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def olist_to_html_node(block):
    lines = block.splitlines()
    html_items = []
    for line in lines:
        text = line[3:]
        node = text_to_children(text)
        html_items.append(ParentNode("li", node))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    lines = block.splitlines()
    html_items = []
    for line in lines:
        raw_text = line[2:]
        node = text_to_children(raw_text)
        html_items.append(ParentNode("li", node))
    return ParentNode("ul", html_items)