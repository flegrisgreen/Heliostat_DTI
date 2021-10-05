from google.cloud import firestore
from time import time
import os
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'firestore_credentials.json'

class db_monitor():
    def __init__(self):
        self.counter = 1
        

    def poll(self, client):
        tel_docs = client.collection(f'aggregates/agg1_summary/telemetry').where('entry_id', '==', self.counter).stream()
        self.counter += 1
        for doc in tel_docs:
            doc_dict = doc.to_dict()
            # data = json.dumps(doc_dict)
            file = open('time_data/firestore_agg_poll_data.txt', 'a')
            file.write(str(doc_dict) + '\n')
            file.close()
            print(self.counter)
            print(doc_dict)
            return

if __name__ == '__main__':
    client = firestore.Client()
    # TODO: set to monitor one pod in each DT instead of monitoring all the heliostats
    agg_monitor = db_monitor()
    while True:
        try:
            agg_monitor.poll(client)
        except:
            print('Not able to contact firestore')