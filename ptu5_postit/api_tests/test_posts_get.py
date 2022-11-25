import requests
from pprint import pprint

reqUrl = "http://127.0.0.1:8000/posts/"

headersList = {
 "Accept": "*/*",
 "User-Agent": "CodeAcademy API Test App" 
}

payload = ""

response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

pprint(response.text)