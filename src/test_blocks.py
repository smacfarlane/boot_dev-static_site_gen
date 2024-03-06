import unittest

from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from htmlnode import ParentNode, LeafNode

class TestBlocks(unittest.TestCase):
    def test_simple_markdown(self):
        md = '''This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items'''

        blocks = markdown_to_blocks(md)

        self.assertEqual(3, len(blocks))

    def test_leading_newline_block_markdown(self):
        md = '''
* list


* other list

Item'''
        blocks = markdown_to_blocks(md)

        self.assertEqual(3, len(blocks))

    def test_empty_block_markdown(self):
        md = '''



            '''
        blocks = markdown_to_blocks(md)
        self.assertEqual(0, len(blocks))

    def test_headings(self):
        self.assertEqual(BlockType.Heading, block_to_block_type("# words"))
        self.assertEqual(BlockType.Heading, block_to_block_type("## words"))
        self.assertEqual(BlockType.Heading, block_to_block_type("### words"))
        self.assertEqual(BlockType.Heading, block_to_block_type("#### words"))
        self.assertEqual(BlockType.Heading, block_to_block_type("##### words"))
        self.assertEqual(BlockType.Heading, block_to_block_type("###### words"))

    def test_code(self):
        multiline = '''```

        ```'''
        empty = '``````'
        self.assertEqual(BlockType.Code, block_to_block_type(multiline))
        self.assertEqual(BlockType.Code, block_to_block_type(empty))

    def test_quotes(self):
        multiline = '''> Quotes
>
> with a blank line'''
        single = '> text'
        trailing= '''> Quotes
>
> with a blank line
>'''
        
        self.assertEqual(BlockType.Quote, block_to_block_type(multiline))
        self.assertEqual(BlockType.Quote, block_to_block_type(single))
        self.assertEqual(BlockType.Quote, block_to_block_type(trailing))

    def test_unordered_lists(self):
        star_single = "* Item"
        star_nospace = "*"
        star_multi = """* Item
* 
* With blank"""
        
        dash_single = "* Item"
        dash_nospace = "*"
        dash_multi = """* Item
* 
* With blank"""

        mixed = """* Item
- other item
* last item"""

        self.assertEqual(BlockType.UnorderedList, block_to_block_type(star_single))
        self.assertEqual(BlockType.UnorderedList, block_to_block_type(star_nospace))
        self.assertEqual(BlockType.UnorderedList, block_to_block_type(star_multi))
        self.assertEqual(BlockType.UnorderedList, block_to_block_type(dash_single))
        self.assertEqual(BlockType.UnorderedList, block_to_block_type(dash_nospace))
        self.assertEqual(BlockType.UnorderedList, block_to_block_type(dash_multi))
        self.assertEqual(BlockType.UnorderedList, block_to_block_type(mixed))

    def test_ordered_list(self):
        single = "1. item"
        multi = """1. item
2. other
3. last"""

        self.assertEqual(BlockType.OrderedList, block_to_block_type(single))
        self.assertEqual(BlockType.OrderedList, block_to_block_type(multi))

    def test_paragraph(self):
        # Poorly formed headings
        self.assertEqual(BlockType.Paragraph, block_to_block_type("#Heading"))
        self.assertEqual(BlockType.Paragraph, block_to_block_type("####### Heading"))

        # Invalid code blocks
        self.assertEqual(BlockType.Paragraph, block_to_block_type("`````"))
        self.assertEqual(BlockType.Paragraph, block_to_block_type("```code"))

        # Invalid quote blocks
        self.assertEqual(BlockType.Paragraph, block_to_block_type(">\nwords"))

        # Invalid unordered lists
        invalid_uolist = """- Item
other item
- Last Item"""
        self.assertEqual(BlockType.Paragraph, block_to_block_type(invalid_uolist))

        # Invalid ordered lists
        invalid_start_count = "2. Item"
        skipped_count = """1. Item
2. Other
4. Cat"""
        mixed = """1. Item
> quote
"""
        self.assertEqual(BlockType.Paragraph, block_to_block_type(invalid_start_count))
        self.assertEqual(BlockType.Paragraph, block_to_block_type(skipped_count))
        self.assertEqual(BlockType.Paragraph, block_to_block_type(mixed))
        
        
    def test_markdown_to_nodes(self):
        document = """# heading

### heading 

> quote
> quote

1. list
2. item

- list
- list

``` code ```


Cats make the best pets
"""
        expected = ParentNode("div", [
            LeafNode("h1", "heading"),
            LeafNode("h3", "heading"),
            LeafNode("blockquote", " quote\n quote"),
            ParentNode("ol", [
                LeafNode("li", " list"),
                LeafNode("li", " item"),
            ]),
            ParentNode("ul", [
                LeafNode("li", " list"),
                LeafNode("li", " list"),
            ]),
            ParentNode("pre", [LeafNode("code", " code ")]),
            LeafNode("p", "Cats make the best pets")
        ])

        node = markdown_to_html_node(document)

        self.assertEqual(expected, node)

