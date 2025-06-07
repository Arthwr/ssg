from copystatic import copy_static_files
from generate_page import traverse_and_generate_html

DIR_PATH_STATIC = "static"
DIR_PATH_PUBLIC = "public"
DIR_PATH_CONTENT = "content"
TEMPLATE_PATH = "template.html"


def main():
    copy_static_files(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    print(
        f"Generating pages from '/{DIR_PATH_CONTENT}' to '/{DIR_PATH_PUBLIC}' using {TEMPLATE_PATH}:"
    )
    traverse_and_generate_html(DIR_PATH_CONTENT, TEMPLATE_PATH, DIR_PATH_PUBLIC)


main()
