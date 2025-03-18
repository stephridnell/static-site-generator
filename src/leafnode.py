from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(self, tag: str, value: str | None, props: dict | None = None) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value is required for leaf nodes")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
