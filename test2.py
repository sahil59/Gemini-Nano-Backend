from pymongo import MongoClient
import redis
import json

from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi

# Connection string with explicit certificate path
client = MongoClient(
    "mongodb+srv://pranavsingh8108:Pranav7777@cluster0.rdvs2.mongodb.net/",
    server_api=ServerApi('1'),
    tls=True,
    tlsCAFile=certifi.where()  # This is the key addition for macOS
)

db = client['test_database']
collection = db['test_collection'] 

try:
    # Test the connection
    client.admin.command('ping')
    print("Connected successfully to MongoDB!")
    
    # Your database operations
    
    query_result = collection.find_one({"email": "pranav.singh@gmail.com"})
    print(query_result)
    
except Exception as e:
    print(f"An error occurred: {e}")
# print("Retrieved document:", query_result['_id'])


r = redis.Redis(
    # host='redis-13397.c330.asia-south1-1.gce.redns.redis-cloud.com', 
    host="redis-12162.c330.asia-south1-1.gce.redns.redis-cloud.com",
    port=12162, 
    db=0,
    password="Xl81F7gDusrIMNygWZbOOF3SOX4OvNzU"
)

print("redis with no problem") 

# Delete key "1" if it exists
r.delete("1")

# Check if "mongo_id" exists
docs_id = '1idQBzG7L9PJcLRo-dv18yS07pY7vHjYorJ3MJFOHClA'
updated_document = collection.find_one({"email": "pranav.singh@gmail.com"})
result = r.get(str(updated_document['_id']))

data_dicts = {}

for i in updated_document['messages1']:
   data_dicts[i['name']]=i['id']


file_content = ""

# Open the file in read mode
with open("output.txt", "r") as file:
    # Traverse the file line by line
    for line in file:
        # Append each line to the string
        file_content += line

# print("result is",result)
if result is None:
    # Set the key "mongo_id" with a value and serialize it using json.dumps
    print("setting up key")
    r.set(str(updated_document['_id']), json.dumps({"documents_list": 23,"docs":data_dicts}))
    # Set the key to expire after 1 hour (3600 seconds)
    r.expire(str(updated_document['_id']), 36)


# Decode the result from bytes to string
if result is not None:
    print("fetching key")
    result = result.decode('utf-8')
    a = json.loads(result)
    print(a["docs"]["Let Us C - Solutions.pdf"])
    if f'docs{docs_id}' in a:

        print("Yes")
    else:
        a[f'docs{docs_id}'] = file_content 
        r.set(str(updated_document['_id']), json.dumps(a))
    
        # Reset the expiration time (optional)
        r.expire(str(updated_document['_id']), 36)
    # print(result['docs'])

print("now the result is",result)