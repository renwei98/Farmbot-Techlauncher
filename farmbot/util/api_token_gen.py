import json
import urllib.request


def get_token(username, password):
    data = {'user': {'email': username, 'password': password}}

    req = urllib.request.Request('https://my.farmbot.io/api/tokens')
    req.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(req, json.dumps(data).encode('utf-8'))

    raw_json = response.read()
    token_data = json.loads(raw_json)
    the_token = token_data['token']['encoded']

    return the_token
