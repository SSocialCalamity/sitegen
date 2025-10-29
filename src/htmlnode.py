class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        propstr = ""
        for prop in self.props:
            propstr += " " + str(prop) + '="' + str(self.props[prop]) + '"'
        return(propstr)

    def __repr__(self):
        repr = f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        return(repr)