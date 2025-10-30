import re
from textnode import TextNode, TextType
from leafnode import LeafNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if(node.text_type == TextType.TEXT):
            split_text = node.text.split(delimiter)
            if(len(split_text) % 2 == 0):
                raise Exception("unmatched delimeters found, invalid node text")
            count = 0
            if(list(node.text)[0] == list(delimiter)[0]):
                count += 1
            for segment in split_text:
                if(len(segment) > 0):
                    if(count == 1):
                        new_nodes.append(TextNode(segment, text_type))
                        count -= 1
                    else:
                        new_nodes.append(TextNode(segment, TextType.TEXT))
                        count += 1
        else:
            new_nodes.append(node)
    return(new_nodes)

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.TEXT:
            node = LeafNode(None, text_node.text)
            return(node)
        case TextType.BOLD:
            node = LeafNode("b", text_node.text)
            return(node)
        case TextType.ITALIC:
            node = LeafNode("i", text_node.text)
            return(node)
        case TextType.CODE:
            node = LeafNode("code", text_node.text)
            return(node)
        case TextType.LINK:
            node = LeafNode("a", text_node.text, {"href": text_node.url})
            return(node)
        case TextType.IMAGE:
            node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return(node)
        case _:
            raise Exception(f"Not a valid TextType: {text_node.text_type}")

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return(matches)

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return(matches)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if(node.text_type != TextType.TEXT):
            new_nodes.append(node)
        else:
            markdown_images = extract_markdown_images(node.text)
            if(len(markdown_images) < 1):
                new_nodes.append(node)
                continue
            tmp_node_text = node.text
            for image in markdown_images:
                split_str = f"![{image[0]}]({image[1]})"
                sections = tmp_node_text.split(split_str, 1)
                if(len(list(sections[0])) > 0):
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                tmp_node_text = sections[1]
                if(len(extract_markdown_images(tmp_node_text)) < 1 and len(list(tmp_node_text)) > 0):
                    new_nodes.append(TextNode(tmp_node_text, TextType.TEXT))
    return(new_nodes)

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if(node.text_type != TextType.TEXT):
            new_nodes.append(node)
        else:
            markdown_links = extract_markdown_links(node.text)
            if(len(markdown_links) < 1):
                new_nodes.append(node)
                continue
            tmp_node_text = node.text
            for image in markdown_links:
                split_str = f"[{image[0]}]({image[1]})"
                sections = tmp_node_text.split(split_str, 1)
                if(len(list(sections[0])) > 0):
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.LINK, image[1]))
                tmp_node_text = sections[1]
                if(len(extract_markdown_links(tmp_node_text)) < 1 and len(list(tmp_node_text)) > 0):
                    new_nodes.append(TextNode(tmp_node_text, TextType.TEXT))
    return(new_nodes)

def text_to_textnodes(text):
    orig_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([orig_node], "_", TextType.ITALIC),
                    "**",
                    TextType.BOLD),
                "`",
                TextType.CODE)
        )
    )
    return(new_nodes)