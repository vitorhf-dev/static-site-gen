import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links
from inline_markdown import *
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
    )
    def test_split_links_none(self):
        node = TextNode("no links here", TextType.TEXT)
        out = split_nodes_link([node])
        assert out == [node]

    def test_split_links_multiple(self):
        node = TextNode(
            "a [one](u1) b [two](u2) c",
            TextType.TEXT,
        )
        out = split_nodes_link([node])
        assert out == [
            TextNode("a ", TextType.TEXT),
            TextNode("one", TextType.LINK, "u1"),
            TextNode(" b ", TextType.TEXT),
            TextNode("two", TextType.LINK, "u2"),
            TextNode(" c", TextType.TEXT),
        ]

    def test_split_images_none(self):
        node = TextNode("plain text only", TextType.TEXT)
        out = split_nodes_image([node])
        assert out == [node]

    def test_split_images_multiple(self):
        node = TextNode(
            "pre ![alt1](u1) mid ![alt2](u2) post",
            TextType.TEXT,
        )
        out = split_nodes_image([node])
        assert out == [
            TextNode("pre ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "u1"),
            TextNode(" mid ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "u2"),
            TextNode(" post", TextType.TEXT),
        ]

    def test_passthrough_non_text(self):
        img_node = TextNode("alt", TextType.IMAGE, "u")
        out_links = split_nodes_link([img_node])
        out_images = split_nodes_image([img_node])
        assert out_links == [img_node]
        assert out_images == [img_node]
    
    def test_text_to_textnodes_plain(self):
        text = "This is just plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        assert result == expected
    
    def test_text_to_textnodes_bold_only(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        assert result == expected

    def test_text_to_textnodes_all_types(self):
        text = "**bold** _italic_ `code` ![img](url) [link](site)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "site"),
        ]
        assert result == expected

if __name__ == "__main__":
    unittest.main()
