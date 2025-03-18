from textnode import TextNode, TextType


def main():
    print("# hello world")
    text_node = TextNode("hello world", TextType.LINK,
                         "https://www.google.com")
    print(text_node)


if __name__ == "__main__":
    main()
