import re

from textnode import TextNode, TextType

def text_to_textnodes(text):
	nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)

	return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []

	for node in old_nodes:
		if node.type != TextType.TEXT:
			new_nodes.append(node)
			continue

		split_nodes = []
		sections = node.text.split(delimiter)

		if len(sections) % 2 == 0:
			raise ValueError("invalid markdown, formatted section not closed")
		
		for i in range(len(sections)):
			if sections[i] == "":
				continue
			elif i % 2 == 0:
				split_nodes.append(TextNode(sections[i], TextType.TEXT))
			else:
				split_nodes.append(TextNode(sections[i], text_type))

		new_nodes.extend(split_nodes)

	return new_nodes

def split_nodes_image(old_nodes):
	new_nodes = []

	for node in old_nodes:
		images = extract_markdown_images(node.text)

		if len (images) < 1:
			new_nodes.append(node)
			continue

		remaining_text = node.text
		for image in images:
			sections = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
			
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			
			new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
			remaining_text = sections[1]

		if remaining_text != "":
			new_nodes.append(TextNode(remaining_text, TextType.TEXT))

	return new_nodes

def split_nodes_link(old_nodes):
	new_nodes = []

	for node in old_nodes:
		links = extract_markdown_links(node.text)

		if len (links) < 1:
			new_nodes.append(node)
			continue

		remaining_text = node.text
		for link in links:
			sections = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
			new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
			remaining_text = sections[1]

		if remaining_text != "":
			new_nodes.append(TextNode(remaining_text, TextType.TEXT))

	return new_nodes


def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
