from enum import Enum
import re

from htmlnode import HtmlNode, LeafNode, ParentNode

class BlockType(Enum):
    Paragraph = 1,
    Heading = 2,
    Code = 3,
    Quote = 4,
    UnorderedList = 5,
    OrderedList = 6,

def block_to_block_type(input: str) -> BlockType:
    heading_re = r"^#{1,6} "

    if re.match(heading_re, input):
        return BlockType.Heading
    if input.startswith("```") and input.endswith("```") and len(input) >= 6:
        return BlockType.Code

    lines = input.split("\n")

    if is_quote_block(lines):
        return BlockType.Quote
    if is_unordered_list(lines):
        return BlockType.UnorderedList
    if is_ordered_list(lines):
        return BlockType.OrderedList
    

    return BlockType.Paragraph

def is_quote_block(lines: list[str]) -> bool:
    for line in lines:
        if not line.startswith(">"):
            return False

    return True
    
def is_unordered_list(lines: list[str]) -> bool:
    for line in lines:
        if not (line.startswith("*") or line.startswith("-")):
            return False

    return True

def is_ordered_list(lines: list[str]) -> bool:
    count = 1

    for line in lines:
        if not line.startswith(f"{count}."):
            return False
        count += 1

    return True

def markdown_to_blocks(md: str) -> list[str]:
    split = md.split("\n\n")
    result = []
    for para in split:
        para = para.strip()
        if para != "":
            result.append(para)

    return result

def heading_to_html_node(block: str) -> HtmlNode:
    # Assumption: this is a heading block and therefore is one to six '#' followed by a space
    split = block.split(' ', 1)
    heading = f"h{len(split[0])}"
    text = split[1]
    return LeafNode(heading, text)

def unordered_list_to_html_node(block: str) -> HtmlNode:
    lines = block.split("\n")
    children = []
    for line in lines:
        node = LeafNode("li", line[1:])
        children.append(node)
    return ParentNode("ul", children)

def ordered_list_to_html_node(block: str) -> HtmlNode:
    lines = block.split("\n")
    children = []
    for line in lines:
        # Assumption: each line starts with Number.
        line = line.split(".", 1)[1]
        node = LeafNode("li", line)
        children.append(node)
    return ParentNode("ol", children)

def code_block_to_html_node(block:str) -> HtmlNode:
    code = block[3:-3]
    
    return ParentNode("pre", [LeafNode("code", code)])

def quote_block_to_html_node(block:str) -> HtmlNode:
    lines = block.split("\n")
    result = []
    for line in lines:
        result.append(line[1:])

    return LeafNode("blockquote", "\n".join(result))

def paragraph_to_html_node(block:str) -> HtmlNode:
    return LeafNode("p", block)

def markdown_to_html_node(md: str) -> HtmlNode:
    blocks = markdown_to_blocks(md)

    result = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.Paragraph:
            result.append(paragraph_to_html_node(block))
        elif block_type == BlockType.Quote:
            result.append(quote_block_to_html_node(block))
        elif block_type == BlockType.Code:
            result.append(code_block_to_html_node(block))
        elif block_type == BlockType.OrderedList:
            result.append(ordered_list_to_html_node(block))
        elif block_type == BlockType.UnorderedList:
            result.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.Heading:
            result.append(heading_to_html_node(block))
        else:
            raise ValueError(f"unhandled block type: {block_type}")

    return ParentNode("div", result)



