from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list[HtmlNode], props: dict | None = None) -> None:
        super().__init__(tag, props=props, children=children)

    def to_html(self) -> str:
        if self.children is None:
            raise ValueError("Children are required for parent nodes")

        if self.tag is None:
            raise ValueError("Tag is required for parent nodes")

        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
