import re

def extract_markdown_images(input: str) -> list[tuple[str, str]]:
    img_re = r"!\[(.*?)\]\((.*?)\)"

    return re.findall(img_re, input)

def extract_markdown_links(input: str) -> list[tuple[str, str]]:
    link_re = r"\[(.*?)\]\((.*?)\)"

    return re.findall(link_re, input)
