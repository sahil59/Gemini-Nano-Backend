# import requests
# from bs4 import BeautifulSoup

# # List of URLs to crawl
# urls = [
#     'https://valorant-esports.fandom.com/wiki/VALORANT_Esports_Wiki',
#     'https://www.fandom.com/licensing',
#     'http://VLR.gg',
#     'https://valorant.fandom.com/wiki/VALORANT',
#     'https://jqlang.github.io/jq/'
# ]

# def crawl_and_extract(url):
#     try:
#         # Fetch the webpage
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()  # Raise an exception for HTTP errors

#         # Parse the HTML content
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract the title of the page
#         title = soup.title.string if soup.title else "No title"

#         # Extract all paragraphs
#         paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

#         # Extract all links
#         links = [a['href'] for a in soup.find_all('a', href=True)]

#         # Return the extracted information
#         return {
#             'url': url,
#             'title': title,
#             'paragraphs': paragraphs[:5],  # Limit to first 5 paragraphs for brevity
#             'links': links[:10]  # Limit to first 10 links
#         }
#     except Exception as e:
#         print(f"Error crawling {url}: {e}")
#         return None

# # Crawl each URL and collect information
# crawled_data = [crawl_and_extract(url) for url in urls]

# # Print the extracted data
# for data in crawled_data:
#     if data:
#         print(f"\nURL: {data['url']}")
#         print(f"Title: {data['title']}")
#         print("Paragraphs:", data['paragraphs'])
#         print("Links:", data['links'])

######################################################################################################################

# import json
# import re
# from collections import deque

# def is_valid_content(content):
#     """Check if the content contains alphanumeric characters."""
#     return bool(re.search(r'[a-zA-Z0-9]', content))

# def traverse_json_and_extract(node, queue):
#     """
#     Recursively traverse the JSON structure and extract valid `textRun` content.
#     """
#     if isinstance(node, dict):
#         for key, value in node.items():
#             if key == "textRun" and isinstance(value, dict):
#                 # Extract content if it's valid
#                 content = value.get("content", "").strip()
#                 if is_valid_content(content):
#                     queue.append(content)
#             else:
#                 # Recurse into nested dictionaries
#                 traverse_json_and_extract(value, queue)
#     elif isinstance(node, list):
#         for item in node:
#             # Recurse into lists
#             traverse_json_and_extract(item, queue)

# def write_to_text_file(queue, output_file):
#     """
#     Write all extracted content from the queue to a text file.
#     """
#     with open(output_file, "w") as file:
#         for content in queue:
#             file.write(content + "\n")

# # Main function to process JSON and write to a text file
# def process_json_to_plain_text(data, output_file):
#     queue = deque()  # Queue to hold extracted content
#     traverse_json_and_extract(data, queue)  # Extract all valid content
#     write_to_text_file(queue, output_file)  # Write the output to a text file

# # Load JSON and process
# with open("test.json", "r") as file:
#     data = json.load(file)

# process_json_to_plain_text(data, "output.txt")
# print("Text content written to 'output.txt'.")

######################################################################################################################
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

def write_to_text_file(queue, output_file):
    """
    Write formatted content from the queue to a text file.
    """
    
    # with open(output_file, "w") as file:
    c = ""
    for content in queue:
        c += f"{content}" + "\n"
    
    return c

# Main function to process JSON and write to a text file
def process_json_to_preserve_styles(data, output_file):
    queue = deque()
    traverse_json_and_extract(data, queue)  # Traverse the JSON structure
    s = write_to_text_file(queue, output_file)  # Write the output to a text file
    return s

# Load JSON and process
with open("test.json", "r") as file:
    data = json.load(file)

# process_json_to_preserve_styles(data, "output.txt")
print("Styled text content written to 'output.txt'.")

import requests
import json

def extract_sheets(data):
    spreadsheet_id = data.get("spreadsheetId")
    sheets = data.get("sheets", [])
    extracted_data = f"Spreadsheet ID: {spreadsheet_id}\n\n"

    for sheet in sheets:
        sheet_props = sheet.get("properties", {})
        title = sheet_props.get("title", "Untitled")
        sheet_id = sheet_props.get("sheetId", "Unknown")
        row_count = sheet_props.get("gridProperties", {}).get("rowCount", "Unknown")
        col_count = sheet_props.get("gridProperties", {}).get("columnCount", "Unknown")
        frozen_rows = sheet_props.get("gridProperties", {}).get("frozenRowCount", 0)

        extracted_data += f"Sheet Title: {title}\n"
        extracted_data += f"  Sheet ID: {sheet_id}\n"
        extracted_data += f"  Rows: {row_count}\n"
        extracted_data += f"  Columns: {col_count}\n"
        extracted_data += f"  Frozen Rows: {frozen_rows}\n\n"

    return extracted_data.strip()

try:
    token = "ya29.a0AeDClZAREM2azykCs0CTjPadoWJ4E2MZRjUTDd1AnvL6GoVyMT8rtbtYCMaDIrcnPC_FSoXXAG2I1ysoOeAC5YDJzCnlcNH2ug4jvlBQ52Lhz9jegnpwBQgjFpqoMgWRZa7jdR-5XWaLVu0b3ubESObXYD61MICDfeDs3_l15gaCgYKAakSARESFQHGX2Miut64heIT8CAS6LeLZKQLdg0177"
    print(f"Received token: {token}")
    # 1VNFP4FcoD4Wiz2rpKEV0CsGAage_sykNQ6E5bGV7Vrc

    # url = "https://docs.googleapis.com/v1/documents/1idQBzG7L9PJcLRo-dv18yS07pY7vHjYorJ3MJFOHClA"
    # url = "https://www.googleapis.com/drive/v3/files"
    # url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
    url = "https://sheets.googleapis.com/v4/spreadsheets/1VNFP4FcoD4Wiz2rpKEV0CsGAage_sykNQ6E5bGV7Vrc"

    headers = {
        'Authorization': f'Bearer {token}'
    }
    # client.drop_database('test_collection')
    response = requests.request("GET", url, headers=headers)

    # print(response.text)
    data = response.text
    data1_new_1 = json.loads(response.text)

    all_results = []
    a11 = extract_sheets(data1_new_1)
    print(a11)
    # content = data1_new_1["body"]["content"]
    # print(content)
    # text, urls = process_json_to_preserve_styles(content, "output3.txt")
    # print(text)
    # data = text
    # print("URL",urls)
    # print(content)
    # Extract the "messages" list
    # messages = data.get("messages", [])        

    # Access a collection (it will be created if it doesn’t exist)
    # collection = db['test_collection']

    # # Insert a test document
    # test_document = {"rt": "1", "messages1":data}
    # replace_result = collection.replace_one(
    #     {"rt": "1"},  # Filter: Find the document with rt = "1"
    #     test_document,  # Replace with this new document
    #     upsert=True  # Create a new document if none matches
    # )

    # if replace_result.upserted_id:
    #     print(f"New document created with ID: {replace_result.upserted_id}")
    # else:
    #     # Retrieve the `_id` of the updated document
    #     updated_document = collection.find_one({"rt": "1"})
    #     print(f"Updated document ID: {updated_document['_id']}")

    # updated_document = collection.find_one({"rt": "1"})
    # print(f"Inserted document ID: {updated_document['_id']}")
    
    # Connect to Redis
    # r = redis.Redis(host='localhost', db=0)

    print("redis with no problem") 

    # Delete key "a" if it exists
    # r.delete(str(updated_document['_id']))

    # Check if "mongo_id" exists
    # result = r.get(str(updated_document['_id']))
    # print("result is",result)
    # if result is None:
    #     # Set the key "mongo_id" with a value and serialize it using json.dumps
    #     print("setting up key")
    #     r.set(str(updated_document['_id']), json.dumps({"a": 23}))
    #     # Set the key to expire after 1 hour (3600 seconds)
    #     r.expire(str(updated_document['_id']), 36)


    # Decode the result from bytes to string
    # if result is not None:
    #     print("fetching key")
    #     result = result.decode('utf-8')

    # Query the document to verify the connection
    # query_result = collection.find_one({"rt": "1"})
    # print("Retrieved document:", query_result)
    # return jsonify({"message": data}), 200
except Exception as e:
    print(f"Error during OAuth callback: {e}")
    # return jsonify({"error": "Invalid token"}), 400