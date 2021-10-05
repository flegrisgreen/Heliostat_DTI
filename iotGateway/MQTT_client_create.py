import paho.mqtt.client as mqtt
import jwt
import ssl
import datetime
import iotGateway as iot
from json import dumps, loads
from google.cloud import pubsub_v1
from time import time

# Create JWT for GCP IoT Core MQTT client
def jwt_password(project_id, algorithm):
    now = int(datetime.datetime.utcnow().timestamp())  # Unix time format
    later = now + 10000  # 3600s is 1 hour later in unix time format
    token = {
        "iat": now,                                      # Time when password was created
        "exp": later,                                    # Expiry time for the password
        "aud": project_id                                # GCP project id
    }
    private_key_path = iot.private_key_path
    f = open(private_key_path, 'r')
    private_key = f.read()
    JWT = jwt.encode(token, private_key, algorithm=algorithm)
    return JWT, now

def on_connect(client, userdata, flags, rc):
    print('Connection result: '+mqtt.connack_string(rc))

def on_disconnect(client, userdata, rc):
    print('disconnected')

# Logic to process incoming messages
def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    iot.GCP_msg_received = time()
    # print('Message received on Paho client')
    payload_str = str(message.payload.decode('utf-8'))
    msg_dict = dict(loads(payload_str))
    msg_dict['dt_msg_received'] = iot.GCP_msg_received
    # msg_dict.pop('Random')
    print(str(msg_dict))
    file = open(f'time_data/{iot.device_id}_GCP_data.txt', 'a')
    file.write(str(dumps(msg_dict)) + '\n')
    file.close()
    message.ack()

def on_publish(client, userdata, mid):
    print('Publish successful')

def on_subscribe(client, userdata, mid, granted_qos):
    print('Subscription successful')

def create_client():
    iot.GCP_create_client_time = time()
    project_id = iot.project_id
    algorithm = iot.algorithm
    GCP_client_id = f'projects/{iot.project_id}/locations/{iot.location}/registries/{iot.registry}/devices/{iot.device_id}'
    client = mqtt.Client(client_id=GCP_client_id)  # Specify the client id according to google's naming convention
    tls_cert_path = iot.tls_cert_path

    # The following line creates a username and password according to the GCP IoT standards. Password is a jwt format password,
    # that uses a openssl private key (copy/pasted from GCP) and project id to create the password.
    JWT, JWTiat = jwt_password(project_id, algorithm)  #JWT is for the password field and JWTiat is for the JWT renewal
    client.username_pw_set(username='unused',
                           password=JWT)  # username parameter not used by google
    print('JWT token created')
    client.tls_set(ca_certs=tls_cert_path, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Set callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    # Connect to broker
    print(f'connecting to device: {iot.device_id}')
    print(f'connecting using client: {GCP_client_id}')
    client.connect(iot.mqtt_host_name, iot.mqtt_bridge_port, keepalive=60)


    # Paho client subscriptions to IoT Core
    device_id =iot.device_id
    commandsub = f'/devices/{device_id}/commands/#'
    configsub = f'/devices/{device_id}/config'  # Subscribe to config channel to receive configuration messages
    client.subscribe(commandsub, qos=0)
    # client.subscribe([(commandsub, 1), (configsub, 1)])
    # print('Client subscribed to all channels')

    # Cloud Pub/Sub client code below
    def callback(message):
        iot.GCP_msg_received = time()
        payload = message.data.decode('utf-8')
        msg_dict = dict(loads(payload))
        msg_dict['dt_msg_received'] = iot.GCP_msg_received
        # msg_dict.pop('Random')
        print(str(msg_dict))
        file = open(f'time_data/{iot.device_id}_GCP_data.txt', 'a')
        file.write(str(dumps(msg_dict)) + '\n')
        file.close()
        message.ack()

    def update_config(message):
        msg = message.data.decode('utf-8')
        print(msg + '; on topic config')
        if msg == 'No new data':
            print('Returned without change')
            return

        if isinstance(msg, str):
            print('Message received: ' + msg)

        # The message being received in message.data is a byte object, convert back to dictionary using json.loads()
        try:
            config_data = loads(message.data)  # config_data is a dictionary
            if config_data['Reset'] == True:
                col = 'status'
                val = 'True'
                iot.db.updateQ2(database=iot.DBname, tname='helio_status', param=col, host='local', val=val,
                                helio_id=config_data['helio_id'])
                print(f'Helio {config_data["helio_id"]} has been reset')
            else:
                print('Configuration data not changed')
        except Exception as e:
            print(e)
        message.ack()

    # https://googleapis.dev/python/pubsub/latest/index.html provides documentation for google pubsub class
    # Cloud Pub/Sub client subscriber
    project_id = iot.project_id
    subscriber = pubsub_v1.SubscriberClient()

    sub_path = subscriber.subscription_path(project_id, iot.sub)
    config = subscriber.subscription_path(project_id, iot.configsub)

    reply = subscriber.subscribe(sub_path, callback=callback)
    conf = subscriber.subscribe(config, callback=update_config)
    
    # Use pub/sub seek method to acknowledge all unacknowledged messages
    now = time() + 7200
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    cut_off_time = dict({'seconds': seconds, 'nanos': nanos})
    response = subscriber.seek(sub_path, time=cut_off_time)
    iot.GCP_finish_client_create = time()
    return client, JWTiat

