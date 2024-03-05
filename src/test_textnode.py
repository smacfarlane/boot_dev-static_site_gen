import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        node3 = TextNode("This is a test node", "bold")
        node4 = TextNode("This is a text node", "bold", "url.dev")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)

    def test_url(self):
        node = TextNode("Test", "bold")
        url = TextNode("Test", "bold", "test.dev")
        self.assertEqual(node.url, None)
        self.assertEqual(url.url, "test.dev")


    def test_repr(self):
        node = TextNode("This is a bold node", "bold")
        node2 = TextNode("This is an italic node with url", "bold", "test.dev" )
        
        self.assertEqual(f"{node}", "TextNode(This is a bold node, bold, None)")
        self.assertEqual(f"{node2}", "TextNode(This is an italic node with url, bold, test.dev)")



if __name__ == "__main__":
    unittest.main()



