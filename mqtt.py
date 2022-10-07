from http import client
from logging import getLoggerClass
from statistics import mode
from paho.mqtt import client as mqtt_client
import json
import time
import csv

#topics
#mr74  -> mosquitto_sub -t meraki/v1/mr/N_611363649415560954/0C:8D:DB:D9:17:32/ble/#
#mr33 -> 'meraki/v1/mr/N_611363649415560954/68:3A:1E:83:31:8F/ble/#'
#mr44 -> 'meraki/v1/mr/N_611363649415560954/F8:9E:28:74:51:F9/ble/#'

broker = '192.168.128.17'
topic74 = 'meraki/v1/mr/N_611363649415560954/0C:8D:DB:D9:17:32/ble/#'
topic33 = 'meraki/v1/mr/N_611363649415560954/68:3A:1E:83:31:8F/ble/#'
topic44 = 'meraki/v1/mr/N_611363649415560954/F8:9E:28:74:51:F9/ble/#'
topic_personas = '/merakimv/Q2GV-2V9V-NMDF/0'
message_dic = []
personas = []


def on_connect(client, userdata, flags, rc): 
      if rc==0: 
          print("connected OK") 
      else: 
            print("Bad connection Returned code= ",rc) 

def on_message(client, userdata, message):
        global message_dic
        message = json.loads(message.payload.decode("utf-8")) 
        metrics = '\n' + message['mrMac'] + ',' + message['clientMac'] + ',' +message['rssi'] 
        if message['clientMac']== '00:FA:B6:01:E8:5B': #00:FA:B6:01:E8:49': or message['clientMac'] == '00:FA:B6:01:E8:5B' or message['clientMac'] == '00:FA:B6:01:E8:6D':
            print(message['mrMac'] + '    ' + message['clientMac'] + '    ' +message['rssi']) 
        #print(message['mrMac'] + '    ' + message['clientMac'] + '    ' +message['rssi']) 
            message_dic.append(int(message['rssi']))
        
        return message_dic
        #file = open('mqtt_message_mR74.txt',mode="w")
        #file.write(str(message_dic))
        #file.close()

def filtro_max_min(message):
    minimo = min(message)
    maximo = max(message) 
    print(minimo,maximo)

def on_messagemv(client, userdata, message):
        global personas, n_personas
        message = json.loads(message.payload.decode("utf-8")) 
        n=message['counts']['person']
        print(message)
        personas.append(n)
        n_personas = mode(personas)
        print(personas, ' moda: ',n_personas)

def almacenar(lista,topic):
    
    if topic == topic74: ap='74' 
    elif topic == topic33: ap = '33'  
    else: ap = '44'
    with open('./files/mqtt_message_mR{}_prueba.csv'.format(ap),mode="w", newline='\n') as newfile:
        writer = csv.writer(newfile)
        writer.writerow(lista)

def general(broker):
    global client 
    client = mqtt_client.Client('mqtt_client')
    client.on_connect = on_connect
    
    topics = [topic44] #,topic33,topic44]
    toma_muestra(topics)
    

def toma_muestra(topics):
    global message_dic
    for topic in topics:
        client.connect(broker)
        client.subscribe(topic)
        print("suscrito a " + topic)
        client.on_message = on_message
        client.loop_start()
        time.sleep(20)
        filtro_max_min(message_dic)
        almacenar(message_dic,topic)
        message_dic = []
        client.loop_stop()
        client.disconnect()


general(broker)

def camara():
    global clientmv , personas, n_personas
    personas = []
    clientmv = mqtt_client.Client('mv_mqtt_client')
    clientmv.on_connect = on_connect
    clientmv.connect(broker)
    clientmv.subscribe(topic_personas)
    print("suscrito a " + topic_personas)
    clientmv.on_message = on_messagemv
    clientmv.loop_start()
    time.sleep(1)   
    clientmv.loop_stop()
    clientmv.disconnect()
    return n_personas

#for i in range(0,5):
#    camara()