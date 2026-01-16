import requests
import json

response = requests.get('https://api.chucknorris.io/jokes/random')
response_json = response.json()


# response1 = request.get('https://google.com')
# print(response1)

# print(response)

print("Fetched Joke: "+response_json['value'])
print("URL: " +response_json['url'])
print("Joke fetched successfully")


category = 'money'

response2 = requests.get('https://api.chucknorris.io/jokes/random?categotry='+category)

response2_json = response2.json()

print("Fetched Joke from category "+category+": "+response2_json['value'])
