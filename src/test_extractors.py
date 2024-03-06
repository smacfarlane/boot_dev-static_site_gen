import unittest

from extractors import *

class TestExtractors(unittest.TestCase):
    def test_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        expected = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"), 
            ("another", "https://i.imgur.com/dfsdkjfd.png")
        ]

        self.assertEqual(expected, extract_markdown_images(text))

    def test_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [
            ("link", "https://www.example.com"), 
            ("another", "https://www.example.com/another")
        ]

        self.assertEqual(expected, extract_markdown_links(text))
