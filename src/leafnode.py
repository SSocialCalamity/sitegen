from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if(self.value == None):
            raise ValueError
        if(self.tag == None):
            return(self.value)
        builder_str = f"<{self.tag}"
        builder_str += self.props_to_html()
        builder_str += f">{self.value}</{self.tag}>"
        return(builder_str)

    def __repr__(self):
        repr = f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"
        return(repr)