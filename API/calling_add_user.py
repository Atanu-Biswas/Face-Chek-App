import requests

url = 'http://127.0.0.1:5000/add_user'
name='atanu'
details = 'chatrabagi'
payload = {'name':name,'details':details}

response = requests.post(url, data=payload)

print(response)
