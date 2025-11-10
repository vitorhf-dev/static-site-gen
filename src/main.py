import os
import shutil
import sys
from copystatic import copystatic
from gencontent import generate_page

dir_path_public = "docs"
dir_path_static = "static"
dir_path_content = "content"
template_path = "template.html"

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

def generate_pages_recursive(content_root, template_path, public_root, basepath):
    for root, _, files in os.walk(content_root):
        for name in files:
            if not name.endswith(".md"):
                continue
            from_path = os.path.join(root, name)
            rel = os.path.relpath(from_path, content_root)
            rel_no_ext = os.path.splitext(rel)[0]
            parts = rel_no_ext.split(os.sep)

            if parts == ["index"]:
                dest_path = os.path.join(public_root, "index.html")
            elif parts[-1] == "index":
                dest_path = os.path.join(public_root, *parts[:-1], "index.html")
            else:
                dest_path = os.path.join(public_root, *parts, "index.html")

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_page(from_path, template_path, dest_path, basepath)

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copystatic(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

if __name__ == "__main__":
    main()