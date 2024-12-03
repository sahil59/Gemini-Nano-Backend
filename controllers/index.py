import requests
import os
import redis
import json
from helpers.pdf_helper import extract_text_from_pdf
from helpers.docs_helper import process_json_to_preserve_styles
from helpers.sheets_helper import process_sheets

r = redis.Redis(
    # host='redis-13397.c330.asia-south1-1.gce.redns.redis-cloud.com', 
    host="redis-12162.c330.asia-south1-1.gce.redns.redis-cloud.com",
    port=12162, 
    db=0,
    password="Xl81F7gDusrIMNygWZbOOF3SOX4OvNzU"
)

def handle_pdf(token,file_id):
        result = r.get(str(f"{token}_{file_id}"))

        if result is None:

          # Step 2: Retrieve file metadata
          metadata_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=name,mimeType"
          metadata_headers = {'Authorization': f'Bearer {token}'}
          metadata_response = requests.get(metadata_url, headers=metadata_headers)

          if metadata_response.status_code != 200:
              print(f"Error fetching metadata: {metadata_response.text}")
              return {"message":"Error while fetching file", "success":False}

          metadata = metadata_response.json()
          file_name = metadata.get('name')
          mime_type = metadata.get('mimeType')

        

          # Step 3: Download the file
          drive_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
          drive_headers = {'Authorization': f'Bearer {token}'}
          
          drive_response = requests.get(drive_url, headers=drive_headers, stream=True)

          if drive_response.status_code == 200:
              content_type = drive_response.headers.get('Content-Type', '')
              
              if content_type != mime_type:
                  print(f"Error: Mismatch in content type. Expected: {mime_type}, Got: {content_type}")
                  return {"error": "File download failed due to content type mismatch","success":False}
              
              download_progress = 0
              file_size = 0
              file_path = file_name

              with open(file_path, 'wb') as f:
                  for chunk in drive_response.iter_content(chunk_size=1024):
                      if chunk:
                          f.write(chunk)
                          download_progress += len(chunk)
                          if not file_size:
                              file_size = int(drive_response.headers.get('Content-Length', 0))
                          if file_size > 0:
                              print(f"Downloaded: {download_progress}/{file_size} bytes ({(download_progress / file_size) * 100:.2f}%)")

              print(f"File downloaded successfully: {file_path}")
              a1 = extract_text_from_pdf(file_path)
              os.remove(file_path)
              r.set(str(f"{token}_{file_id}")), json.dumps({"docs":a1})
              r.expire(str(f"{token}_{file_id}"), 3600)
              return a1
          
        else:
            return result

def handle_sheets(token,file_id):
    result = r.get(str(f"{token}_{file_id}"))

    if result is None:
      url = f"https://sheets.googleapis.com/v4/spreadsheets/{file_id}"

      headers = {
          'Authorization': f'Bearer {token}'
      }
      # client.drop_database('test_collection')
      response = requests.request("GET", url, headers=headers)

      # print(response.text)
      data = response.text
      data1_new_1 = json.loads(response.text)
      extracted_data = process_sheets(data1_new_1)
      r.set(str(f"{token}_{file_id}")), json.dumps({"docs":a1})
      r.expire(str(f"{token}_{file_id}"), 3600)
      return extracted_data
    else:
      return result

def handle_docs(token,file_id):
    # 1VNFP4FcoD4Wiz2rpKEV0CsGAage_sykNQ6E5bGV7Vrc
    result = r.get(str(f"{token}_{file_id}"))

    if result is  None:
      url = f"https://docs.googleapis.com/v1/documents/{file_id}"
      

      headers = {
          'Authorization': f'Bearer {token}'
      }
      # client.drop_database('test_collection')
      response = requests.request("GET", url, headers=headers)

      # print(response.text)
      data = response.text
      data1_new_1 = json.loads(response.text)

      content = data1_new_1["body"]["content"]
      # print(content)
      texts = process_json_to_preserve_styles(content)
      r.set(str(f"{token}_{file_id}")), json.dumps({"docs":a1})
      r.expire(str(f"{token}_{file_id}"), 3600)
      return texts
    else:
      return result