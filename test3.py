# from PyPDF2 import PdfReader
# import pytesseract
# from PIL import Image
# from pdf2image import convert_from_path

# # Path to your PDF file
# pdf_path = "DVD Exp 4.pdf"

# # Function to extract text from PDF pages
# def extract_text_from_pdf(pdf_path):
#     # First attempt with PyPDF2 for text-based PDFs
#     reader = PdfReader(pdf_path)
#     text = ""
#     for page in reader.pages:
#         text1 = page.extract_text()
#         text += text1 
#         # If no text found, use pytesseract for OCR on images
#         if not text1.strip():
#             images = convert_from_path(pdf_path)
#             for img in images:
#                 text += pytesseract.image_to_string(img)
    
#     return text

# # Extract and display the text
# extracted_text = extract_text_from_pdf(pdf_path)
# print("________________________________")
# print(extracted_text)
# print("________________________________")


############################################################################################
import requests
import json

try:
    token = "ya29.a0AeDClZAREM2azykCs0CTjPadoWJ4E2MZRjUTDd1AnvL6GoVyMT8rtbtYCMaDIrcnPC_FSoXXAG2I1ysoOeAC5YDJzCnlcNH2ug4jvlBQ52Lhz9jegnpwBQgjFpqoMgWRZa7jdR-5XWaLVu0b3ubESObXYD61MICDfeDs3_l15gaCgYKAakSARESFQHGX2Miut64heIT8CAS6LeLZKQLdg0177"
    print(f"Received token: {token}")
    # 1VNFP4FcoD4Wiz2rpKEV0CsGAage_sykNQ6E5bGV7Vrc

    url = "https://docs.googleapis.com/v1/documents/1idQBzG7L9PJcLRo-dv18yS07pY7vHjYorJ3MJFOHClA"
    # url = "https://www.googleapis.com/drive/v3/files"
    # url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
    # url = "https://sheets.googleapis.com/v4/spreadsheets/1VNFP4FcoD4Wiz2rpKEV0CsGAage_sykNQ6E5bGV7Vrc"

    headers = {
        'Authorization': f'Bearer {token}'
    }
    # client.drop_database('test_collection')
    response = requests.request("GET", url, headers=headers)

    # print(response.text)
    data = response.text
    data1_new_1 = json.loads(response.text)

    all_results = []

    
    content = data1_new_1["body"]["content"]
    print(content)
    # text, urls = extract_text_and_urls(content)
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