import json
import paho.mqtt.publish as publish
from util import api_token_gen

# from read_commands import ActionHandler

device_id = api_token_gen.token_data['token']['unencoded']['bot']
mqtt_host = api_token_gen.token_data['token']['unencoded']['mqtt']
token = api_token_gen.token_data['token']['encoded']

# Prepare the Celery Script command.
message = {
    'kind': 'take_photo',
    'args': {}
}

# Send the command to the device. Check Farmbot log for success
publish.single(
    'bot/{}/from_clients'.format(device_id),
    payload=json.dumps(message),
    hostname=mqtt_host,
    auth={
        'username': device_id,
        'password': token
        }
)
