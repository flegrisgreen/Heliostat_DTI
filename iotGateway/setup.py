from time import sleep, time
from datetime import datetime
import iotGateway as iot
import iotGateway.ReadDB as read
import iotGateway.MQTT_client_create as mqtt
import iotGateway.Mosq_MQTT_Client as mosq
from json import dumps
from threading import Thread
from google.cloud import pubsub_v1 as pub
# from google.cloud import iot_v1

class thread(Thread):

    # Create a thread for each client
    def __init__(self, name, client, JWTiat=0):
        Thread.__init__(self)
        self.name = name
        self.client = client
        if name == 'GCP':
            self.JWTiat = JWTiat
            # self.GCP_client = iot_v1.DeviceManagerClient()
            self.GCP_client = pub.PublisherClient()

    def run(self):
        # Random data dictionary approx 1 kB
        random_data = {'James 2:6': 'Be quick to listen, slow to speak and slow to anger',
                       'Bruce Lee': 'Absorb what is useful, discard what is not and add that which is uniquely your own',
                       'Aristotle': 'No one would choose a friendless existence on condition of having all the other things in the world',
                       'Stephen Covey': 'Some people climb the ladder with all their might and when they get to the top, realize it was the wrong ladder all along',
                       'Richard Feynman': 'I was born not knowing and have had only a little time to change that here and there',
                       'Dr Seuss': 'Do not cry because it is over.  Smile because it happened',
                       'Oscar Wilde': 'Be yourself; everyone else is already taken',
                       'Albert Einstein': 'Life is like riding a bicycle, to keep your balance you must keep moving',
                       'Unknown': 'The higher the mountain the thinner the air, the better the view',
                       'Allen watts': 'Trying to define yourself is like trying to bite your own teeth',
                       'Robert Oppenheimer': 'I have become death, the destroyer of worlds',
                       'The end': 'Good luck and thank you for all the fish'}
        random_data_list = []
        # Size of random data appended
        for i in range(1, 10):
            random_data_list.append(random_data)
            
        helio_row_ids = read.list_helios()
        self.client.loop_start()

        # Check connection
        while not self.client.is_connected():
            sleep(1)
        print('connected')
        c = 1
        while True:
            print(c)
            c = c + 1

            if self.name == 'GCP':
            # The next block of code performs JWT and client renewal after one hour of continuous functioning
                sec_since_issued = int(datetime.utcnow().timestamp()) - self.JWTiat
                if sec_since_issued > 3600:  # Wait one hour before refreshing the client
                    print('Refreshing JWT token')
                    self.client, self.JWTiat = mqtt.create_client()
                    self.client.connect(iot.mqtt_host_name, iot.mqtt_bridge_port, keepalive=60)
            
            # Get new heliostat data entry
            for helio in helio_row_ids:
                row_id = helio_row_ids.get(helio)
                data_dict, cols, row_id = read.read(helio, row_id)
                helio_row_ids.update({helio: row_id})
                # read() returns all the latest info in dictionary format and also returns the columns that are the dictionary entries
                # The next 4 lines make a list of all the connected helios
                if data_dict is not None:
                    for dicti in data_dict:
                        if dicti[cols[1]] not in iot.helios:
                            iot.helios.append(dicti[cols[1]])
                
                # For every new data entry perform the following
                if data_dict is not None:
                    for dicti in data_dict:
                        helio_id = dicti['helio_id']
                        
                        # Logic for GCP pub/sub experiment
                        if self.name == 'GCP':
                            iot.GCP_msg_sent = time()
                            
                            #4C Communication data
                            timestamps = {"exe_start": iot.start_time, "GCP_client_start": iot.GCP_create_client_time,
                                          "GCP_client_fin": iot.GCP_finish_client_create, "GCP_msg_send": iot.GCP_msg_sent,
                                          "firestore_timestamp": 0}
                            dicti.update(timestamps)
                            dicti['device_id'] = iot.device_id
                            # dicti['Random'] = random_data_list
                            # dicti['msg_size'] = '10 KB'
                            payload = dumps(dicti)
                            
                            # 4A communication data
                            agg1_info = iot.agg1_info
                            agg1_dict = {}
                            for item in agg1_info:
                                agg1_dict[item] = dicti[item]
                            agg1_dict.update(timestamps)
                            agg1_dict['device_id'] = iot.device_id
                            # agg1_dict['Random'] = random_data_list
                            # agg1_dict['msg_size'] = '10 KB'
                            payload2 = dumps(agg1_dict).encode('utf-8')
                            # topic_path = self.GCP_client.device_path(iot.project_id, iot.location, "Agg_registry", "agg1")
                            topic_path = self.GCP_client.topic_path(iot.project_id, 'agg_data')
                            
                            # Publish to cloud IoT Core
                            self.client.publish(f'/devices/{iot.device_id}/events', payload=payload, qos=0, retain=False)
                            
                            #Publish to aggregate using Cloud Pub/Sub
                            try:
                                # self.GCP_client.send_command_to_device(topic_path, payload2)
                                self.GCP_client.publish(topic_path, data=payload2)
                            except:
                                print('Could not send message to aggregate')
                            # print(f'Published {payload} to GCP')
                            sleep(1)

                        if self.name == 'Mosquitto':
                            # Aggregates and the data that each aggregate must receive
                            agg1_info = iot.agg1_info
                            agg1_dict = {}
                            for item in agg1_info:
                                agg1_dict[item] = dicti[item]

                            # Timestamp info
                            iot.mosq_msg_sent = time()
                            timestamps = {"exe_start": iot.start_time, "mosq_client_start": iot.mosq_create_client_time,
                                          "mosq_client_fin": iot.mosq_finish_client_create,
                                          "mosq_msg_send": iot.mosq_msg_sent}
                            agg1_dict.update(timestamps)
                            agg1_dict['device_id'] = iot.device_id
                            # agg1_dict['msg_size'] = '50 KB'
                            # agg1_dict['Random'] = random_data_list
                            payload = dumps(agg1_dict)

                            # Publish data to all the agregates
                            self.client.publish(f'telemetry/agg1/heliostat{helio_id}',
                                                payload=str(payload), qos=1, retain=False)
                            sleep(0.5)
                            # print(payload)

                else:
                    payload = 'No new data'
                    # client.publish(f'/devices/{iot.device_id}/events', payload=payload, qos=0, retain=False)
                    print(payload)



def start():
    # client, JWTiat = mqtt.create_client()
    mosq_client = mosq.create_client()

    # GCP_client = thread('GCP', client, JWTiat)
    Mosq_client = thread('Mosquitto', mosq_client)

    # GCP_client.start()
    Mosq_client.start()

    # threads = []
    # threads.append(GCP_client)
    # threads.append(Mosq_client)
    #
    # for t in threads:
    #     t.join()
    #
    # print('All threads released. Terminating program')


