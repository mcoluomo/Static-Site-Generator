import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        split_node_text = node.text.split(delimiter)
        if len(split_node_text) % 2 == 0:
            msg = "invalid Markdown, formatted section not closed"
            raise ValueError(msg)

        for index, section in enumerate(split_node_text):
            if section.strip() == "":
                continue

            if index % 2 == 0:
                split_nodes.append(
                    TextNode(section, TextType.TEXT),
                )
            else:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extracted_image(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        images = extracted_image(node.text)
        if not images:
            if text.strip() == "":
                continue
            new_nodes.append(node)
            continue

        last_index = 0
        for alt, image_url in images:
            img_md = f"![{alt}]({image_url})"
            idx = text.find(img_md, last_index)

            if idx > last_index and text[last_index:idx].strip() != "":
                new_nodes.append(TextNode(text[last_index:idx], TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, image_url))
            last_index = idx + len(img_md)

        if last_index < len(text) and text[last_index:].strip() != "":
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes


def extracted_link(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        links = extracted_link(node.text)
        if not links:
            if text.strip() == "":
                continue

            new_nodes.append(node)
            continue

        last_index = 0
        for title, link_url in links:
            link_md = f"[{title}]({link_url})"
            idx = text.find(link_md, last_index)

            if idx > last_index and text[last_index:idx].strip() != "":
                new_nodes.append(TextNode(text[last_index:idx], TextType.TEXT))

            new_nodes.append(TextNode(title, TextType.LINK, link_url))
            last_index = idx + len(link_md)

        if last_index < len(text) and text[last_index:].strip() != "":
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes
