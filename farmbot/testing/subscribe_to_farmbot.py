import paho.mqtt.client as mqtt
from util import api_token_gen

device_id = api_token_gen.token_data['token']['unencoded']['bot']
token = api_token_gen.token_data['token']['encoded']
server = api_token_gen.token_data['token']['unencoded']['mqtt']


def on_connect(client, userdata, flags, rc):
    if rc == 5:
        return "authentication error: wrong username or password"
    elif rc == 0:
        print("authentication successful")

    # For docs on subscribe functions, see https://github.com/FarmBot-Labs/FarmBot-Python-Examples
    client.subscribe("bot/" + device_id + "/status")
    client.subscribe("bot/" + device_id + "/logs")
    client.subscribe("bot/" + device_id + "/from_clients")
    client.subscribe("bot/" + device_id + "/from_device")


def on_message(client, userdata, msg):
    # Print received message from Farmbot
    print("Incoming MQTT messages: ")
    print(msg.topic + " " + str(msg.payload))


# Connect to the broker using credentials from `token_generation_example.py`
client = mqtt.Client("name_set_by_user")
client.username_pw_set(device_id, token)

# Attach event handlers:
client.on_connect = on_connect
client.on_message = on_message

# Connect to the server:
client.connect(server, port=1883, keepalive=60)

client.loop_forever()
