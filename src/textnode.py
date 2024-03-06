from htmlnode import HtmlNode, LeafNode

class TextNode:
    def __init__(self, text, text_type, url = None): 
        self.text = text 
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
                self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

InvalidTextTypeError = Exception
InvalidMarkdownError = Exception

def text_node_to_html_node(text_node) -> HtmlNode:
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})

    raise InvalidTextTypeError(text_node.text_type)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            nodes.append(node)
            continue

        split = node.text.split(delimiter)
        # Unclosed delimiters result in an even number of nodes
        if len(split) % 2 == 0:
            raise InvalidMarkdownError(f"unclosed delimeter: {delimiter}")
        for i in range(0, len(split)):
            if i % 2 == 0:
                nodes.append(TextNode(split[i], "text"))
            else:
                nodes.append(TextNode(split[i], text_type))

    return nodes
