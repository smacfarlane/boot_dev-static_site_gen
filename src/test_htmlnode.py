import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_boot_dev_example(self):
        node = ParentNode("p", [
                          LeafNode("b", "Bold text"),
                          LeafNode(None, "Normal text"),
                          LeafNode("i", "Italic text"),
                          LeafNode(None, "Normal text"),
        ])

        expected = "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>"
        self.assertEqual(expected, node.to_html())

    def test_nested_parent_node(self):
        node = ParentNode("p", [
                          ParentNode("p", [
                            LeafNode("b", "Bold text")
                          ])])
        expected = "<p><p><b>Bold text</b></p></p>"
        self.assertEqual(expected, node.to_html())

    def test_nested_empty_parenty_node(self):
        node = ParentNode("p", [ParentNode("p", [])])

        expected = "<p><p></p></p>"
        self.assertEqual(expected, node.to_html())

    def test_error_cases(self):
        no_tag = ParentNode(None, [])
        no_children = ParentNode("<p>", None)
        self.assertRaises(ValueError, no_tag.to_html)
        self.assertRaises(ValueError, no_children.to_html)


     # TODO: More test cases


if __name__ == "__main__":
    unittest.main()

