class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key,value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value Error. LeafNodes must have a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        all_children = ""
        if self.tag is None:
            raise ValueError("Value Error. ParentNodes must have a tag")
        if self.children is None:
            raise ValueError("Value Error. ParentNodes must have children")
        for self.child in self.children:
            all_children += self.child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{all_children}</{self.tag}>'
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
