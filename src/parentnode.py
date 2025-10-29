from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if(self.tag == None):
            raise ValueError("No tag in parent node")
        if(self.children == None):
            raise ValueError("Children do not exist")
        builder_str = f"<{self.tag}"
        builder_str += self.props_to_html()
        builder_str += f">"
        for child in self.children:
            builder_str += child.to_html()
        builder_str += f"</{self.tag}>"
        return(builder_str)

    def __repr__(self):
        repr = f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"
        return(repr)