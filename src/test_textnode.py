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

if __name__ == '__main__':
	unittest.main()