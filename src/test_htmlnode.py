import unittest

from htmlnode import HtmlNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode(None, None, None, {"href": "test.dev", "target": "_blank"})
        noprops = HtmlNode()

        self.assertEqual("", noprops.props_to_html())
        self.assertEqual('href="test.dev" target="_blank"', node.props_to_html())
    
    def test_to_html(self):
        node = HtmlNode()
        self.assertRaises(NotImplementedError, node.to_html)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        invalid = LeafNode(None, None, None)
        no_tag = LeafNode(None, "moocow", {"unused": "tag"})
        p = LeafNode("p", "This is a paragraph of text.")
        a = LeafNode("a", "Click me!", {"href": "https://google.com"})
    
        self.assertRaises(ValueError, invalid.to_html)
        self.assertEqual("moocow", no_tag.to_html())
        self.assertEqual("<p>This is a paragraph of text.</p>", p.to_html())
        self.assertEqual('<a href="https://google.com">Click me!</a>', a.to_html())




if __name__ == "__main__":
    unittest.main()

