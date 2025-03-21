import os

from pages import copy_directory, generate_page


def main():
    # copy everything from static to public
    if os.path.exists("static"):
        copy_directory("static", "public")

    # generate index page
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
