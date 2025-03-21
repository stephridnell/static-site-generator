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


def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str) -> None:
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

    # Replace base path in href and src attributes
    html_doc = html_doc.replace(
        'href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')

    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the output file
    with open(dest_path, 'w') as f:
        f.write(html_doc)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str) -> None:
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)

        if os.path.isdir(content_path):
            # Recursively process subdirectories
            dest_subdir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(
                content_path, template_path, dest_subdir, base_path)

        elif content_path.endswith('.md'):
            # Generate HTML for markdown files
            rel_path = os.path.relpath(content_path, dir_path_content)
            dest_path = os.path.join(
                dest_dir_path, rel_path.replace('.md', '.html'))

            # Create the HTML page
            generate_page(content_path, template_path, dest_path, base_path)
