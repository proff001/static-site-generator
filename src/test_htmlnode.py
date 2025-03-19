import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
	def test_tag(self):
		node = HTMLNode("p", "Hello, world!", None, None)
		self.assertEqual(node.tag, "p")

	def test_value(self):
		node = HTMLNode("p", "Hello, world!", None, None)
		self.assertEqual(node.value, "Hello, world!")

	def test_children(self):
		node = HTMLNode("p", "Hello, world!", None, None)
		self.assertEqual(node.children, None)

	def test_props(self):
		node = HTMLNode("p", "Hello, world!", None, None)
		self.assertEqual(node.props, None)

	def test_props_to_html(self):
		node = HTMLNode(props={ "href": "https://www.google.com", "target": "_blank" })
		self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

	def test_props_to_html_no_props(self):
		node = HTMLNode()
		self.assertEqual(node.props_to_html(), "")

	def test_repr(self):
		node = HTMLNode("p", "Hello, world!", None, None)
		self.assertEqual(repr(node), "HTMLNode(p, Hello, world!, None, None)")

	def test_leaf_to_html(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_props(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

	def test_leaf_no_value(self):
		node = LeafNode("p", None)
		self.assertRaises(ValueError, node.to_html)

	def test_to_html_with_no_tag(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode(None, [child_node])
		self.assertRaises(ValueError, parent_node.to_html)

	def test_to_html_with_no_child(self):
		parent_node = ParentNode("div", None)
		self.assertRaises(ValueError, parent_node.to_html)

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
		)

if __name__ == '__main__':
	unittest.main()