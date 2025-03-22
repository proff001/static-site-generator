import os

from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_pages_recursively(content_path, template_path, dest_dir_path):
	for file in os.listdir(content_path):
		from_path = os.path.join(content_path, file)
		dest_path = os.path.join(dest_dir_path, file)

		if os.path.isfile(from_path):
			dest_path = Path(dest_path).with_suffix(".html")
			generate_page(from_path, template_path, dest_path)
		elif os.path.isdir(os.path.join(content_path, file)):
			generate_pages_recursively(from_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
	print("Generating page from", from_path, "to", dest_path)

	with open(from_path, "r") as file:
		content = file.read()

	with open(template_path, "r") as file:
		template = file.read()

	title = extract_title(content)
	node = markdown_to_html_node(content)
	html = node.to_html()

	template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

	dest_dir_path = os.path.dirname(dest_path)
	if not os.path.exists(dest_dir_path):
		os.makedirs(dest_dir_path)

	with open(dest_path, "w") as file:
		file.write(template)

def extract_title(markdown):
	lines = markdown.split("\n")
	for line in lines:
		if line.startswith("# "):
			return line[2:].strip()

	raise ValueError("no title found")
