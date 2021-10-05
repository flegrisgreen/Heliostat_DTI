# Heliostat Instance Twin

## Getting started
- Download Python 3.8 or later
- Needs a MQTT broker
- See the __init__.py file for the configurations
- Switch between brokers in the setup.py file

## Installing dependencies
- Run the setup_venv.bat file and then update_modules.bat file to update all the dependencies

## Running the instance
- Run the run_dts.bat file
- or change the working values in the run.py file of each DTI (see commented code)
- Note the instance will not run if there is no MQTT broker to connect to
- Note: The desired clients must be uncommented in the setup.py file (bottom in start function)

## Modules
- Database_poll.py and firestore_poll.py are debugging programs to check that the data wrote to the SQL and Firestore databases in Google Cloud Platform
- Run.py is the entry-point and it should be called using the run_dts.bat to provide the required arguments
- In the IoTGateway folder:
    - DatabaseManager is a set of functions to interact with the database
    - Mosq_MQTT_Client.py creates a MQTT client that connect to a local MQTT broker
    - MQTT_clinet_create creates an MQTT client to connect to GCP's IoT Core service
    - ReadDB.py reads data from a local SQL database
    - process.py converts the csv format data to a python dictionary
    - setup.py orchestrates the other modules
    - init.py contains the config settings