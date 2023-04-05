import requests
import uuid


new_uuid = uuid.uuid4()
new_uuid = str(new_uuid)
print(new_uuid)
url = 'http://127.0.0.1:5000/entry'
payload = {'user_id':new_uuid}

response = requests.post(url, data=payload)

print(response)