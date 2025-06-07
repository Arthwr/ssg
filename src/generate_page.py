import os

from block_markdown import markdown_to_html_node
from inline_markdown import extract_title


def traverse_and_generate_html(source, template, destination):
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(src_path):
            root, ext = os.path.splitext(dest_path)
            if ext:
                dest_path = root + ".html"

            print(f" * converting {src_path} -> {dest_path}")
            generate_page(
                src_path,
                template,
                dest_path,
            )

        elif os.path.isdir(src_path):
            traverse_and_generate_html(src_path, template, dest_path)


def generate_page(from_path, template_path, dest_path):
    with open(from_path) as md_text:
        md_data = md_text.read()

    with open(template_path) as tmpl_text:
        tmpl_data = tmpl_text.read()

    html_str = markdown_to_html_node(md_data).to_html()
    html_title = extract_title(md_data)

    html_content = tmpl_data.replace("{{ Title }}", html_title).replace(
        "{{ Content }}", html_str
    )

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as file:
        file.write(html_content)
