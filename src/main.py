import os

from pages import copy_directory
from textnode import TextNode, TextType


def main():
    # copy everything from static to public
    if os.path.exists("static"):
        copy_directory("static", "public")


if __name__ == "__main__":
    main()
