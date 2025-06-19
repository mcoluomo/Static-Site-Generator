import shutil
from logging import INFO, basicConfig, getLogger
from pathlib import Path

from block_markdown import markdown_to_html_node


def copy_static_to_public():
    dest_path = Path("docs")
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


def generate_page(from_path, template_path, dest_path, basepath):
    logger = getLogger(__name__)
    try:
        logger.info("Reading markdown from %s", from_path)
        markdown = from_path.read_text()
    except Exception:
        logger.exception("Failed to read markdown file %s", from_path)
        raise

    try:
        logger.info("Reading HTML template from %s", template_path)
        html_template = Path(template_path).read_text()
    except Exception:
        logger.exception("Failed to read template file %s", template_path)
        raise

    try:
        logger.info("Converting markdown to HTML nodes")
        markdown_as_html_nodes = markdown_to_html_node(markdown)
        html_content = markdown_as_html_nodes.to_html()
    except Exception:
        logger.exception("Failed to convert markdown to HTML")
        raise

    try:
        logger.info("Extracting title from %s", from_path)
        extracted_title = extract_title(from_path)
    except Exception:
        logger.exception("Failed to extract title from %s", from_path)
        raise

    try:
        logger.info("Filling template for %s", dest_path)
        html = (
            html_template.replace("{{ Title }}", extracted_title, 1)
            .replace(
                "{{ Content }}",
                html_content,
                1,
            )
            .replace('href="/', f'href="{basepath}')
            .replace('src="/', f'src="{basepath}')
        )
    except Exception:
        logger.exception("Failed to fill template for %s", dest_path)
        raise

    try:
        logger.info("Ensuring output directory exists for %s", dest_path)
        Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        logger.exception("Failed to create output directory for %s", dest_path)
        raise

    try:
        logger.info("Writing HTML to %s", dest_path)
        Path(dest_path).write_text(html, encoding="utf-8")
        logger.info(
            "Successfully generated page from %s to %s using %s",
            from_path,
            dest_path,
            template_path,
        )
    except Exception:
        logger.exception("Failed to write HTML to %s", dest_path)
        raise


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    basicConfig(level=INFO)
    logger = getLogger(__name__)

    current_item = Path(dir_path_content)
    if current_item.is_file() and current_item.suffix == ".md":
        try:
            logger.info("Generate a page")
            dest_dir = dest_dir_path.parent

            generate_page(
                current_item,
                template_path,
                dest_dir / "index.html",
                basepath,
            )

        except OSError as e:
            err_msg = f"An OS error occurred: {e}"
            logger.exception(err_msg)

    else:
        for child in current_item.iterdir():
            generate_pages_recursive(
                child,
                template_path,
                Path(dest_dir_path) / child.name,
                basepath,
            )
