import paho.mqtt.client as mqtt
import iotGateway as iot
import os
from json import loads, dumps
from time import time

def on_connect(client, userdata, flags, rc):
    print('Connection result: '+mqtt.connack_string(rc))

def on_disconnect(client, userdata, rc):
    print('disconnected')

def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    iot.mosq_msg_received = time()
    payload = message.payload.decode('utf-8')
    msg_dict = dict(loads(payload))
    msg_dict['dt_msg_received'] = iot.mosq_msg_received
    # msg_dict.pop('Random')
    print('Message received')
    file = open(f'time_data/{iot.device_id}_mosq_data.txt', 'a')
    file.write(str(dumps(msg_dict))+'\n')
    file.close()
    message.ack()

def on_publish(client, userdata, mid):
    print('Publish successful')

def on_subscribe(client, userdata, mid, granted_qos):
    print('Subscription successful')

def create_client():
    password = os.environ.get('PASSWORD')
    iot.mosq_create_client_time = time()
    client = mqtt.Client(client_id=f'{iot.device_id}')  # Specify the client id
    client.username_pw_set(username='heliostat',
                           password=password)  # username parameter not used by google
    tls_ca_cert = iot.tls_ca_cert
    tls_client_cert = iot.tls_client_cert
    tls_client_key = iot.tls_client_key
    client.tls_set(ca_certs=tls_ca_cert, certfile=tls_client_cert, keyfile=tls_client_key)

    # Set callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    # Connect to broker
    client.connect(iot.mosq_mqtt_hostname, iot.mosq_mqtt_port, keepalive=60)
    iot.mosq_finish_client_create = time()

    # Paho subscription for aggregation
    client.subscribe(f'telemetry_reply/{iot.device_id}', qos=1)
    return client