# python
import unittest
from markdown_blocks import BlockType, block_to_block_type

class TestMarkdownBlocks(unittest.TestCase):
    def test_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_headings_1_to_6(self):
        for line in ["# T", "## T", "### T", "#### T", "##### T", "###### T"]:
            with self.subTest(line=line):
                self.assertEqual(block_to_block_type(line), BlockType.HEADING)

    def test_heading_invalids(self):
        for line in ["####### Too many", "#NoSpace"]:
            with self.subTest(line=line):
                self.assertEqual(block_to_block_type(line), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = ">> nested\n> still quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- a\n- b\n- c"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_requires_space(self):
        block = "-a\n- b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_valid(self):
        block = "1. a\n2. b\n3. c"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalids(self):
        cases = [
            "0. a\n1. b",
            "1. a\n3. b",
            "2. a\n3. b",
            "1.a\n2. b",
            "1. a\n2 b",
        ]
        for block in cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_fallback(self):
        block = "Just a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()