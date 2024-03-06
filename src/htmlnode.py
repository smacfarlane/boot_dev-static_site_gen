class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        text = []
        if self.props is not None:
            for (key, value) in self.props.items():
                text.append(f'{key}="{value}"')

        return " ".join(text)

    def __repr__(self) -> str:
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"

class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)


    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("leaf node requires value")
        if self.tag is None:
            return self.value
        props = self.props_to_html()
        if props != "":
            props = " " + props
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"



