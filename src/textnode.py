from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def to_html_node(self):
        match(self.text_type):
            case TextType.TEXT:
                node = LeafNode(None, self.text)
                return(node)
            case TextType.BOLD:
                node = LeafNode("b", self.text)
                return(node)
            case TextType.ITALIC:
                node = LeafNode("i", self.text)
                return(node)
            case TextType.CODE:
                node = LeafNode("code", self.text)
                return(node)
            case TextType.LINK:
                node = LeafNode("a", self.text, {"href": self.url})
                return(node)
            case TextType.IMAGE:
                node = LeafNode("img", "", {"src": self.url, "alt": self.text})
                return(node)
            case _:
                raise Exception(f"Not a valid TextType: {self.text_type}")
    
    def __eq__(self, other):
        if((self.text == other.text)
         and (self.text_type == other.text_type)
         and (self.url == other.url)):
            return True
        return False
    
    def __repr__(self):
        repr = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return(repr)
