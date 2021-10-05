from iotGateway import setup as setup
import iotGateway as iot
import argparse
import os
from time import time

if __name__=='__main__':
    iot.start_time = time()
    parser = argparse.ArgumentParser(description='Enter the number of the credentials set and the device id')
    parser.add_argument(dest='cred_num', metavar='cred_num', help='Enter the number for the set of credentials')
    parser.add_argument(dest='device_id', metavar='device_id', help='Enter the device id as given in Google IoT Core')
    parser.add_argument(dest='dbname', metavar='dbname', help='Enter the name of the source database')

    args = parser.parse_args()
    iot.cred_num = args.cred_num
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'GCP_credentials\\credentials_{iot.cred_num}.json'
    iot.private_key_path = private_key_path = f'GCP_credentials\\rsa_private_{iot.cred_num}.pem'
    iot.device_id = args.device_id
    iot.sub = f'device_{args.device_id}'
    iot.DBname = args.dbname

    # print(iot.device_id)
    # print(f'credentials number: {iot.cred_num}')
    setup.start()