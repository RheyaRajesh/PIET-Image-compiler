import requests

url = "http://127.0.0.1:8000/run"
files = {'file': open('simple.png', 'rb')}
data = {'codel_size': '1'}
response = requests.post(url, files=files, data=data)
print(response.json())
