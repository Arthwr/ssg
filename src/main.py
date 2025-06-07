import sys

from generator.static_handler import copy_static_files
from generator.page_generator import traverse_and_generate_html
from config import (
    STATIC_FILES_DIRECTORY,
    INPUT_CONTENT_DIRECTORY,
    TEMPLATE_FILE_PATH,
    OUTPUT_DIRECTORY,
)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Copying static files...")
    copy_static_files(STATIC_FILES_DIRECTORY, OUTPUT_DIRECTORY)

    print(
        f"Generating pages from '/{INPUT_CONTENT_DIRECTORY}' to '/{OUTPUT_DIRECTORY}' using {TEMPLATE_FILE_PATH}:"
    )
    traverse_and_generate_html(
        INPUT_CONTENT_DIRECTORY, TEMPLATE_FILE_PATH, OUTPUT_DIRECTORY, basepath
    )


if __name__ == "__main__":
    main()
