from blocks import markdown_to_html_node

import os
import shutil
import re

def main():
    copy_static("static")
    generate_page("content/index.md", "templates/template.html", "public/index.html")

PUBLIC="public"
NoHeadingError = Exception("no h1 found")

def copy_static(source: str) -> None:
    if not os.path.exists(source):
        raise Exception(f"path does not exist: {source}")
    
    if os.path.exists(PUBLIC):
        print(f"Remove: {PUBLIC}")
        shutil.rmtree(PUBLIC)


    copy_directory(source, PUBLIC)

def copy_directory(source: str, dest: str) -> None:
    if not os.path.exists(dest):
        print(f"Create: {dest}")
        os.mkdir(dest)

    for entry in os.listdir(source):
        source_path = os.path.join(source, entry)
        dest_path = os.path.join(dest, entry)
        print(f"Copy:   {os.path.join(source,entry)} -> {dest_path}")
        if os.path.isdir(source_path):
            sub = os.path.join(dest, os.path.basename(entry))
            copy_directory(source_path, sub)
        else:
            shutil.copy(source_path, dest_path)

def extract_title(md: str) -> str:
    h1_re = r"# (.*)"
    title = re.match(h1_re, md)

    if title is None:
        raise NoHeadingError

    return title[0]

def generate_page(source_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {source_path} to {dest_path} using {template_path}")

    f = open(source_path, 'r')
    source = f.read()
    f.close()

    f = open(template_path, 'r')
    template = f.read()
    f.close()

    nodes = markdown_to_html_node(source)
    # nodes.debug()
    html = nodes.to_html()
    title = extract_title(source)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)


    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, 'w') as f:
        f.write(template)

    
    return None

main()

