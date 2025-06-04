import os
import shutil


def recursive_copy(source_folder, target_folder):
    for item in os.listdir(source_folder):
        src_path = os.path.join(source_folder, item)
        dest_path = os.path.join(target_folder, item)

        print(f" * {src_path} -> {dest_path}")

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            os.mkdir(dest_path)
            recursive_copy(src_path, dest_path)


def convert_static_to_public(source, target):
    if not os.path.isdir(source):
        raise Exception(f"No {source} folder found")

    if os.path.exists(target):
        print("Deleting public directory...")
        shutil.rmtree(target)

    os.mkdir(target)
    print("Copying static files to public directory:")
    recursive_copy(source, target)
