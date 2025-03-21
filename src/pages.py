import os
import shutil

from blockmd import markdown_to_html_node


def copy_directory(src: str, dst: str) -> None:
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.makedirs(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            copy_directory(src_path, dst_path)

        else:
            shutil.copy(src_path, dst_path)


def extract_title(markdown_text: str) -> str:
    lines = markdown_text.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise ValueError("No h1 header found in markdown file")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(
        f"Generating page from {from_path} to {dest_path} using template: {template_path}")

    # Read markdown content
    with open(from_path, 'r') as f:
        markdown_content = f.read()

    # Read template
    with open(template_path, 'r') as f:
        template = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Get title
    title = extract_title(markdown_content)

    # Replace template placeholders
    html_doc = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content)

    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the output file
    with open(dest_path, 'w') as f:
        f.write(html_doc)
