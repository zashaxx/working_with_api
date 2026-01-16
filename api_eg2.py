import requests
import json

base_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita"
response = requests.get(base_url)
response_json = response.json()

print("status code;", response.status_code)
print("response body:", response_json)


