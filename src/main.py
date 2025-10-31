from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
import os
import shutil

def clean_public():
    if(os.path.exists('public/')):
        shutil.rmtree('public')
        os.mkdir('public')

def copy_static(path=""):
    full_path = "static/"
    if(path != ""):
        full_path += path
    files = os.listdir(full_path)
    for file in files:
        full_file_path = full_path + file
        dest_full_path = full_path.replace("static", "public")
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

def main():
    clean_public()
    copy_static()

main()