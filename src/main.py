from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
import os
import shutil
import sys
from helpers import *

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if(not os.path.exists(from_path)):
        raise Exception(f"input markdown file does not exist: {from_path}")
    if(not os.path.exists(from_path)):
        raise Exception(f"template file does not exist: {template_path}")
    from_path_file = ""
    template_path_file = ""
    with open(from_path, "r", encoding="utf-8") as f:
        from_path_file = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_path_file = f.read()
    title = extract_title(from_path_file)
    from_path_html = markdown_to_html_node(from_path_file).to_html()
    template_path_file = template_path_file.replace("{{ Title }}", title)
    template_path_file = template_path_file.replace("{{ Content }}", from_path_html)
    href_replace = 'href="' + base_path
    src_replace = 'src="' + base_path
    template_path_file = template_path_file.replace('href="/', href_replace)
    template_path_file = template_path_file.replace('src="/', src_replace)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_path_file)
    return

def generage_pages_recursive(dir_path_content, template_path, base_path):
    full_path = ""
    if(dir_path_content == ""):
        full_path = "content/"
    else:
        full_path += dir_path_content
    files = os.listdir(full_path)
    print(f"found files: {files} in {full_path}")
    for file in files:
        full_file_path = full_path + file
        dest_full_path = full_path.replace("content", "docs")
        dest_full_file_path = dest_full_path + file
        if(os.path.isfile(full_path + file)):
            print(f"found file: {file}")
            if(os.path.exists(dest_full_path)):
                print(f"directory: {dest_full_path} already exists")
            else:
                print(f"directory: {dest_full_path} does not exist, creating it")
                os.mkdir(dest_full_path)
            dest_full_file_path = dest_full_file_path.replace(".md", ".html")
            print(f"running command: generate_page({full_file_path}, {template_path}, {dest_full_file_path}, {base_path})")
            generate_page(full_file_path, template_path, dest_full_file_path, base_path)
        else:
            print(f"found dir: {file}")
            if(os.path.exists(dest_full_path)):
                print(f"directory: {dest_full_path} already exists")
            else:
                print(f"directory: {dest_full_path} does not exist, creating it")
                os.mkdir(dest_full_path)
            print(f"running command: generage_pages_recursive({full_path + file + "/"}, {template_path}, {base_path})")
            generage_pages_recursive(full_path + file + "/", template_path, base_path)
    return

def clean_public():
    if(os.path.exists('docs/')):
        shutil.rmtree('docs')
        os.mkdir('docs')
    else:
        os.mkdir('docs')
    return

def copy_static(path=""):
    full_path = "static/"
    if(path != ""):
        full_path += path
    files = os.listdir(full_path)
    for file in files:
        full_file_path = full_path + file
        dest_full_path = full_path.replace("static", "docs")
        dest_full_file_path = dest_full_path + file
        if(os.path.isfile(full_path + file)):
            print(f"found file: {file}")
            if(os.path.exists(dest_full_path)):
                print(f"directory: {dest_full_path} already exists")
            else:
                print(f"directory: {dest_full_path} does not exist, creating it")
                os.mkdir(dest_full_path)
            print(f"running command: shutil.copy({full_file_path}, {dest_full_file_path})")
            shutil.copy(full_file_path, dest_full_file_path)
        else:
            print(f"found dir: {file}")
            copy_static(file + "/")
    return

def main():
    base_path = "/"
    if(len(sys.argv) > 1):
        base_path = sys.argv[1]
    clean_public()
    copy_static()
    generage_pages_recursive("", "template.html", base_path)

main()