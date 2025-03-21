import os
import sys

from pages import copy_directory, generate_pages_recursive


def main():
    # Get base path from command line argument, default to "/"
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    # copy everything from static to public
    if os.path.exists("static"):
        copy_directory("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", base_path)


if __name__ == "__main__":
    main()
