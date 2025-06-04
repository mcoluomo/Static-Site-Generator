import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_html_node(markdown):
    split_markdown = markdown_to_blocks(markdown)
    for block in split_markdown:
        block_type = block_to_block_type(block)
        new_text_node = text_to_children(block)


# returns list of html nodes from block text
def text_to_children(text):
    html_nodes = []
    text_nodes_list = text_to_textnodes(text)
    for node in text_nodes_list:
        html_node_from_text_node = text_node_to_html_node(node)
        html_nodes.append(html_node_from_text_node)

def block_to_block_type(block_of_markdown):
    match block_of_markdown:
        case s if s.startswith(
            (
                "# ",
                "## ",
                "### ",
                "#### ",
                "##### ",
                "###### ",
            ),
        ):
            return BlockType.HEADING
        case s if s.startswith("```") and s.endswith("```"):
            return BlockType.CODE
        case s if s.startswith(">"):
            return BlockType.QUOTE
        case s if s.startswith("- "):
            return BlockType.ULIST
        case s if re.match(r"^\d+\.\s", s):
            return BlockType.OLIST
        case _:
            return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    return [inline.strip() for inline in split_markdown if inline.strip() != ""]
