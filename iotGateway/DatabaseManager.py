import psycopg2 as psycopg2

class DatabaseManager:
    """Class that contains function to manage the pgSQL database"""
    # TODO: Change these parameters to accommodate any other database connection
    global cloudip
    global cloudpassword
    cloudip = '35.188.178.150'
    cloudpassword = 'helio100'

    def __init__(self):
        return

# ------------------------------- Function that creates a table in a pgSQL database ----------------------------------
    def createTable(self, database, name, cols, dtype, host='local'):

        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password="helio", host="127.0.0.1", port="5432")

        cur = con.cursor()
        assert isinstance(name, object)
        i = 0
        str = []
        while i < len(cols):
            a = cols[i]
            b = dtype[i]
            if i == 0:
                c = a+" "+b+" PRIMARY KEY"
            else:
                c = a + " " + b
            str.append(c)
            i = i+1

        fullstr = ", "
        fullstr= fullstr.join(str)
        cur.execute('''CREATE TABLE {} ({})'''.format(name, fullstr))
        con.commit()
        con.close()
        print("Table {} created".format(name))
        return

    def deleteTable(self, database, table, host='local'):

        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password="helio", host="127.0.0.1", port="5432")

        cur = con.cursor()
        cur.execute('DROP TABLE {}'.format(table))
        con.commit()
        con.close()
        print('Table {} deleted'.format(table))

# ----------------------------------- Function to insert a query -------------------------------------------------

    def insertQ(self, database, tname, params, vals, host='local'):

        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password="helio", host="127.0.0.1", port="5432")

        cur = con.cursor()
        assert isinstance(tname, object)
        parameters = ", "
        parameters = parameters.join(params)

        for i in range(len(vals)):
            vals[i] = "'{}'".format(str(vals[i]))

        values = ", "
        values = values.join(vals)
        cur.execute("INSERT INTO {} ({}) VALUES({})".format(tname, parameters, values))
        print("Query has been committed to {}".format(tname))
        con.commit()
        con.close()
        return

# ------------------------------- Function to select all queries ------------------------------------------------------
    def selectAll(self, database, tname, cols, host='local'):

        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip,
                                   port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password="helio", host="127.0.0.1", port="5432")

        cur = con.cursor()
        if isinstance(cols, tuple):
            parameters = ", "
            parameters = parameters.join(cols)
        else:
            parameters = cols

        cur.execute(
            "SELECT {} FROM {};".format(parameters, tname))  # This statement will limit the list
        entries = cur.fetchall()  # Fetch all retrieved values
        # entries = cur.fetchmany(10)
        result = []
        for entry in entries:
            for i in range(len(entry)):
                if isinstance(cols, tuple):
                    thisEntry = str(cols[i]) + ':' + str(entry[i])
                    result.append(thisEntry)
                else:
                    thisEntry = str(entry[i])
                    result.append((thisEntry))
        con.close()
        return result

    # todo: add a select latest function
    # todo: add a select all parameters method that can be used as "select * from ..." -> might need GUI for this
# ------------------------------ Function to select a single query ---------------------------------------------
    def select(self, database, tname, cols, pattern, host='local'):
        # Cols are the columns that you want to select from the table.
        # pattern is <parameter of interest> operator <value>
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password="helio", host="127.0.0.1", port="5432")

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
        con.close()
        return result

    # Select function for the weather readings (due to large number of weather entries)
    def Wselect(self, database, tname, cols, pattern, host='local'):
        # Cols are the columns that you want to select from the table.
        # pattern is <parameter of interest> operator <value>
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password="helio", host="127.0.0.1", port="5432")

        cur = con.cursor()
        if isinstance(cols, tuple):
            parameters = ", "
            parameters = parameters.join(cols)
        else:
            parameters = cols

        cur.execute("SELECT {} FROM {} WHERE {} ORDER BY ID ASC;".format(parameters, tname, pattern))  # This statement will limit the list
        # entries = cur.fetchall()  # Fetch all retrieved values
        entries = cur.fetchone()
        result = []
        i = 0
        for entry in entries:
            if isinstance(cols, tuple):
                thisEntry = str(cols[i]) + ':' + str(entry)
                result.append(thisEntry)
                i = i + 1
            else:
                thisEntry = str(entry)
                result.append(thisEntry)
                i = i + 1
        con.close()
        return result

# ------------------------------ Function to update a query ------------------------------------------------------
    def updateQ(self, database, tname, param, val, id, host='local'):
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password="helio", host="127.0.0.1", port="5432")

        cur = con.cursor()
        cur.execute("UPDATE {} set {} = {} where id={}".format(tname, param, str(val), str(id)))
        con.commit()
        con.close()

    def createTrigger(self, database, host='local'):
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password="helio", host="127.0.0.1", port="5432")

        cur = con.cursor()
        cur.execute('CREATE TRIGGER UPDATERT BEFORE INSERT ON PUBLIC.BATTERY FOR EACH ROW EXECUTE PROCEDURE'
                    ' PUBLIC.UPDATE_BATTERYRT();')
        con.commit()
        con.close()

    def updateQ2(self, database, tname, param, val, helio_id, host='local'):
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=cloudpassword, host=cloudip,
                                   port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password="helio", host="127.0.0.1", port="5432")

        cur = con.cursor()
        cur.execute("UPDATE {} set {} = {} where helio_id = '{}'".format(tname, param, str(val), str(helio_id)))
        con.commit()
        con.close()