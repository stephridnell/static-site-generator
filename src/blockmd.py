def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(lambda x: x != "", map(lambda x: x.strip(), blocks)))
