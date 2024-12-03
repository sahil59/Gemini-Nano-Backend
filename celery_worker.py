from celery import Celery
from pymongo import MongoClient
import os
import json
import requests
import datetime
from celery.utils.log import get_task_logger
from pymongo.server_api import ServerApi
import certifi
from redis import Redis
# Setup logging
logger = get_task_logger(__name__)

# Celery configuration
redis_password = "Xl81F7gDusrIMNygWZbOOF3SOX4OvNzU"


celery_app = Celery(
    'worker',
    broker=f'redis://:Xl81F7gDusrIMNygWZbOOF3SOX4OvNzU@redis-12162.c330.asia-south1-1.gce.redns.redis-cloud.com:12162/0',
    backend=f'redis://:Xl81F7gDusrIMNygWZbOOF3SOX4OvNzU@redis-12162.c330.asia-south1-1.gce.redns.redis-cloud.com:12162/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
# celery -A celery_worker worker --loglevel=info
# MongoDB connection with error handling
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
    logger.info("MongoDB connection successful")
except Exception as e:
    logger.error(f"MongoDB connection failed: {str(e)}")
    raise

def check_user_if_not_exists(email):
    """
    Inserts a new user document if the email does not exist.

    :param email: str, User's email ID.
    :param refresh_token: str, Refresh token for authentication.
    :param documents: dict, Document data to insert.
    :return: str, Operation result message.
    """
    existing_user = collection.find_one({"email": email})
    if existing_user:
        return True
    else:
       False

def insert_user(email, refresh_token, documents):

    new_user = {
        "email": email,
        "refresh_token": refresh_token,
        "documents": documents,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    }
    collection.insert_one(new_user)
    return "New user created successfully."

def fetch_all_documents(email):
    """
    Fetches and returns all elements from the 'documents' field if the email exists.

    :param email: str, User's email ID.
    :return: dict, All key-value pairs from the documents or an appropriate message.
    """
    user = collection.find_one({"email": email})
    if user:
        documents = user.get("documents", {})
        if documents:
            return {"status": "success", "documents": documents}
        else:
            return {"status": "success", "message": "No documents found for this user."}
    else:
        return {"status": "error", "message": "User with the given email not found."}

def add_new_documents(email, new_documents):
    """
    Adds new documents to the 'documents' field of an existing user.

    :param email: str, User's email ID.
    :param new_documents: dict, New documents to add or update.
    :return: str, Operation result message.
    """
    user = collection.find_one({"email": email})
    if user:
        # Merge new documents with the existing documents
        updated_documents = {**user.get("documents", {}), **new_documents}
        update_result = collection.update_one(
            {"email": email},
            {
                "$set": {
                    "documents": updated_documents,  # Update the 'documents' field
                    "updated_at": datetime.datetime.utcnow()  # Update the timestamp
                }
            }
        )
        if update_result.modified_count > 0:
            return "New documents added successfully."
        else:
            return "No changes made to the documents."
    else:
        return "User with the given email not found."

@celery_app.task(name="process_google_data", bind=True, max_retries=3)
def process_google_data(self, email: str, token: str, refresh_token:str, output_file: str):
    """
    Process Google Drive data and store it in MongoDB
    
    Args:
        email (str): User's email
        token (str): Google OAuth token
        output_file (str): Path to output file
    
    Returns:
        dict: Processing result with status and message
    """
    try:
        url = "https://www.googleapis.com/drive/v3/files"
        headers = {'Authorization': f'Bearer {token}'}
        all_results = {}
        
        if(check_user_if_not_exists(email)):
            docs = fetch_all_documents(email)        
            doc_exist = False
            params = {'orderBy':'createdTime'}
            response = requests.get(url, headers=headers, params=params ,timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            
            data = response.json()
            # all_results.extend(data.get('files', []))
            f1 = data.get('files', [])
            for i in f1:
                if docs["documents"] not in docs:
                    all_results[f'{i["name"]}'] = [i["id"],i["mimeType"]]
                else:
                    doc_exist = True
                    break
            
            # Pagination handling
            page_count = 0
            next_page_token = data.get('nextPageToken')
            
            while next_page_token and doc_exist:  # Limit to prevent infinite loops
                params = {'pageToken': next_page_token,'orderBy':'createdTime'}
                logger.info(f"Fetching page {page_count + 2}")
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                f1 = data.get('files', [])

                for i in f1:
                    if docs["documents"] not in docs:
                        all_results[f'{i["name"]}'] = [i["id"],i["mimeType"]]
                    else:
                        doc_exist = True
                        break  
                next_page_token = data.get('nextPageToken')
                page_count += 1

            if(len(all_results)!=0):
                add_new_documents(email, all_results)

            docs = fetch_all_documents(email)

            return {
                "status": "success",
                "message": "Succesfully retrieved the docs",
                "total_files": len(docs["documents"]),
                "docs":docs["documents"]
            }

        else:
            # Initial request
            params = {'orderBy':'createdTime'}
            response = requests.get(url, headers=headers, params=params ,timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            
            data = response.json()
            # all_results.extend(data.get('files', []))
            f1 = data.get('files', [])
            logger.info(f"files:{f1}")
            for i in f1:
                all_results[f'{i["name"]}'] = [i["id"],i["mimeType"]]
            
            # Pagination handling
            page_count = 0
            next_page_token = data.get('nextPageToken')
            
            while next_page_token:  # Limit to prevent infinite loops
                params = {'pageToken': next_page_token,'orderBy':'createdTime'}
                logger.info(f"Fetching page {page_count + 2}")
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                f1 = data.get('files', [])

                for i in f1:
                    all_results[f'{i["name"]}'] = [i["id"],i["mimeType"]]
                next_page_token = data.get('nextPageToken')
                page_count += 1

            # MongoDB operations
            # test_document = {
            #     "email": email,
            #     "messages1": all_results,
            #     "total_files": len(all_results),
            #     # "last_updated": datetime.utcnow()
            # }
            
            # replace_result = collection.replace_one(
            #     {"email": email},
            #     test_document,
            #     upsert=True
            # )

            # # File operations
            # try:
            #     with open(output_file, 'w') as f:
            #         for result in all_results:
            #             f.write(json.dumps(result) + '\n')
            # except IOError as e:
            #     logger.error(f"File write error: {str(e)}")
            #     # Continue execution even if file write fails
            
            # # Prepare response
            # if replace_result.upserted_id:
            #     message = f"New document created with ID: {replace_result.upserted_id}"
            #     logger.info(message)
            # else:
            #     updated_document = collection.find_one({"email": email})
            #     if updated_document:
            #         message = f"Updated document ID: {updated_document['_id']}"
            #         logger.info(message)
            #     else:
            #         message = "Document not found after update"
            #         logger.warning(message)
            
            insert_user(email, refresh_token, all_results)
            return {
                "status": "success",
                "message": "Succesfully added the docs",
                "total_files": len(all_results),
                "pages_processed": page_count + 1
            }

    except requests.exceptions.RequestException as e:
        error_msg = f"Google API request failed: {str(e)}"
        logger.error(error_msg)
        # Retry the task if it's a temporary failure
        if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)):
            try:
                self.retry(countdown=60, exc=e)  # Retry after 1 minute
            except self.MaxRetriesExceededError:
                return {"status": "error", "message": f"Max retries exceeded: {error_msg}"}
        return {"status": "error", "message": error_msg}
        
    except Exception as e:
        error_msg = f"Task failed: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}