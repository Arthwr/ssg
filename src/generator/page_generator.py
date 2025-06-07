import os

from markdown.block_markdown import markdown_to_html_node
from markdown.inline_markdown import extract_title


def traverse_and_generate_html(source, template_path, destination, basepath):
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(src_path):
            root, ext = os.path.splitext(dest_path)
            if ext:
                dest_path = root + ".html"

            print(f" * converting {src_path} -> {dest_path}")
            generate_page(src_path, template_path, dest_path, basepath)

        elif os.path.isdir(src_path):
            traverse_and_generate_html(src_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    with open(from_path) as md_text:
        md_data = md_text.read()

    with open(template_path) as tmpl_text:
        tmpl_data = tmpl_text.read()

    html_content = markdown_to_html_node(md_data).to_html()
    title = extract_title(md_data)

    final_html = (
        tmpl_data
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as file:
        file.write(final_html)
