import unittest

from textnode import TextNode, TextType
from blocktype import BlockType
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
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_start_with_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_single_image(self):
        node = TextNode(
            "single image ![image](https://i.imgur.com/zjjcJKZ.png) that is the only image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("single image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" that is the only image", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )
    def test_split_links_start_with_link(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and another [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )
    def test_split_links_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and stuff after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and stuff after", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
    def test_text_to_textnodes2(self):
        text = '**bold text** with an _italic things_ word and a `" code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and more stuff'
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic things", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode('" code block', TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and more stuff", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnodes3(self):
        text = '![image 1](https://i.localhost/squanch.png)**bold text** with an _italic things_[link0](hey a link) word and a `" code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("image 1", TextType.IMAGE, "https://i.localhost/squanch.png"),
                TextNode("bold text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic things", TextType.ITALIC),
                TextNode("link0", TextType.LINK, "hey a link"),
                TextNode(" word and a ", TextType.TEXT),
                TextNode('" code block', TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

#heading on the bottom
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "#heading on the bottom",
            ],
        )
    def test_markdown_to_blocks3(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

#heading on the bottom





"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "#heading on the bottom",
            ],
        )
    def test_block_to_block_type(self):
        md = """###### heading"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
    def test_block_to_block_type2(self):
        md = """## heading"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
    def test_block_to_block_type3(self):
        md = """####### heading"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_block_to_block_type4(self):
        md = """### ##heading"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
    def test_block_to_block_type5(self):
        md = """```code block```"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)
    def test_block_to_block_type6(self):
        md = """``code block```"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_block_to_block_type7(self):
        md = """```code block``"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_block_to_block_type8(self):
        md = """````code block```"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)
    def test_block_to_block_type9(self):
        md = """>quote
>quote 2
> quote 3"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)
    def test_block_to_block_type10(self):
        md = """>quote
quote 2
> quote 3"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_block_to_block_type11(self):
        md = """>>quote
>quote 2
>>>" quote 3"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)
    def test_block_to_block_type12(self):
        md = """- unorder
- unorder 2
- unorder 3"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    def test_block_to_block_type13(self):
        md = """- unorder
-unorder 2
- unorder 3"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_block_to_block_type14(self):
        md = """1. ordered
2. ordered 2
3. ordered 3"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    def test_block_to_block_type15(self):
        md = """1. ordered
3. ordered 2
2. ordered 3"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_block_to_block_type16(self):
        md = """1. ordered
2. ordered 2
3.ordered 3"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_block_to_block_type17(self):
        md = """1. ordered
2. ordered 2
3. ordered 3
4. a
5. b"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_unordered_list(self):
        md = """
- unordered
- list
- example
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>unordered</li><li>list</li><li>example</li></ul></div>",
        )
    def test_ordered_list(self):
        md = """
1. unordered
2. list
3. example
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>unordered</li><li>list</li><li>example</li></ol></div>",
        )
    def test_blockquote(self):
        md = """
> quote1
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote1</blockquote></div>",
        )
    def test_blockquote2(self):
        md = """
> quote1
>quote2
>quote3
> quote4
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote1\nquote2\nquote3\nquote4</blockquote></div>",
        )
    def test_heading1(self):
        md = """
# Heading 1
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1></div>",
        )
    def test_heading4(self):
        md = """
#### Heading 4
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>Heading 4</h4></div>",
        )
    def test_invalid_heading7(self):
        md = """
####### Heading 7
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>####### Heading 7</p></div>",
        )
    def test_link(self):
        md = """
[link0](hey a link)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><a href="hey a link">link0</a></p></div>',
        )
    def test_image_link(self):
        md = """
![imagelink](https://localhost/182739182.png)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><img src="https://localhost/182739182.png" alt="imagelink"></img></p></div>',
        )

if __name__ == "__main__":
    unittest.main()