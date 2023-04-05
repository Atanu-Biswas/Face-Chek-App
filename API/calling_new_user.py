import requests
import base64
from urllib.parse import quote
import uuid

image =''
with open('img.jpg', 'rb') as image_file:
    encoded_string = base64.urlsafe_b64encode(image_file.read()).decode('utf-8')
    image = quote(encoded_string)

new_uuid = uuid.uuid4()
new_uuid = str(new_uuid)
encoding ='string data'

url = 'http://127.0.0.1:5000/new_user'
payload = {'user_id':new_uuid,'Image': image, 'image_encoding': encoding}

response = requests.post(url, data=payload)

print(response)