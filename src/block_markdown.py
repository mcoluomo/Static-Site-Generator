import re
from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_html_node(markdown):
    block_nodes_children = []
    split_markdown = markdown_to_blocks(markdown)
    for block in split_markdown:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            text = block.removeprefix("```").removesuffix("```")
            cleaned_text = re.sub(r"\n\s+", "\n", text).removeprefix("\n")
            child_node = text_node_to_html_node(TextNode(cleaned_text, TextType.CODE))
            block_nodes_children.append(ParentNode("pre", [child_node]))
        else:
            child_node = text_to_children(block)
            if isinstance(child_node, list):
                block_nodes_children.extend(child_node)
            else:
                block_nodes_children.append(child_node)

    return ParentNode("div", block_nodes_children)


# returns list of html (leafnodes) nodes currently from block text
def text_to_children(text):
    block_type = block_to_block_type(text)

    match block_type:
        case BlockType.QUOTE:
            split_text = re.sub(r"\n?>\s", "\n", text).split("\n")
            cleaned_split_text = [s.strip() for s in split_text if s.strip()]
            list_leaf_nodes = [LeafNode(value=text) for text in cleaned_split_text]
            return ParentNode("blockquote", list_leaf_nodes)

        case BlockType.OLIST:
            split_text = re.split(r"\n?[1-9]\d*\.\s", text)
            cleaned_split_text = [s.strip() for s in split_text if s.strip()]

            list_leaf_nodes = [LeafNode("li", text) for text in cleaned_split_text]
            return ParentNode("ol", list_leaf_nodes)

        case BlockType.ULIST:
            split_text = re.sub(r"\n?-\s", "\n", text).split("\n")
            cleaned_split_text = [s.strip() for s in split_text if s.strip()]
            list_leaf_nodes = [LeafNode("li", text) for text in cleaned_split_text]

            return ParentNode("ul", list_leaf_nodes)

        case BlockType.HEADING:
            split_text = re.sub(r"\n?#+\s", "\n", text).split("\n")

            cleaned_split_text = [s.strip() for s in split_text if s.strip()]
            matches = re.findall(r"^\n?#+", text)
            tag_type = len("".join(matches))
            return [LeafNode(f"h{tag_type}", text) for text in cleaned_split_text]

        case _:
            new_text_block = " ".join(text.replace("\n", "").split())
            text_nodes_list = text_to_textnodes(new_text_block)
            leaf_nodes = [text_node_to_html_node(node) for node in text_nodes_list]
            return ParentNode("p", leaf_nodes)


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
