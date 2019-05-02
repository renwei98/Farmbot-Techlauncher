import paho.mqtt.client as mqtt
import logging
import api_token_gen


def subscribe_topics(client,topics,qos=0):
   print("topic ",topics,"  ",qos)
   
   if type(topics) is not list: #topics should be list of tuples
      if type(topics) is not tuple: #topics isn't tuple?
         topic_list=[(topics,qos)] #topic is single
      else:
         topic_list=[topics]
   else:
      topic_list=topics
   try:
      r=client.subscribe(topic_list)
      if r[0]==0:
          logging.info("subscribed to topic"+str(topic_list)+" return code" +str(r))
          client.topic_ack.append([topic_list,r[1]]) #keep track of subscription
#if successful won't return anything 
      else:
          logging.info("error on subscribing "+str(r))
# if unsuccessful return -1
          return -1

   except Exception as e:
      logging.info("error on subscribe"+str(e))
      return -1
   return r
         
def check_subs(client):
   wcount=0
   while wcount<10: #wait loop
      if len(client.topic_ack)==0:
          return True
      wcount+=1
      if not client.running_loop:
         client.loop(.01)  #check for messages manually
   return False

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected")
    else:
        print("connection failed, rc = ",rc)

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")


device_id = api_token_gen.token_data['token']['unencoded']['bot']
token = api_token_gen.token_data['token']['encoded']
broker= api_token_gen.token_data['token']['unencoded']['mqtt']

# testing locally
mqtt.Client.connected_flag=False#create flag in class
mqtt.Client.topic_ack=[]#create topic acknowledgement list in class
mqtt.Client.running_loop=False#create topic acknowledgement list in class
client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect #assign function to callback

topic0="" 
topic1 =("bot/" + device_id + "/logs")
client= mqtt.Client("Python1",False)       #create client object

client.username_pw_set(device_id, token)
client.connect(broker, port=1883, keepalive=60)

client.loop_start()
print("Subscribing to topics ",topic0)
r=subscribe_topics(client,topic0,0)    #subscribe single topic
print ("subscribed return = ",r)
print('\n')
print("Subscribing to topics ",topic1)
r=subscribe_topics(client,topic1,1)    #subscribe single topic
print ("subscribed return = ",r)


client.disconnect()
client.loop_stop()
