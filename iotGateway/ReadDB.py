import iotGateway as iot
from iotGateway import process as p

# Read data from the local PostgreSQL database
def read(helio, row_id):
    
    # Set SQL query pattern
    pattern = f"id > {row_id} ORDER by id"  # Get all the latest values since last read based on id
    helio = helio.split('.', 1)
    helio_table = ''.join(helio)
    helio_table = f'local_helio{helio_table}'   
    
    # Query the data
    data = iot.db.select(database=iot.DBname, tname=helio_table, cols=iot.columns, pattern=pattern)
    
    # Save individual data entries to a dictionary
    if len(data) > 0:
        data_dict, cols = p.data_dict(data)
        size = len(data_dict)
        latest_id = data_dict[size-1][cols[0]]
        row_id = latest_id

    else:
        print('No new data from read()')
        data_dict = None
        cols = None
    
    # Reset query value
    data.clear()
    return data_dict, cols, row_id

def list_helios():

    helio_list = iot.db.selectAll(iot.DBname, 'local_helio_list', 'helio_id')
    helio_init = '0'
    helio_ids = dict.fromkeys(helio_list, helio_init)
    return helio_ids

