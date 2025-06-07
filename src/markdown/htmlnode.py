class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""

        html_props = " ".join(
            map(lambda str: f'{str[0]}="{str[1]}"', self.props.items())
        )
        html_str = " " + html_props

        return html_str


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        elif self.tag is None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def traverse_children(self):
        result = ""
        for node in self.children:
            result += node.to_html()

        return result

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        elif self.children is None:
            raise ValueError("Invaild HMTL: no children passed")
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.traverse_children()}</{self.tag}>"
