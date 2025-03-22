import unittest

from markdown_blocks import (
	BlockType,
	block_to_block_type,
	markdown_to_blocks,
	markdown_to_html_node
)

class TestBlockMarkdown(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(blocks, [
			"This is **bolded** paragraph",
			"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
			"- This is a list\n- with items",
		])

	def test_markdown_blocks_to_block_types(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		block_types = list(map(block_to_block_type, blocks))
		self.assertEqual(block_types, [
			BlockType.PARAGRAPH,
			BlockType.PARAGRAPH,
			BlockType.ULIST,
		])
	
	def test_markdown_block_to_paragraph(self):
		block = "This is a paragraph"
		self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
	
	def test_markdown_blocks_to_headings(self):
		blocks = markdown_to_blocks("""
# Heading 1\n\n
## Heading 2\n\n
### Heading 3\n\n
#### Heading 4\n\n
##### Heading 5\n\n
###### Heading 6
""")
		block_types = list(map(block_to_block_type, blocks))
		self.assertEqual(block_types, [
			BlockType.HEADING,
			BlockType.HEADING,
			BlockType.HEADING,
			BlockType.HEADING,
			BlockType.HEADING,
			BlockType.HEADING,
		])

	def test_block_to_block_types(self):
		block = "# heading"
		self.assertEqual(block_to_block_type(block), BlockType.HEADING)
		block = "```\ncode\n```"
		self.assertEqual(block_to_block_type(block), BlockType.CODE)
		block = "> quote\n> more quote"
		self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
		block = "- list\n- items"
		self.assertEqual(block_to_block_type(block), BlockType.ULIST)
		block = "1. list\n2. items"
		self.assertEqual(block_to_block_type(block), BlockType.OLIST)
		block = "paragraph"
		self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

	def test_markdown_block_to_code(self):
		block = "```\ncode\n```"
		self.assertEqual(block_to_block_type(block), BlockType.CODE)

	def test_markdown_block_to_code_with_invalid_syntax(self):
		block = "```\ncode\n`"
		self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

	def test_markdown_block_to_quote(self):
		block = "> This is a quote\n> with multiple lines\n> and more"
		self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

	def test_markdown_block_to_quote_with_invalid_syntax(self):
		block = "> This is a quote\n> with multiple lines\n* and more"
		self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

	def test_markdown_block_to_unordered_list(self):
		block = "- This is an unordered list\n- with multiple lines\n- and more"
		self.assertEqual(block_to_block_type(block), BlockType.ULIST)

	def test_markdown_block_to_unordered_list_with_invalid_syntax(self):
		block = "- This is an unordered list\n- with multiple lines\n* and more"
		self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

	def test_markdown_block_to_ordered_list(self):
		block = "1. This is an ordered list\n2. with multiple lines\n3. and more"
		self.assertEqual(block_to_block_type(block), BlockType.OLIST)

	def test_markdown_block_to_ordered_list_with_invalid_syntax(self):
		block = "1. This is an ordered list\n2. with multiple lines\n* and more"
		self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
		)

	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)



	def test_paragraph(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
		)

	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
		)

	def test_lists(self):
		md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
		)

	def test_headings(self):
		md = """
# this is an h1

this is paragraph text

## this is an h2
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
		)

	def test_blockquote(self):
		md = """
> This is a
> blockquote block

this is paragraph text

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
		)

	def test_code(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)


if __name__ == "__main__":
	unittest.main()
