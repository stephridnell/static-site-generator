class HtmlNode:
    def __init__(self, tag: str | None = None, value: str | None = None,
                 children: list['HtmlNode'] | None = None, props: dict | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html not implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        return " " + " ".join([f"{k}=\"{v}\"" for k, v in self.props.items()])

    def __repr__(self) -> str:
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
