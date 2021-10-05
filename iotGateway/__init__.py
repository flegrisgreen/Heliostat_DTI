import iotGateway.DatabaseManager as DB
import os

# Database variables
db = DB.DatabaseManager()
DBname = 'dt_db1'
columns = ['id', 'helio_id', 'battery', 'motor1', 'motor2', 'date', 'status', 'grena_target']
data_types = ['int', 'varchar(127)', 'real', 'real', 'real', 'timestamp', 'varchar(50)', 'varchar(127)']

# Experiment parameters
# List of all helios that are sending information (updates as the helios send info)
helios = []
start_time = 0.0

GCP_create_client_time = 0.0
GCP_finish_client_create = 0.0
GCP_msg_sent = 0.0
GCP_msg_received = 0.0

mosq_create_client_time = 0.0
mosq_finish_client_create = 0.0
mosq_msg_sent = 0.0
mosq_msg_received = 0.0

# x and y arrays for the live plots
x_vals = []
y_vals = []

# MQTT parameters
project_id = os.environ.get('CLOUD_PROJECT')
location = 'us-central1'
registry = 'Test_registry'
device_id = 'device'
algorithm = 'RS256'
mqtt_bridge_port = 8883
mqtt_host_name = 'mqtt.googleapis.com'

# Subscription
sub = 'device_messages'
configsub = 'config_sub'

# subscription = f'projects/{project_id}/subscriptions/{sub}'
configsub_core = f'/devices/{device_id}/config'
commandsub = f'/devices/{device_id}/commands/#'

# Google Cloud Authentication variables
# This sets the environment variable, GOOGLE_APPLICATION_CREDENTIALS, so that google APIs can be used.
# the path is a json key from service account credentials
cred_num = '1'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'GCP_credentials\\credentials_{cred_num}.json'  -> This is being set in Run.py
tls_cert_path = 'GCP_credentials\\roots.pem'
private_key_path = f'GCP_credentials\\rsa_private_{cred_num}.pem'

# Mosquitto MQTT client parameters
mosq_mqtt_port = 8883

# Cloud based Mosquitto client
mosq_mqtt_hostname = os.environ.get('CLOUD_IP')
tls_ca_cert = 'cloud_credentials\cloudca.pem'
tls_client_cert = 'cloud_credentials\cloudclient.crt'
tls_client_key = 'cloud_credentials\cloudclient.key'

# Local Mosquitto client
# mosq_mqtt_hostname = os.environ.get('LOCALHOST')
# tls_ca_cert = 'local_credentials\ca.crt'
# tls_client_cert = 'local_credentials\client.crt'
# tls_client_key = 'local_credentials\client.key'

# Aggregate parameters
agg1_info = ['helio_id', 'date', 'status']