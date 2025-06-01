from split_node import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


def text_to_textnodes(text):
    if text.strip() == "":
        return []

    delimiters_in_text = [
        delimiter for delimiter in ["**", "_", "`"] if delimiter in text
    ]
    previous_nodes = [TextNode(text, TextType.TEXT)]
    delimiter_texttype = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE,
    }

    while True:
        nodes_before = previous_nodes.copy()

        current_nodes = split_nodes_image(previous_nodes)
        if current_nodes != previous_nodes:
            previous_nodes = current_nodes

        current_nodes = split_nodes_link(previous_nodes)
        if current_nodes != previous_nodes:
            previous_nodes = current_nodes

        if not delimiters_in_text:
            break
        for delimiter in delimiters_in_text:
            current_nodes = split_nodes_delimiter(
                previous_nodes,
                delimiter,
                delimiter_texttype[delimiter],
            )
            if current_nodes != previous_nodes:
                previous_nodes = current_nodes

        if previous_nodes == nodes_before:
            break

    return previous_nodes
