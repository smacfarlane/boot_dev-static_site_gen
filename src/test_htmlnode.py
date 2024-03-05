import unittest

from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode(None, None, None, {"href": "test.dev", "target": "_blank"})
        noprops = HtmlNode()

        self.assertEqual("", noprops.props_to_html())
        self.assertEqual('href="test.dev" target="_blank"', node.props_to_html())
    
    def test_to_html(self):
        node = HtmlNode()
        self.assertRaises(NotImplementedError, node.to_html)



if __name__ == "__main__":
    unittest.main()
