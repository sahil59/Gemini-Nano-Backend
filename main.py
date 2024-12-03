# # from flask import Flask, request, jsonify
# from datetime import timedelta
# from flask_cors import CORS
# import os
# from dotenv import load_dotenv
# import requests
# import pymongo
# import json
# import redis
# import json
# from celery import Celery
# from celery_app import make_celery

# # app = Flask(__name__)
# from fastapi import FastAPI
# app = FastAPI()

# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# # Configure Celery

# load_dotenv()
# # myclient = pymongo.MongoClient("mongodb://localhost:27017/")


# #########################################

# # from flask import Flask, request, jsonify
# # from datetime import timedelta
# # from flask_cors import CORS
# # import os
# # from dotenv import load_dotenv
# # import requests
# # import redis
# # import json
# from celery_app import make_celery


# # Celery configuration
# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379/0',
#     CELERY_RESULT_BACKEND='redis://localhost:6379/0',
#     CELERY_ACCEPT_CONTENT=['json'],
#     CELERY_TASK_SERIALIZER='json',
#     CELERY_RESULT_SERIALIZER='json',
#     CELERY_TIMEZONE='UTC'
# )

# # Initialize Celery
# celery = make_celery(app)

# # Define a Celery Task
# @celery.task
# def fetch_google_data(token, email,output_file):
#     url = "https://www.googleapis.com/drive/v3/files"
#     headers = {'Authorization': f'Bearer {token}'}
#     print(headers)
#     all_results = []
#     collection = db['test_collection']

    
#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             print(f"Error: {response.status_code}, {response.text}")
#             return

#         data = response.json()
#         all_results.extend(data.get('files', []))  # Adjust 'files' to match the API response key

#         # Loop through pages
#         next_page_token = data.get('nextPageToken')
#         i = 0
#         while next_page_token:
#             params = {'pageToken': next_page_token}
#             # print(f"Hii{i}, NextPage:{params['pageToken']}")
#             i+=1
#             # print(i)
#             response = requests.get(url, headers=headers, params=params)
#             if response.status_code != 200:
#                 print(f"Error: {response.status_code}, {response.text}")
#                 break
#             data = response.json()
#             all_results.extend(data.get('files', []))
#             next_page_token = data.get('nextPageToken')

#         # Insert a test document

#         test_document = {"email": email, "messages1": all_results}
#         replace_result = collection.replace_one(
#             {"email": email},  # Filter: Find document with matching email
#             test_document,     # Replace with this new document
#             upsert=True       # Create a new document if none matches
#         )

#         if replace_result.upserted_id:
#             print(f"New document created with ID: {replace_result.upserted_id}")
#         else:
#             # Retrieve the `_id` of the updated document using the email
#             updated_document = collection.find_one({"email": email})  # Changed query to use email
#             if updated_document:  # Add null check
#                 print(f"Updated document ID: {updated_document['_id']}")
#             else:
#                 print("Document not found")

#         # updated_document = collection.find_one({"rt": "1"})
#         # print(f"Inserted document ID: {updated_document['_id']}")

#         # Write results to file
#         with open(output_file, 'w') as f:
#             for result in all_results:
#                 f.write(json.dumps(result) + '\n')

#         print(f"Total files fetched: {len(all_results)}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Route to Trigger the Task
# @app.route('/fetch-data', methods=['POST'])
# def fetch_data():
#     token = request.json.get('access_token')
#     email = request.json.get('email')
#     if not token:
#         return jsonify({"error": "Token is required"}), 400

#     # Trigger the Celery task
#     output_file = 'output_list.txt'
#     fetch_google_data.apply_async(args=[token, email,output_file])

#     return jsonify({"message": "Data fetching started in the background"}), 202

# #########################################


# # mydb = myclient["mydatabase"]
# # CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_ID ="152620060314-7fven1dprv3tsjctqt8ehh3btl119c9n.apps.googleusercontent.com"
# CLIENT_SECRET =  "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"#os.getenv("CLIENT_SECRET")
# REDIRECT_URI = "http://localhost:5000"#os.getenv("REDIRECT_URI")


# def extract_text_and_urls(content_list):
#     extracted_text = []
#     extracted_urls = []

#     for item in content_list:
#         if 'paragraph' in item:
#             elements = item['paragraph'].get('elements', [])
#             for element in elements:
#                 # Extract text
#                 text_run = element.get('textRun', {})
#                 content = text_run.get('content', '').strip()
#                 if content:
#                     extracted_text.append(content)
                
#                 # Extract URLs
#                 text_style = text_run.get('textStyle', {})
#                 link = text_style.get('link', {}).get('url')
#                 if link:
#                     extracted_urls.append(link)

#     return extracted_text, extracted_urls

# from collections import deque

# def extract_text_and_urls_iterative(root):
#     extracted_text = []
#     extracted_urls = []
#     queue = deque([root])  # Initialize a queue with the root node

#     while queue:
#         node = queue.popleft()  # Get the next node to process

#         # If the node is a dictionary, process its keys
#         if isinstance(node, dict):
#             for key, value in node.items():
#                 if key == "textRun" and isinstance(value, dict):
#                     # Extract text
#                     content = value.get('content', '').strip()
#                     if content:
#                         extracted_text.append(content)

#                     # Extract URL
#                     text_style = value.get('textStyle', {})
#                     link = text_style.get('link', {}).get('url')
#                     if link:
#                         extracted_urls.append(link)
#                 else:
#                     # Add other dictionary entries to the queue
#                     queue.append(value)

#         # If the node is a list, add all its elements to the queue
#         elif isinstance(node, list):
#             queue.extend(node)

#     return extracted_text, extracted_urls

# @app.route('/auth/callback', methods=['POST'])
# def exchange_code():
#     # auth_code = request.get_json().get('code')
#     # print(f"Received auth code: {auth_code}")
#     # print(f"Client ID: {CLIENT_ID}, Client Secret: {CLIENT_SECRET}, Redirect URI: {REDIRECT_URI}")

#     # url = "https://oauth2.googleapis.com/token"

#     # payload = {
#     #     'client_id': CLIENT_ID,
#     #     'client_secret': CLIENT_SECRET,
#     #     'code': auth_code,
#     #     'grant_type': 'authorization_code',
#     #     'redirect_uri': REDIRECT_URI
#     # }

#     # headers = {
#     #     'Content-Type': 'application/x-www-form-urlencoded'
#     # }

#     # response = requests.request("POST", url, headers=headers, data=payload)
#     # print("respinse",response)
#     # if response.status_code != 200:
#     #     print(f"Error: {response.status_code}, Response: {response.text}")
#     #     return jsonify({"error": "Token exchange failed", "details": response.json()}), response.status_code
    
#     # return jsonify(response.json())
#     # print(response.json())

#     try:
#         token = request.get_json()['access_token']
#         print(f"Received token: {token}")
#         # 1VNFP4FcoD4Wiz2rpKEV0CsGAage_sykNQ6E5bGV7Vrc

#         url = "https://docs.googleapis.com/v1/documents/1idQBzG7L9PJcLRo-dv18yS07pY7vHjYorJ3MJFOHClA"
#         # url = "https://www.googleapis.com/drive/v3/files"
#         # url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
#         # url = "https://sheets.googleapis.com/v4/spreadsheets/1VNFP4FcoD4Wiz2rpKEV0CsGAage_sykNQ6E5bGV7Vrc"

#         headers = {
#             'Authorization': f'Bearer {token}'
#         }
#         client.drop_database('test_collection')
#         response = requests.request("GET", url, headers=headers)

#         print(response.text)
#         data = response.text
#         data1_new_1 = json.loads(response.text)

#         all_results = []

#         # Start the loop with the initial URL
#         # next_page_token = data1_new_1['nextPageToken']
#         # i = 0
#         # while True:
#         #     # Add nextPageToken as a query parameter if it exists
#         #     params = {}
#         #     if next_page_token:
#         #         params['pageToken'] = next_page_token

#         #     # Make the GET request
#         #     response = requests.get(url, headers=headers, params=params)
#         #     print(f"hiiii {i} params, {params}")
#         #     i+=1
#         #     # Check for HTTP errors
#         #     if response.status_code != 200:
#         #         print(f"Error: {response.status_code}, {response.text}")
#         #         break

#         #     # Parse the JSON response
#         #     data = response.json()
#         #     all_results.extend(data.get('files', []))  # Adjust 'files' to the correct key for the data

#         #     # Fetch the nextPageToken
#         #     next_page_token = data.get('nextPageToken')

#         #     # Break the loop if no nextPageToken is present
#         #     if  next_page_token=="":
#         #         break

#         # # Write all results to a text file
#         # with open('output_list.txt', 'w') as f:
#         #     for result in all_results:
#         #         f.write(json.dumps(result) + '\n')  # Write each result as a JSON string, one per line

#         # print(f"Total files fetched: {len(all_results)}")
#         # print("Results written to output_list.txt")
#         # print(type(data1_new_1))
#         # with open('data.json', 'w') as json_file:
#         #     json.dump(json.loads(response.text), json_file, indent=4)
        
#         # with open('data.json', 'r') as json_file:
#         #     data1 = json.load(json_file)
        
#         content = data1_new_1["body"]["content"]
#         text, urls = extract_text_and_urls(content)
#         # data = text
#         # print("URL",urls)
#         # print(content)
#         # Extract the "messages" list
#         # messages = data.get("messages", [])        

#         # Access a collection (it will be created if it doesn’t exist)
#         collection = db['test_collection']

#         # Insert a test document
#         test_document = {"rt": "1", "messages1":data}
#         replace_result = collection.replace_one(
#             {"rt": "1"},  # Filter: Find the document with rt = "1"
#             test_document,  # Replace with this new document
#             upsert=True  # Create a new document if none matches
#         )

#         if replace_result.upserted_id:
#             print(f"New document created with ID: {replace_result.upserted_id}")
#         else:
#             # Retrieve the `_id` of the updated document
#             updated_document = collection.find_one({"rt": "1"})
#             print(f"Updated document ID: {updated_document['_id']}")

#         updated_document = collection.find_one({"rt": "1"})
#         print(f"Inserted document ID: {updated_document['_id']}")
        
#         # Connect to Redis
#         r = redis.Redis(host='localhost', db=0)

#         print("redis with no problem") 

#         # Delete key "a" if it exists
#         # r.delete(str(updated_document['_id']))

#         # Check if "mongo_id" exists
#         result = r.get(str(updated_document['_id']))
#         print("result is",result)
#         if result is None:
#             # Set the key "mongo_id" with a value and serialize it using json.dumps
#             print("setting up key")
#             r.set(str(updated_document['_id']), json.dumps({"a": 23}))
#             # Set the key to expire after 1 hour (3600 seconds)
#             r.expire(str(updated_document['_id']), 36)


#         # Decode the result from bytes to string
#         if result is not None:
#             print("fetching key")
#             result = result.decode('utf-8')

#         # Query the document to verify the connection
#         # query_result = collection.find_one({"rt": "1"})
#         # print("Retrieved document:", query_result)
#         return jsonify({"message": data}), 200
#     except Exception as e:
#         print(f"Error during OAuth callback: {e}")
#         return jsonify({"error": "Invalid token"}), 400

# @app.route('/pdf-download',methods = ['POST'])
# def pdf_download():
#     try:
#         token = request.get_json()['access_token']
#         file_id = "10imS401kHcU20PIUC91XMH5rDb1przCy"

#         # Step 2: Retrieve file metadata
#         metadata_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=name,mimeType"
#         metadata_headers = {'Authorization': f'Bearer {token}'}
#         metadata_response = requests.get(metadata_url, headers=metadata_headers)

#         if metadata_response.status_code != 200:
#             print(f"Error fetching metadata: {metadata_response.text}")
#             return jsonify({"error": "Failed to retrieve file metadata"}), 400

#         metadata = metadata_response.json()
#         file_name = metadata.get('name')
#         mime_type = metadata.get('mimeType')

#         print(f"File Name: {file_name}, MIME Type: {mime_type}")
#         print("Step 2: File metadata retrieved successfully")

#         # Step 3: Download the file
#         drive_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
#         drive_headers = {'Authorization': f'Bearer {token}'}
        
#         drive_response = requests.get(drive_url, headers=drive_headers, stream=True)

#         if drive_response.status_code == 200:
#             content_type = drive_response.headers.get('Content-Type', '')
            
#             if content_type != mime_type:
#                 print(f"Error: Mismatch in content type. Expected: {mime_type}, Got: {content_type}")
#                 return jsonify({"error": "File download failed due to content type mismatch"}), 400
            
#             download_progress = 0
#             file_size = 0
#             file_path = file_name

#             with open(file_path, 'wb') as f:
#                 for chunk in drive_response.iter_content(chunk_size=1024):
#                     if chunk:
#                         f.write(chunk)
#                         download_progress += len(chunk)
#                         if not file_size:
#                             file_size = int(drive_response.headers.get('Content-Length', 0))
#                         if file_size > 0:
#                             print(f"Downloaded: {download_progress}/{file_size} bytes ({(download_progress / file_size) * 100:.2f}%)")

#             print(f"File downloaded successfully: {file_path}")
#             return jsonify({"message": "File downloaded successfully", "file_path": file_path}), 200
#         else:
#             print(f"Error downloading file: {drive_response.text}")
#             return jsonify({"error": "Failed to download file"}), 400
#     except Exception as e:
#         print(f"Error during OAuth callback: {e}")
#         return jsonify({"error": "Invalid token"}), 400

# @app.route('/new-access-token', methods=['POST'])
# def refresh_access_token():
#     refresh_token = request.get_json().get('refresh_token')
#     print(f"Received refresh token: {refresh_token}")

#     url = "https://oauth2.googleapis.com/token"

#     payload = {
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET,
#         'refresh_token': refresh_token,
#         'grant_type': 'refresh_token'
#     }

#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)

#     if response.status_code != 200:
#         print(f"Error: {response.status_code}, Response: {response.text}")
#         return jsonify({"error": "Token exchange failed", "details": response.json()}), response.status_code
    
#     print(response.json())
#     return jsonify(response.json())

# @app.route('/revoke-access-token', methods=['POST'])
# def revoke_access_token():
#     token = request.get_json().get('access_token')
#     print(f"Received access token: {token}")

#     url = "https://oauth2.googleapis.com/revoke"
    
#     payload = {
#         'token': token
#     }
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)

#     if response.status_code != 200:
#         print(f"Error: {response.status_code}, Response: {response.text}")
#         return jsonify({"error": "Token revocation failed", "details": response.json()}), response.status_code

#     print(response.json())
#     return jsonify(response.json())


# from pymongo import MongoClient

# # Create a connection to MongoDB server running locally on port 27017
# client = MongoClient("mongodb://localhost:27017/")
# db = client['test_database']

# # @app.route('/auth/callback1', methods=['POST'])
# # def auth_callback():        
# #     try:
# #         token = request.get_json().get('access_token')
# #         print(f"Received token: {token}")

# #         # url = "https://docs.googleapis.com/v1/documents/1txJzLBGC-UXQpORFRiFNyXlde0HCsD2u4thnznRp8lA"
# #         # url = "https://www.googleapis.com/drive/v3/files"
# #         url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"

# #         headers = {
# #             'Authorization': f'Bearer {token}'
# #         }

# #         response = requests.request("GET", url, headers=headers)

# #         # print(response.text)

       

# #         return jsonify({"message": "Token received successfully"}), 200
# #     except Exception as e:
# #         print(f"Error during OAuth callback: {e}")
# #         return jsonify({"error": "Invalid token"}), 400



# # Access a database (it will be created if it doesn’t exist)
# # db = client['test_database']

# # # Access a collection (it will be created if it doesn’t exist)
# # collection = db['test_collection']

# # # Insert a test document
# # test_document = {"name": "Alice", "age": 30, "city": "Wonderland"}
# # insert_result = collection.insert_one(test_document)
# # print(f"Inserted document ID: {insert_result.inserted_id}")

# # Query the document to verify the connection
# collection = db['test_collection']

# query_result = collection.find_one({"email": "pranav.singh@gmail.com"})
# print("Retrieved document:", query_result)


# if __name__ == '__main__':
#     app.run(debug=True)



# # Compare with the expected JSON string



# # print(r.keys())


##################################################################################

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from typing import List, Any
from celery_worker import process_google_data
import httpx
from pymongo.server_api import ServerApi
import certifi
from pymongo import MongoClient
from functools import partial
from controllers.index import handle_docs
from controllers.index import handle_sheets
from controllers.index import handle_pdf

app = FastAPI()

# CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_ID ="152620060314-7fven1dprv3tsjctqt8ehh3btl119c9n.apps.googleusercontent.com"
CLIENT_SECRET =  "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"#os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000"#os.getenv("REDIRECT_URI")


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GoogleData(BaseModel):
    email: str 
    access_token: str
    refresh_token: str

try:
    client = MongoClient(
        "mongodb+srv://pranavsingh8108:Pranav7777@cluster0.rdvs2.mongodb.net/",
        server_api=ServerApi('1'),
        tls=True,
        tlsCAFile=certifi.where()  # This is the key addition for macOS
    )
    # Verify connection
    client.server_info()
    db = client['test_database']
    collection = db['test_collection']
except Exception as e:
    raise

@app.post("/process-data")
async def create_task(request: GoogleData):
    try:
        # Trigger Celery task
        existing_user = collection.find_one({"email": request.email})

        if existing_user:
            documents = existing_user.get("documents", None)  # Use .get() to safely retrieve 'documents' key
            if documents:
                print("Documents:", documents)
            else:
                print("No documents key found or it is empty.")
        else:
            print("User does not exist.")
        task = process_google_data.delay(request.email, request.access_token, request.refresh_token,'output_list.txt')
        return {
            "documents": documents,
            "message": "Task started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/task-status/{task_id}")
# async def get_task_status(task_id: str):
#     task = process_google_data.AsyncResult(task_id)
#     if task.ready():
#         return {
#             "status": "completed",
#             "result": task.result
#         }
#     return {
#         "status": "processing"
#     }

class TokenRefreshRequest(BaseModel):
    refresh_token: str

# Response model
class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    # scope: Optional[str] = None
    token_type: str

@app.post('/new-access-token', response_model=TokenResponse)
async def refresh_access_token(request: TokenRefreshRequest):
    try:
        print(request)
        url = "https://oauth2.googleapis.com/token"
        
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': request.refresh_token,
            'grant_type': 'refresh_token'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload)
        print(response)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail={
                    "error": "Token exchange failed",
                    "details": response.json()
                }
            )
        
        return response.json()

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to communicate with Google OAuth server",
                "details": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "details": str(e)
            }
        )

class AuthCodeRequest(BaseModel):
    code: str


@app.post("/auth/callback")
async def exchange_code(auth_code_request: AuthCodeRequest):
    auth_code = auth_code_request.code
    print(f"Received auth code: {auth_code}")
    print(f"Client ID: {CLIENT_ID}, Client Secret: {CLIENT_SECRET}, Redirect URI: {REDIRECT_URI}")

    url = "https://oauth2.googleapis.com/token"

    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        raise HTTPException(status_code=response.status_code, detail={
            "error": "Token exchange failed",
            "details": response.json()
        })

    return {"message": "Token exchange successful", "data": response.json()}


"""
We will take the lists of docs and query to pocess for accordingly using the tools and everything else to work for, 
if any single doc required for sumarization and anything else we will load the important docs and provide the docs context and part through 
the LLM and then provide that docs for summarization and translation. We can also use write api to generate ideas and rpompts for further instructions of the underlying docs
"""

class QueryRequest(BaseModel):
    query: str
    docs: List[str]
    email: str
    token: str

@app.post('/query')
async def query_docs(request: QueryRequest):
    """
    Endpoint to process a query against a list of documents.
    """
    try:
        # Loop over the documents
        existing_user = collection.find_one({"email": request.email})

        if existing_user:
            documents = existing_user.get("documents", None)  # Use .get() to safely retrieve 'documents' key
            if documents:
                print("Documents:", documents)
            else:
                print("No documents key found or it is empty.")
        else:
            print("User does not exist.")
        
        for i,doc in enumerate(request.docs):
            switch = {
                "application/pdf": partial(handle_pdf, request.token, documents[doc][0]),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": partial(handle_sheets, request.token, documents[doc][0]),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": partial(handle_docs, request.tokentoken, documents[doc][0]),
            }

            result = switch.get(documents[doc][1], lambda: "Unsupported mimetype")()
        
            # Append the results from each document
            if result != "Unsupported mimetype":
                texts += f"Results from Document {i + 1}:\n{result}\n\n"
            else:
                texts += f"Document {i + 1} has unsupported MIME type.\n"
        # Placeholder for query processing
        print(f"Query: {request.query}")
        
        return {"message": "Documents processed successfully", "query": request.query, "num_docs": len(request.docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#uvicorn main:app --reload