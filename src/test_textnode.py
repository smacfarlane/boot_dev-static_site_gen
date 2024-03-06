import unittest

from htmlnode import LeafNode
from textnode import * 

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

    def test_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("sample text", "text"))

        self.assertIsInstance(node, LeafNode)
        self.assertEqual("sample text", node.value)
        self.assertIsNone(node.tag)

    def test_bold_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("sample text", "bold"))

        self.assertIsInstance(node, LeafNode)
        self.assertEqual("sample text", node.value)
        self.assertEqual("b", node.tag)

    def test_link_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("sample text", "link", "https://test.dev"))

        self.assertIsInstance(node, LeafNode)
        self.assertEqual("sample text", node.value)
        self.assertEqual("a", node.tag)
        self.assertDictEqual({"href": "https://test.dev"}, node.props)

    def test_image_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("sample text", "image", "https://test.dev"))

        self.assertIsInstance(node, LeafNode)
        self.assertIsNone(node.value)
        self.assertEqual("img", node.tag)
        self.assertDictEqual({"alt": "sample text", "src": "https://test.dev"}, node.props)

    def test_invalid_text_node_to_html_node(self):
        node = TextNode("sample text", "cats", "https://cats.cats")

        self.assertRaises(InvalidTextTypeError, text_node_to_html_node, node)

    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        self.assertListEqual(
                [
                    TextNode("This is text with a ", "text"),
                    TextNode("code block", "code"),
                    TextNode(" word", "text")
                ], 
                new_nodes)

    def test_split_italic_block(self):
        node = TextNode("This is text with a *italic block* word", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")

        self.assertListEqual(
                [
                    TextNode("This is text with a ", "text"),
                    TextNode("italic block", "italic"),
                    TextNode(" word", "text")
                ], 
                new_nodes)

    def test_split_bold_block(self):
        node = TextNode("This is text with a **bold block** word", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")

        self.assertListEqual(
                [
                    TextNode("This is text with a ", "text"),
                    TextNode("bold block", "bold"),
                    TextNode(" word", "text")
                ], 
                new_nodes)

    def test_split_bold_with_italic_block(self):
        node = TextNode("This is text with a **bold *italic* block** word", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")

        self.assertListEqual(
                [
                    TextNode("This is text with a ", "text"),
                    TextNode("bold *italic* block", "bold"),
                    TextNode(" word", "text")
                ], 
                new_nodes)

    def test_unclosed_delimter(self):
        node = TextNode("This is text with a *italic block word", "italic")
        
        self.assertRaises(InvalidMarkdownError, split_nodes_delimiter, node)

if __name__ == "__main__":
    unittest.main()



