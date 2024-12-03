import json
import re
from collections import deque

def is_valid_content(content):
    """Check if the content contains alphanumeric characters."""
    return bool(re.search(r'[a-zA-Z0-9]', content))

def format_text(content, text_style):
    """Apply textStyle attributes like bold, italic, and font size."""
    if not content:
        return content

    # Apply bold
    if text_style.get("bold"):
        content = f"**{content}**"
    # Apply italic
    if text_style.get("italic"):
        content = f"*{content}*"
    # Add font size
    font_size = text_style.get("fontSize")
    if font_size:
        content = f"[Font Size: {font_size}] {content}"

    return content

def format_paragraph(content, paragraph_style):
    """Format paragraphs based on paragraphStyle, like heading levels or alignment."""
    if not content:
        return content

    # Handle headings
    heading = paragraph_style.get("namedStyleType")
    if heading:
        if heading == "HEADING_1":
            content = f"# {content}"
        elif heading == "HEADING_2":
            content = f"## {content}"
        elif heading == "HEADING_3":
            content = f"### {content}"

    # Handle alignment
    alignment = paragraph_style.get("alignment")
    if alignment == "CENTER":
        content = f"<center>{content}</center>"
    elif alignment == "RIGHT":
        content = f"<div style='text-align:right;'>{content}</div>"

    return content

def traverse_json_and_extract(node, queue, path=None):
    """
    Recursively traverse the JSON tree and extract `textRun` content with styles.
    """
    if path is None:
        path = []

    if isinstance(node, dict):
        for key, value in node.items():
            if key == "paragraph" and isinstance(value, dict):
                # Process paragraph elements and styles
                paragraph_style = value.get("paragraphStyle", {})
                elements = value.get("elements", [])
                for element in elements:
                    if "textRun" in element:
                        # Extract textRun content with textStyle
                        text_run = element["textRun"]
                        content = text_run.get("content", "").strip()
                        text_style = text_run.get("textStyle", {})
                        if is_valid_content(content):
                            formatted_text = format_text(content, text_style)
                            formatted_text = format_paragraph(formatted_text, paragraph_style)
                            queue.append(formatted_text)
            else:
                # Recurse into nested dictionaries
                traverse_json_and_extract(value, queue)
    elif isinstance(node, list):
        for item in node:
            # Recurse into lists
            traverse_json_and_extract(item, queue)

def write_to_text_file(queue):
    """
    Write formatted content from the queue to a text file.
    """
    
    # with open(output_file, "w") as file:
    c = ""
    for content in queue:
        c += f"{content}" + "\n"
    
    return c

# Main function to process JSON and write to a text file
def process_json_to_preserve_styles(data):
    queue = deque()
    traverse_json_and_extract(data, queue)  # Traverse the JSON structure
    s = write_to_text_file(queue)  # Write the output to a text file
    return s