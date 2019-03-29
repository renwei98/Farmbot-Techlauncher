from dotenv import load_dotenv
import os
import json
import urllib.request

load_dotenv()
data = {'user': {'email': os.getenv("EMAIL"), 'password': os.getenv("PASSWORD")}}

req = urllib.request.Request('https://my.farmbot.io/api/tokens')
req.add_header('Content-Type', 'application/json')
response = urllib.request.urlopen(req, json.dumps(data).encode('utf-8'))

raw_json = response.read()
token_data = json.loads(raw_json)

the_token = token_data['token']['encoded']

print("Your device id is: \n" + token_data['token']['unencoded']['bot'] + "\n")
print("The MQTT Host is: \n" + token_data['token']['unencoded']['mqtt'] + "\n")
print("The token is: \n" + the_token)
