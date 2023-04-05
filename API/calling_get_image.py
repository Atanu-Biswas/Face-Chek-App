import requests

url = 'http://127.0.0.1:5000/get_image'
response = requests.get(url)

if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print(f'Request failed with status code {response.status_code}')
