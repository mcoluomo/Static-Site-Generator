from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold" 
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    def __eq__(self, other):
        
        if not isinstance(other, TextNode):
            return False
        
        return (self.text == other.text 
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self):
        
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node:
        case TextNode(text=text, text_type=TextType.TEXT):
            return LeafNode(value=text)
        case TextNode(text=text, text_type=TextType.BOLD):
            return LeafNode("b", text)
        case TextNode(text=text, text_type=TextType.ITALIC):
            return LeafNode("i", text)
        case TextNode(text=text, text_type=TextType.CODE):
            return LeafNode("code", text)
        case TextNode(text=text, text_type=TextType.LINK, url=url):
            return LeafNode("a", text, {"href": url})
        case TextNode(text=text, text_type=TextType.IMAGE, url=url):
            return LeafNode(tag="img", props={"src": url, "alt": text})
        case _:
            raise ValueError("invalid node. Perhaps the wrong TextType was given")