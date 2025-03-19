import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
	def test_text(self):
		node = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node.text, "This is a text node")

	def test_type(self):
		node = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node.type, TextType.BOLD)

	def test_url(self):
		node = TextNode("This is a text node", TextType.BOLD, None)
		self.assertEqual(node.url, None)

	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_repr(self):
		node = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(repr(node), "TextNode(This is a text node, TextType.BOLD, None)") 

class TestTextNodeToHTMLNode(unittest.TestCase):
	def test_text(self):
		node = TextNode("This is a text node", TextType.NORMAL)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
		node = TextNode("This is a text node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a text node")

	def test_italic(self):
		node = TextNode("This is a text node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is a text node")

	def test_code(self):
		node = TextNode("This is a text node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a text node")

	def test_link(self):
		node = TextNode("This is a text node", TextType.LINK, "https://google.com/")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a text node")
		self.assertEqual(html_node.props, { "href": "https://google.com/" })

	def test_image(self):
		node = TextNode("This is a text node", TextType.IMAGE, "https://google.com/")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props, { "src": "https://google.com/", "alt": "This is a text node" })

if __name__ == '__main__':
	unittest.main()