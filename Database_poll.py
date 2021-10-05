from time import time
import psycopg2

class db_monitor():
    def __init__(self, helio_id):
        self.counter = 1
        self.helio_id = helio_id

    def poll(self, con):
        pattern = f'id = {self.counter}'
        data = select(con, f'helio{self.helio_id}', '*', pattern)
        if data is not None and data != '':
            received = time()
            data.append(received)
            file = open(f'time_data/sql_poll_data.txt', 'a')
            file.write(str(data) + '\n')
            file.close()
            print(self.counter)
            self.counter += 1
            print(data)
        return

def select(con, tname, cols, pattern):
    cur = con.cursor()
    if isinstance(cols, tuple) or isinstance(cols, list):
        parameters = ", "
        parameters = parameters.join(cols)
    else:
        parameters = cols

    cur.execute("SELECT {} FROM {} WHERE {};".format(parameters, tname, pattern))  # This statement will limit the list
    entries = cur.fetchall()  # Fetch all retrieved values
    # entries = cur.fetchmany(10)
    result = []
    for entry in entries:
        for i in range(len(entry)):
            if isinstance(cols, tuple) or isinstance(cols, list):
                thisEntry = str(cols[i]) + ':' + str(entry[i])
                result.append(thisEntry)
            else:
                thisEntry = str(entry[i])
                result.append(thisEntry)
    return result

if __name__=="__main__":
    cloudip = '35.188.178.150'
    cloudpassword = 'helio100'
    database = 'appdata'
    pod_nums = range(1, 58)
    con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip, port='5432')
    # con = psycopg2.connect(database="dt_db1", user="postgres", password="helio", host="127.0.0.1", port="5432")
    # pod_nums = range(13, 18)
    helio_nums = []
    for num in pod_nums:
        helios = [f'{num}1', f'{num}2', f'{num}3', f'{num}4', f'{num}5', f'{num}6']
        helio_nums = helio_nums + helios

    monitors = []
    for num in helio_nums:
        num = db_monitor(num)
        monitors.append(num)

    while True:
        try:
            for monitor in monitors:
                monitor.poll(con)
        except:
            print('Not able to read tables')

    con.close()
