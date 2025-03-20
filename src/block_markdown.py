
def markdown_to_blocks(text):
	blocks = text.split("\n\n")

	return list(map(lambda block: block.strip(), blocks))
