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
import json

app = FastAPI()
client_secrets = json.loads('config/client_secrets.json')

CLIENT_ID =client_secrets['CLIENT_ID']
CLIENT_SECRET =  client_secrets['CLIENT_SECRET']
REDIRECT_URI = client_secrets['REDIRECT_URI']


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
        client_secrets['MONGO_CONNECTION'],
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