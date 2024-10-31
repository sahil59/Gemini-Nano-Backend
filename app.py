from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.route('/auth/callback', methods=['POST'])
def exchange_code():
    auth_code = request.get_json().get('code')
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

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return jsonify({"error": "Token exchange failed", "details": response.json()}), response.status_code
    
    return jsonify(response.json())
    # print(response.json())

    # try:
    #     token = response.json()['access_token']
    #     print(f"Received token: {token}")

    #     # url = "https://docs.googleapis.com/v1/documents/1txJzLBGC-UXQpORFRiFNyXlde0HCsD2u4thnznRp8lA"
    #     # url = "https://www.googleapis.com/drive/v3/files"
    #     url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"

    #     headers = {
    #         'Authorization': f'Bearer {token}'
    #     }

    #     response = requests.request("GET", url, headers=headers)

    #     print(response.text)

    #     return jsonify({"message": "Token received successfully"}), 200
    # except Exception as e:
    #     print(f"Error during OAuth callback: {e}")
    #     return jsonify({"error": "Invalid token"}), 400

@app.route('/new-access-token', methods=['POST'])
def refresh_access_token():
    refresh_token = request.get_json().get('refresh_token')
    print(f"Received refresh token: {refresh_token}")

    url = "https://oauth2.googleapis.com/token"

    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return jsonify({"error": "Token exchange failed", "details": response.json()}), response.status_code
    
    print(response.json())
    return jsonify(response.json())

@app.route('/revoke-access-token', methods=['POST'])
def revoke_access_token():
    token = request.get_json().get('access_token')
    print(f"Received access token: {token}")

    url = "https://oauth2.googleapis.com/revoke"
    
    payload = {
        'token': token
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return jsonify({"error": "Token revocation failed", "details": response.json()}), response.status_code

    print(response.json())
    return jsonify(response.json())

# @app.route('/auth/callback', methods=['POST', 'GET'])
# def auth_callback():        
#     try:
#         token = request.get_json().get('access_token')
#         print(f"Received token: {token}")

#         # url = "https://docs.googleapis.com/v1/documents/1txJzLBGC-UXQpORFRiFNyXlde0HCsD2u4thnznRp8lA"
#         # url = "https://www.googleapis.com/drive/v3/files"
#         url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"

#         headers = {
#             'Authorization': f'Bearer {token}'
#         }

#         response = requests.request("GET", url, headers=headers)

#         print(response.text)

#         return jsonify({"message": "Token received successfully"}), 200
#     except Exception as e:
#         print(f"Error during OAuth callback: {e}")
#         return jsonify({"error": "Invalid token"}), 400

if __name__ == '__main__':
    app.run(debug=True)
