import time
import paho.mqtt.client as mqtt
from datetime import datetime

def on_publish(client, userdata, mid):
    print("sent a message")

# a callback function
def on_message_next_id(client, userdata, msg):
    print('Received a new next id ', msg.payload.decode('utf-8'))

def on_message_stop(client, userdata, msg):
    print('Time', msg.payload.decode('utf-8'))

mqttClient = mqtt.Client("mqtt_client")
mqttClient.username_pw_set("udesc", "udesc")
mqttClient.on_publish = on_publish

mqttClient.message_callback_add('ProximoID', on_message_next_id)
mqttClient.message_callback_add('TempoDecorrido', on_message_stop)

mqttClient.connect('localhost', 1883)
mqttClient.loop_start()

mqttClient.subscribe("ProximoID")
mqttClient.subscribe("TempoDecorrido")

while True:

    current_id_msg = "2" # example
    current_id_info = mqttClient.publish(
        topic='IDAtual',
        payload=current_id_msg.encode('utf-8'),
        qos=0,

    )

    stop_msg = "pousar" 
    stop_info = mqttClient.publish(
        topic='StopCronometr',
        payload=stop_msg.encode('utf-8'),
        qos=0,

    )

    current_id_info.wait_for_publish()
    print(current_id_info.is_published())
    stop_info.wait_for_publish()
    print(stop_info.is_published())
    time.sleep(1) # 1 sec