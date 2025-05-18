from marko.block import FencedCode
from typing import List
import logging

logger = logging.getLogger(__name__)

def extract_code_block(src: str) -> List[str]:
    """
    Extract the first code block from markdown source
    """
    markdown = marko.parse(src)
    def search_for_code(element, code_blocks):
        if isinstance(element, FencedCode):
            code_blocks.append(element.children[0].children)
        elif hasattr(element, "children"):
            for child in element.children:
                search_for_code(child, code_blocks)
    code_blocks = []
    search_for_code(markdown, code_blocks)
    if len(code_blocks) > 1:
        logger.warning("Too many code blocks")
    if len(code_blocks) >= 1:
        return code_blocks[0]
    return src

def swap_sections(src: str) -> str:
    """
    Swap the Working Storage and Linkage Sections
    """
    working_storage, linkage, procedure, begin = [], [], [], []
    current_section = begin

    for line in src.split("\n"):
        stripped_line = line.strip().upper()
        if stripped_line.startswith("WORKING-STORAGE SECTION."):
            current_section = working_storage
        elif stripped_line.startswith("LINKAGE SECTION."):
            current_section = linkage
        elif stripped_line.startswith("PROCEDURE DIVISION"):
            current_section = procedure
            line = "       PROCEDURE DIVISION USING LINKED-ITEMS."
        current_section.append(line)

    return "\n".join(begin + working_storage + linkage + procedure)