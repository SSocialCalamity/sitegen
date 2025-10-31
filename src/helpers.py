import re
from textnode import TextNode, TextType
from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from blocktype import BlockType

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

def markdown_to_blocks(markdown):
    blocks = []
    markdown_split = markdown.split("\n\n")
    for block in markdown_split:
        block = block.strip()
        if(len(list(block)) == 0):
            continue
        blocks.append(block)
    return(blocks)

def block_to_block_type(markdown):
    if(re.match(r"^#{1,6}\s.*", markdown)):
        return(BlockType.HEADING)
    elif(re.match(r"```(.*)```", markdown, re.DOTALL | re.MULTILINE)):
        return(BlockType.CODE)
    quote = 1
    unordered = 1
    ordered = 1
    ordered_count = 1
    for line in markdown.split("\n"):
        if(list(line)[0] != '>'):
            quote = 0
        if(not (list(line)[0] == '-' and list(line)[1] == ' ')):
            unordered = 0
        if(re.match(r"^[0-9]", line)):
            if(not (int(list(line)[0]) == ordered_count and list(line)[1] == "." and list(line)[2] == " ")):
                ordered = 0
        else:
            ordered = 0
        ordered_count += 1
    if(quote == 1):
        return(BlockType.QUOTE)
    if(unordered == 1):
        return(BlockType.UNORDERED_LIST)
    if(ordered == 1):
        return(BlockType.ORDERED_LIST)
    return(BlockType.PARAGRAPH)

def text_to_children(markdown_block, markdown_type):
    children = []
    match(markdown_type):
        case(BlockType.PARAGRAPH | BlockType.HEADING | BlockType.CODE):
            for text_node in text_to_textnodes(markdown_block):
                children.append(text_node_to_html_node(text_node))
        case BlockType.QUOTE:
            count = 1
            for line in markdown_block.split("\n"):
                res = re.search(r">\s?(.*)", line)
                if(len(markdown_block.split("\n")) == count):
                    for text_node in text_to_textnodes(res.group(1)):
                        children.append(text_node_to_html_node(text_node))
                else:
                    for text_node in text_to_textnodes(res.group(1) + "\n"):
                        children.append(text_node_to_html_node(text_node))
                count += 1
        case BlockType.ORDERED_LIST:
            for line in markdown_block.split("\n"):
                res = re.search(r"\d+\.\s(.*)", line)
                tmp_children = []
                for text_node in text_to_textnodes(res.group(1)):
                    tmp_children.append(text_node_to_html_node(text_node))
                tmp_parent = ParentNode("li", tmp_children)
                children.append(tmp_parent)
        case BlockType.UNORDERED_LIST:
            for line in markdown_block.split("\n"):
                res = re.search(r"\-\s(.*)", line)
                tmp_children = []
                for text_node in text_to_textnodes(res.group(1)):
                    tmp_children.append(text_node_to_html_node(text_node))
                tmp_parent = ParentNode("li", tmp_children)
                children.append(tmp_parent)
        case _:
            for text_node in text_to_textnodes(markdown_block):
                children.append(text_node_to_html_node(text_node))
    return(children)

def markdown_block_to_html(markdown_block, markdown_type):
    node = None
    match(markdown_type):
        case BlockType.PARAGRAPH:
            #example on boot dev shows block lines being substituted with spaces instead in paragraphs
            markdown_block = markdown_block.replace("\n", " ")
            children = text_to_children(markdown_block, markdown_type)
            node = ParentNode("p", children)
        case BlockType.HEADING:
            heading = "h1"
            res = re.search(r"(#{1,6})\s(.*)", markdown_block, re.DOTALL | re.MULTILINE)
            match(res.group(1)):
                case "#":
                    heading = "h1"
                case "##":
                    heading = "h2"
                case "###":
                    heading = "h3"
                case "####":
                    heading = "h4"
                case "#####":
                    heading = "h5"
                case "######":
                    heading = "h6"
                case _:
                    heading = "h1"
            children = text_to_children(res.group(2), markdown_type)
            node = ParentNode(heading, children)
        case BlockType.CODE:
            res = re.search(r"```\n?(.*)\n?```", markdown_block, re.DOTALL | re.MULTILINE)
            children = [LeafNode("code", res.group(1))]
            node = ParentNode("pre", children)
        case BlockType.QUOTE:
            children = text_to_children(markdown_block, markdown_type)
            node = ParentNode("blockquote", children)
        case BlockType.ORDERED_LIST:
            children = text_to_children(markdown_block, markdown_type)
            node = ParentNode("ol", children)
        case BlockType.UNORDERED_LIST:
            children = text_to_children(markdown_block, markdown_type)
            node = ParentNode("ul", children)
        case _:
            children = text_to_children(markdown_block, markdown_type)
            node = ParentNode("p", markdown_block)
    return(node)

def markdown_to_html_node(markdown):
    children = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        markdown_type = block_to_block_type(block)
        block_html_node = markdown_block_to_html(block, markdown_type)
        children.append(block_html_node)
    parent_node = ParentNode('div', children)
    return(parent_node)