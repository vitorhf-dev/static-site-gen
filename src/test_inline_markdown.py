import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links
from inline_markdown import (
    split_nodes_delimiter,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestInlineMarkdown(unittest.TestCase):
    def test_single_image(self):
        text = "Look ![alt](https://img.com/a.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt", "https://img.com/a.png")]
        )

    def test_single_link(self):
        text = "Go to [site](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("site", "https://example.com")]
        )

    def test_multiple_images(self):
        text = "![a](u1) and ![b](u2)"
        self.assertEqual(
            extract_markdown_images(text),
            [("a", "u1"), ("b", "u2")]
        )

    def test_multiple_links(self):
        text = "[x](u1) + [y](u2)"
        self.assertEqual(
            extract_markdown_links(text),
            [("x", "u1"), ("y", "u2")]
        )

    def test_mixed_images_and_links(self):
        text = "![pic](u) and [txt](v)"
        self.assertEqual(
            extract_markdown_images(text),
            [("pic", "u")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("txt", "v")]
        )

    def test_no_matches(self):
        text = "Nothing here"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_empty_alt_and_text(self):
        text = "![](img.png) and [](url)"
        self.assertEqual(
            extract_markdown_images(text),
            [("", "img.png")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("", "url")]
        )

    def test_negative_lookbehind_blocks_images_in_link_regex(self):
        text = "![img](u) and [notimg](v)"
        self.assertEqual(
            extract_markdown_links(text),
            [("notimg", "v")]
        )

    def test_exclamation_not_followed_by_bracket(self):
        text = "Bang! [ok](u)"
        self.assertEqual(
            extract_markdown_links(text),
            [("ok", "u")]
        )

    def test_double_bang_image(self):
        text = "!![img](u)"
        # Image should still match once; link should not match the image
        self.assertEqual(extract_markdown_images(text), [("img", "u")])
        self.assertEqual(extract_markdown_links(text), [])


if __name__ == "__main__":
    unittest.main()
