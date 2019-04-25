import paho.mqtt.client as mqtt
import logging

def subscribe_topics(client,topics,qos=0):
   print("topic ",topics,"  ",qos)
   
   if type(topics) is not list: #topics should be list of tuples
      if type(topics) is not tuple: 
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

      else:
          logging.info("error on subscribing "+str(r))
          return -1

   except Exception as e:
      logging.info("error on subscribe"+str(e))
      return -1
   return r
         
def check_subs(client):
   wcount=0
   while wcount<10: 
      if len(client.topic_ack)==0:
          return True
      wcount+=1
      if not client.running_loop:
         client.loop(.01)  #check for messages manually

   return False



def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)



