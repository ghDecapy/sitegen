from textnode import *
from htmlnode import *
import re

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

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!\!)\[(.*?)]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        extracted_images = extract_markdown_images(node.text)
        if len(extracted_images) == 0:
            new_nodes.append(node)
        else:
            for i in range(0, len(extracted_images)):
                image_alt, image_link = extracted_images[i]
                sections = original_text.split(f"![{image_alt}]({image_link})", 1)
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if i == len(extracted_images) - 1 and sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.PLAIN_TEXT))
                original_text = sections[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        extracted_links = extract_markdown_links(node.text)
        if len(extracted_links) == 0:
            new_nodes.append(node)
        else:
            for i in range(0, len(extracted_links)):
                link_text, link = extracted_links[i]
                sections = original_text.split(f"[{link_text}]({link})", 1)
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link))
                if i == len(extracted_links) - 1 and sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.PLAIN_TEXT))
                original_text = sections[1]
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

print(text_to_textnodes(text))