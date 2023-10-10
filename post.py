import requests
 
url = "https://customer-api.krea.se/coding-tests/api/squid-game"
 
data = {
    "answer": "21070",
    "name": "Hari Sagar Ranjitkar",

    
       }
 
response = requests.post(url, json=data)
 
print("Status Code", response.status_code)
print("JSON Response ", response.json())