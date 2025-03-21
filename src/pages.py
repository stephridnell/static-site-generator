import os
import shutil


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
