import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    


if __name__ == "__main__":
    unittest.main()

def test_equal_with_none_url(self):
    n1 = TextNode("hi", TextType.BOLD)
    n2 = TextNode("hi", TextType.BOLD, None)
    self.assertEqual(n1, n2)

def test_not_equal_different_text(self):
    n1 = TextNode("a", TextType.BOLD)
    n2 = TextNode("b", TextType.BOLD)
    self.assertNotEqual(n1, n2)

def test_not_equal_different_type(self):
    n1 = TextNode("same", TextType.BOLD)
    n2 = TextNode("same", TextType.ITALIC)
    self.assertNotEqual(n1, n2)

def test_not_equal_url_mismatch(self):
    n1 = TextNode("t", TextType.LINK, "http://a")
    n2 = TextNode("t", TextType.LINK, None)
    self.assertNotEqual(n1, n2)

def test_equal_all_match_with_url(self):
    n1 = TextNode("t", TextType.LINK, "http://a")
    n2 = TextNode("t", TextType.LINK, "http://a")
    self.assertEqual(n1, n2)


