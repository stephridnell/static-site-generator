import re

from textnode import TextNode, TextType

IMAGE_REGEX = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINK_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(markdown: str) -> list[tuple[str, str]]:
    return re.findall(IMAGE_REGEX, markdown)


def extract_markdown_links(markdown: str) -> list[tuple[str, str]]:
    return re.findall(LINK_REGEX, markdown)


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            # split the text at the image
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            # add the text before the image
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # add the image
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            # update the original text to the text after the image so that we can process the rest of the text
            # in the next iteration
            original_text = sections[1]

        # add the remaining text
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")

            # add the text before the link
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # add the link
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            # update the original text to the text after the image so that we can process the rest of the text
            # in the next iteration
            original_text = sections[1]

        # add the remaining text
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes
