from google.cloud import firestore
from threading import Thread
from time import time
import os
import sys
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'firestore_credentials.json'

class thread(Thread):

    def __init__(self, pods):
        Thread.__init__(self)
        self.pods = pods
        return


    def run(self):
        client = firestore.Client()
        helio_nums = []
        pod_nums = self.pods
        for num in pod_nums:
            helios = [f'{num}.1', f'{num}.2', f'{num}.3', f'{num}.4', f'{num}.5', f'{num}.6']
            helio_nums = helio_nums + helios

        monitors = []
        for num in helio_nums:
            num = db_monitor(num)
            monitors.append(num)

        while True:
            try:
                for monitor in monitors:
                    monitor.poll(client)
            except:
                print('Not able to contact firestore')

class db_monitor():

    def __init__(self, helio_id):
        self.counter = 1
        self.helio_id = helio_id

    def poll(self, client):
        tel_docs = client.collection(f'helio_field/heliostat{self.helio_id}/telemetry').where('id', '==', f'{self.counter}').stream()
        # tel_docs = client.collection(f'aggregates/agg1/telemetry').stream()
        for doc in tel_docs:
            doc_dict = doc.to_dict()
            if int(doc_dict['id']) >= self.counter:
                # data = json.dumps(doc_dict)
                file = open('time_data/firestore_poll_data.txt', 'a')
                file.write(str(doc_dict) + '\n')
                file.close()
                self.counter += 1
                print(self.counter)
                print(doc_dict)
                if self.counter >= 80:
                    sys.exit(0)
            return

if __name__ == '__main__':

    set1 = range(1, 11)
    set2 = range(11, 21)
    set3 = range(21, 31)
    set4 = range(31, 41)
    set5 = range(41, 51)
    set6 = range(51, 58)

    pod_set1 = thread(set1)
    pod_set2 = thread(set2)
    pod_set3 = thread(set3)
    pod_set4 = thread(set4)
    pod_set5 = thread(set5)
    pod_set6 = thread(set6)

    pod_set1.start()
    pod_set2.start()
    pod_set3.start()
    pod_set4.start()
    pod_set5.start()
    pod_set6.start()

