import unittest

from blocks import markdown_to_blocks

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
