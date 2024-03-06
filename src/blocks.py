from enum import Enum
import re

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
