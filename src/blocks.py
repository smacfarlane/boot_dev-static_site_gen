def markdown_to_blocks(md: str) -> list[str]:
    split = md.split("\n\n")
    result = []
    for para in split:
        para = para.strip()
        if para != "":
            result.append(para)

    return result
