import os
from pathlib import Path
from inline_markdown import *
from markdown_blocks import *

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path)
    markdown_content = from_file.read()
    from_file.close()
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()
    html = markdown_to_html_node(markdown_content)
    html_file = html.to_html()
    title = extract_title(markdown_content)
    dest_file = template.replace("{{ Title }}", title).replace("{{ Content }}", html_file)
    dest_file = template.replace('href="/', 'href="' + basepath)
    dest_file = template.replace('src="/', 'src="' + basepath)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(dest_file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            sep = line.split(" ", 1)
            title = sep[1]
            return title
    raise Exception("Title not found")