from textnode import TextNode

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            splitNodeText = node.text.split(delimiter)
            if len(splitNodeText) % 2 == 0 or delimiter + delimiter in node.text :
                raise Exception("invalid Markdown syntax")
            
            for index in range(len(splitNodeText)):
                if splitNodeText[index] == "" or splitNodeText[index] == " ":
                    continue

                else:
                    if index % 2 == 0:
                        new_nodes.extend([TextNode(splitNodeText[index], node.text_type)])
                    else:
                        new_nodes.extend([TextNode(splitNodeText[index], text_type)])

    return new_nodes
