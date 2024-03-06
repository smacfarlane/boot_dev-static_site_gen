from extractors import extract_markdown_images, extract_markdown_links
from htmlnode import HtmlNode, LeafNode
from enum import Enum

class TextType(Enum):
    Text = 1
    Bold = 2,
    Italic = 3,
    Code = 4,
    Link = 5,
    Image = 6
    
    def delimeter(self) -> str | None:
        if self == TextType.Text:
            return None
        if self == TextType.Bold:
            return "**"
        if self == TextType.Italic:
            return "*"
        if self == TextType.Code:
            return "`"
        #TODO: Link and Image 
        return None
    
    def __str__(self) -> str:
        if self == TextType.Text:
            return "text"
        if self == TextType.Bold:
            return "bold"
        if self == TextType.Italic:
            return "italic"
        if self == TextType.Code:
            return "code"
        if self == TextType.Link:
            return "link"
        if self == TextType.Image:
            return "image"
        return ""

class TextNode:
    def __init__(self, text, text_type: TextType, url = None): 
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
    if text_node.text_type == TextType.Text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.Bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.Italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.Code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.Link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.Image:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})

    raise InvalidTextTypeError(text_node.text_type)

def split_nodes_delimiter(old_nodes, text_type: TextType) -> list[TextNode]:
    nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            nodes.append(node)
            continue

        split = node.text.split(text_type.delimeter())
        # Unclosed delimiters result in an even number of nodes
        if len(split) % 2 == 0:
            raise InvalidMarkdownError(f"unclosed delimeter: {text_type.delimeter()}")
        for i in range(0, len(split)):
            if i % 2 == 0:
                nodes.append(TextNode(split[i], TextType.Text))
            else:
                nodes.append(TextNode(split[i], text_type))

    return nodes

def split_nodes_image(old_nodes) -> list[TextNode]:
    result = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            result.append(old_node.text)
            continue


        unparsed = old_node.text
        for (alt, src) in images:
            split = unparsed.split(f"![{alt}]({src})", 1)
            if split[0] != "":
                result.append(TextNode(split[0], TextType.Text))
            result.append(TextNode(alt, TextType.Image, src))
            unparsed = split[1]

        if unparsed != "":
            result.append(TextNode(unparsed, TextType.Text))
 
    return result

def split_nodes_link(old_nodes) -> list[TextNode]:
    result = []
    for old_node in old_nodes:
        images = extract_markdown_links(old_node.text)
        if len(images) == 0:
            result.append(old_node)
            continue

        unparsed = old_node.text
        for (value, href) in images:
            split = unparsed.split(f"[{value}]({href})", 1)
            if split[0] != "":
                result.append(TextNode(split[0], TextType.Text))
            result.append(TextNode(value, TextType.Link, href))

            unparsed = split[1]

        if unparsed != "":
            result.append(TextNode(unparsed, TextType.Text))
     
    return result

