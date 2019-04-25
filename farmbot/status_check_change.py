import paho.mqtt.client as mqtt
def subscribe_topics(client,topics,qos=0):
   print("topic ",topics,"  ",qos)
   
   if type(topics) is not list: #topics should be list of tuples
      if type(topics) is not tuple: 
         topic_list=[(topics,qos)]
      else:
         topic_list=[topics]
   else:
      topic_list=topics
   try:
      r=client.subscribe(topic_list)
      if r[0]==0:
          logging.info("subscribed to topic "+str(topic_list)+" return code" +str(r))
          client.topic_ack.append([topic_list,r[1],0]) #keep track of subscription

      else:
          logging.info("error on subscribing "+str(r))
          print("error on subscribing "+str(r))
          return -1

   except Exception as e:
      logging.info("error on subscribe"+str(e))
      return -1
   return r