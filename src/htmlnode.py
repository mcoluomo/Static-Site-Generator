

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag: str | None= tag
        self.value: str | None= value
        self.children: list = children or []
        self.props: dict = props or {}
        
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""

        props_strings = []
        for key, value in self.props.items():
            props_strings.append(f' {key}="{value}"')

        return "".join(props_strings)

    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("No value was given")
        if not self.tag:
            return self.value
        
        props_string = super().props_to_html()

        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
    
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag attribute was given")
        if not self.children:
            raise ValueError("No children attribute was given")
        
        htmlNode = ""
        for node in self.children:
            leafNodestr = node.to_html()
            
            htmlNode += leafNodestr

        props_string = super().props_to_html()
        return f"<{self.tag}{props_string}>{htmlNode}</{self.tag}>"