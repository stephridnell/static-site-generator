# Static Site Generator

A Python-based static site generator that converts Markdown content into HTML pages. This tool allows you to create static websites with a clean, maintainable structure using Markdown files and HTML templates.

Example live generated pages: [https://stephridnell.github.io/static-site-generator/](https://stephridnell.github.io/static-site-generator/)

## Features

- Convert Markdown files to HTML
- Support for nested directory structures
- Customizable HTML templates
- Static file handling (images, CSS, JavaScript, etc.)
- Configurable base path for assets and links
- Support for various Markdown elements:
  - Headings (h1-h6)
  - Bold text
  - Italic text
  - Code blocks
  - Links
  - Images
  - Lists
  - Blockquotes

## Project Structure

```
.
├── content/         # Markdown content files
├── static/          # Static assets (images, CSS, JS)
├── template.html    # HTML template for pages
├── docs/            # Generated static site
├── src/             # Source code and unit tests
├── main.sh          # Build locally at root directory and run local web server
├── test.sh          # Run unit tests
├── build.sh         # Build the site at /REPO_NAME/
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd static-site-generator
```

2. Ensure you have Python 3.7+ installed.

## Usage

1. Place your Markdown content files in the `content/` directory.
2. Add your static assets (images, CSS, JavaScript) to the `static/` directory.
3. Customize the `template.html` file to match your desired layout.
4. Run the generator:

```bash
./main.sh [base-path]
```

The `base-path` argument is optional. If not provided, it defaults to "/". This is useful when your site will be served from a subdirectory.

Example:

```bash
# For root path (default)
./main.sh

# For a subdirectory
./main.sh /my-site/
```

## Tests

The project includes a comprehensive test suite covering all major functionality.

To run the test suite:

```bash
# Run unit tests
./test.sh
```

## To deploy to GitHub Pages

Replace `REPO_NAME` in the `build.sh` script with your repository name and run:

```bash
./build.sh
```

Configure your repository Pages settings to be built from the `docs` folder in the `main` branch.

Push your changes to the `main` branch and they will be deployed to GitHub Pages at https://GITHUB-USERNAME.github.io/REPO-NAME/

## Template Syntax

The HTML template supports the following placeholders:

- `{{ Title }}`: Replaced with the page title (first h1 heading)
- `{{ Content }}`: Replaced with the converted HTML content

## Markdown Support

The generator supports standard Markdown syntax:

```markdown
# Heading 1

## Heading 2

### Heading 3

**bold text**
_italic text_
`code`

[link text](url)
![alt text](image-url)

- List item 1
- List item 2

> Blockquote
```

## Output

The generated site will be placed in the `docs/` directory, maintaining the same structure as your content directory but with HTML files instead of Markdown files. The `docs/` directory is used because that is what we need to use for GitHub pages.

## Acknowledgments

- Project completed as part of boot.dev backend dev course
