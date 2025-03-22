import os
import sys
import shutil

from copystatic import copy_files_recursively
from gencontent import generate_pages_recursively

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
	basepath = "/"

	if len(sys.argv) > 1:
		basepath = sys.argv[1]

	print("Basepath:", basepath)

	print("Deleting old public directory...")
	if os.path.exists(dir_path_public):
		shutil.rmtree(dir_path_public)

	print("Copying static files to public directory...")
	copy_files_recursively(dir_path_static, dir_path_public)

	print("Generating pages...")
	generate_pages_recursively(dir_path_content, template_path, dir_path_public, basepath)

main()
