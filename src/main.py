from logging import INFO, basicConfig, getLogger

from generate_website import (
    copy_static_to_public,
    generate_pages_recursive,
)


def main():
    basicConfig(level=INFO)
    logger = getLogger(__name__)

    try:
        logger.info("Starting static site generation...")
        copy_static_to_public()
        logger.info("Static files copied to Public directory successfully.")
    except OSError as e:
        err_msg = f"An OS error occurred: {e}"
        logger.exception(err_msg)

    try:
        logger.info("Generate a pages from content recursively")
        generate_pages_recursive("content", "template.html", "public")
        logger.info("Generating Static sites successfully")
    except OSError as e:
        err_msg = f"An OS error occurred: {e}"
        logger.exception(err_msg)


if __name__ == "__main__":
    main()
