import shutil
from pathlib import Path

from block_markdown import markdown_to_html_node


def copy_static_to_public():
    dest_path = Path("public")
    src_path = Path("static")
    if not src_path.exists():
        err_msg = f"The directory {src_path} does not exist."
        raise FileNotFoundError(err_msg)

    if dest_path.exists():
        shutil.rmtree(dest_path)
    dest_path.mkdir(exist_ok=False)

    for item in src_path.iterdir():
        helper_copy_directory(item, dest_path / item.name)

    print(f"* {src_path} -> {dest_path}")


def helper_copy_directory(src_item, dest_item):
    if src_item.is_file():
        shutil.copy2(src_item, dest_item)

    elif src_item.is_dir():
        dest_item.mkdir(exist_ok=True)
        for child in src_item.iterdir():
            helper_copy_directory(child, dest_item / child.name)


class TitleNotFoundError(Exception):
    """Raised when a title cannot be extracted from markdown."""


def extract_title(markdown):
    file = Path(markdown)
    markdown_content = file.read_text()

    if markdown_content.startswith("# "):
        return markdown_content.removeprefix("# ")

    err_msg = "No title found in the provided markdown."
    raise TitleNotFoundError(err_msg)


def generate_page(from_path, template_path, dest_path):
    markdown = Path(from_path).read_text()

    html_template = Path(template_path).read_text()

    markdown_as_html_nodes = markdown_to_html_node(markdown)
    html_content = markdown_as_html_nodes.to_html()
    extracted_title = extract_title(from_path)

    html = html_template.replace("{{ Title }}", extracted_title, 1).replace(
        "{{ Content }}",
        html_content,
        1,
    )

    Path(dest_path).parent.mkdir(parents=True, exist_ok=True)

    Path(dest_path).write_text(html, encoding="utf-8")
    print(f"* Generating page from {from_path} to {dest_path} using {template_path}")
