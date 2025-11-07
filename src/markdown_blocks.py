from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")


    if len(lines) >= 2 and lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.CODE


    if re.match(r"^(#{1,6})\s+.+$", lines[0]):
        return BlockType.HEADING


    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE


    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    nums = []
    for line in lines:
        m = re.match(r"^(\d+)\.\s+.+$", line)
        if not m:
            nums = []
            break
        nums.append(int(m.group(1)))
    if nums and nums == list(range(1, len(lines) + 1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH