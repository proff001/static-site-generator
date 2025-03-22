import re

from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	ULIST = "unordered_list"
	OLIST = "ordered_list"

def markdown_to_blocks(text):
	blocks = text.split("\n\n")
	return list(filter(lambda line: line != "", map(lambda block: block.strip(), blocks)))

def block_to_block_type(block):
	if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
		return BlockType.HEADING

	lines = block.split("\n")
	if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):  
		return BlockType.CODE

	if not False in map(lambda line: line.startswith("> "), lines):
		return BlockType.QUOTE

	if not False in map(lambda line: line.startswith("- "), lines):
		return BlockType.ULIST

	if not False in map(lambda line: re.match(r"\d+\. ", line) != None, lines):
		return BlockType.OLIST

	return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
	children = []
	blocks = markdown_to_blocks(markdown)

	for block in blocks:
		block_type = block_to_block_type(block)

		match block_type:
			case BlockType.HEADING:
				children.append(heading_to_html_node(block))
			case BlockType.PARAGRAPH:
				children.append(paragraph_to_html_node(block))
			case BlockType.CODE:
				children.append(code_to_html_node(block))
			case BlockType.QUOTE:
				children.append(quote_to_html_node(block))
			case BlockType.ULIST:
				children.append(ulist_to_html_node(block))
			case BlockType.OLIST:
				children.append(olist_to_html_node(block))

	return ParentNode("div", children)

def text_to_html_nodes(text):
	text_nodes = text_to_textnodes(text)
	html_nodes = map(text_node_to_html_node, text_nodes)
	return list(html_nodes)

def heading_to_html_node(block):
	level = block.count("#", 0, 6)
	children =text_to_html_nodes(block[level + 1:])
	return ParentNode(f"h{level}", children)

def paragraph_to_html_node(block):
	children = text_to_html_nodes(" ".join(block.split("\n")))
	return ParentNode("p", children)

def code_to_html_node(block):
	text_node = TextNode(block[4:-3], TextType.TEXT)
	child = text_node_to_html_node(text_node)
	code = ParentNode("code", [child])
	return ParentNode("pre", [code])

def quote_to_html_node(block):
	lines = block.split("\n")
	parsed = map(lambda line: line[2:].strip(), lines)
	children = text_to_html_nodes(" ".join(parsed))
	return ParentNode("blockquote", children)

def ulist_to_html_node(block):
	lines = block.split("\n")
	parsed = map(lambda line: line[2:].strip(), lines)
	children = list(map(lambda line: ParentNode("li", text_to_html_nodes(line)), parsed))
	return ParentNode("ul", children)

def olist_to_html_node(block):
	lines = block.split("\n")
	parsed = map(lambda line: line[3:].strip(), lines)
	children = list(map(lambda line: ParentNode("li", text_to_html_nodes(line)), parsed))
	return ParentNode("ol", children)
