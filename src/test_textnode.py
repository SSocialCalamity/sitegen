import unittest

from textnode import TextNode, TextType
from helpers import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_neq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://localhost:8888")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_neq3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text_helper(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text_to_html_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://localhost:8888/img")
        html_node = node.to_html_node().to_html()
        self.assertEqual(html_node, '<a href="http://localhost:8888/img">This is a link</a>')
    def test_text_to_html_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://localhost:8888/img")
        html_node = node.to_html_node().to_html()
        self.assertEqual(html_node, '<img src="http://localhost:8888/img" alt="This is an image"></img>')
    def test_text_to_html_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = node.to_html_node().to_html()
        self.assertEqual(html_node, '<code>This is code</code>')
    def test_split_node1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_node1 = TextNode("This is text with a ", TextType.TEXT)
        new_node2 = TextNode("code block", TextType.CODE)
        new_node3 = TextNode(" word", TextType.TEXT)
        self.assertEqual(new_nodes, [new_node1, new_node2, new_node3])
    def test_split_node2(self):
        node = TextNode("This is text with **bold words** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_node1 = TextNode("This is text with ", TextType.TEXT)
        new_node2 = TextNode("bold words", TextType.BOLD)
        new_node3 = TextNode(" in it", TextType.TEXT)
        self.assertEqual(new_nodes, [new_node1, new_node2, new_node3])
    def test_split_node3(self):
        node = TextNode("This is text with _italic words_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_node1 = TextNode("This is text with ", TextType.TEXT)
        new_node2 = TextNode("italic words", TextType.ITALIC)
        new_node3 = TextNode(" in it", TextType.TEXT)
        self.assertEqual(new_nodes, [new_node1, new_node2, new_node3])
    def test_split_node4(self):
        node = TextNode("_italic words_ at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_node1 = TextNode("italic words", TextType.ITALIC)
        new_node2 = TextNode(" at the start", TextType.TEXT)
        self.assertEqual(new_nodes, [new_node1, new_node2])
    def test_split_node_unmatched(self):
        with self.assertRaises(Exception):
            node = TextNode("This is text with _italic words in it", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
            new_node1 = TextNode("This is text with ", TextType.TEXT)
            new_node2 = TextNode("italic words", TextType.ITALIC)
            new_node3 = TextNode(" in it", TextType.TEXT)
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://localhost/image.png)"
        )
        self.assertListEqual([("image", "https://localhost/image.png")], matches)
    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://localhost/image.png) and another image ![image](https://images.localhost/image2.png)"
        )
        self.assertListEqual([("image", "https://localhost/image.png"), ("image", "https://images.localhost/image2.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [new link](https://localhost/)"
        )
        self.assertListEqual([("new link", "https://localhost/")], matches)
    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "This is text with an [new link](https://localhost/) and another link [new other link](https://localhost/squanch)"
        )
        self.assertListEqual([("new link", "https://localhost/"), ("new other link", "https://localhost/squanch")], matches)

if __name__ == "__main__":
    unittest.main()