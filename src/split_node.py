import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node_text = node.text.split(delimiter)
        if len(split_node_text) % 2 == 0 or delimiter + delimiter in node.text:
            msg = "invalid Markdown, formatted section not closed"
            raise ValueError(msg)

        for index, section in enumerate(split_node_text):
            if section in {"", " "}:
                continue

            if index % 2 == 0:
                new_nodes.extend(
                    [TextNode(section, TextType.TEXT)],
                )
            else:
                new_nodes.extend([TextNode(section, text_type)])

    return new_nodes


def extracted_image(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extracted_image(node.text)
        if not images:
            continue

        text = node.text
        last_index = 0
        for alt, link in images:
            img_md = f"![{alt}]({link})"
            idx = text.find(img_md, last_index)
            if idx > last_index:
                new_nodes.append(TextNode(text[last_index:idx], TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            last_index = idx + len(img_md)
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes


def extracted_link(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    pass
