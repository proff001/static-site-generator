
class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props
	
	def to_html(self):
		raise NotImplementedError("to_html has not been implemented")
	
	def props_to_html(self):
		if self.props is None:
			return ""

		string = ""
		for key in self.props:
			string += f' {key}="{self.props[key]}"'

		return string

	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if not self.value:
			raise ValueError("LeafNode must have a value")
		
		if not self.tag:
			return self.value
		
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if not self.tag:
			raise ValueError("ParentNode must have a tag")
		
		if not self.children:
			raise ValueError("ParentNode must have children")

		string = f"<{self.tag}>"

		for child in self.children:
			string += child.to_html()

		string += f"</{self.tag}>"
		return string
