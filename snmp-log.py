import asyncio
import csv
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime
import time

# Define SNMP OIDs
TEMP_OID = "1.3.6.1.3.2019.5.1.2"  # Replace with your actual OID for temperature
HUMIDITY_OID = "1.3.6.1.3.2019.5.1.5"  # Replace with your actual OID for humidity

# SNMP target details
SNMP_HOST = "192.168.1.105"  # Replace with your SNMP device IP
COMMUNITY = "public"  # Replace with your community string
CSV_FILE_PATH = "snmp_data.csv"

async def fetch_snmp_data():
    # Create SNMP engine
    snmpEngine = SnmpEngine()

    # Prepare OIDs
    oids = [TEMP_OID, HUMIDITY_OID]

    # Prepare the iterator for the SNMP GET request
    iterator = get_cmd(
        snmpEngine,
        CommunityData(COMMUNITY, mpModel=0),
        await UdpTransportTarget.create((SNMP_HOST, 161)),
        ContextData(),
        *[ObjectType(ObjectIdentity(oid)) for oid in oids]
    )

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    # Check for errors in the response
    if errorIndication:
        print(f"Error: {errorIndication}")
        return None

    if errorStatus:
        print(f"{errorStatus.prettyPrint()} at {errorIndex}")
        return None

    # Parse the returned values
    snmp_data = {}
    for varBind in varBinds:
        oid = str(varBind[0])
        value = varBind[1]
        snmp_data[oid] = value

    snmpEngine.close_dispatcher()

    return snmp_data

async def log_snmp_data():
    # Open the CSV file in append mode
    with open(CSV_FILE_PATH, mode="a", newline="") as csvfile:
        fieldnames = ["Timestamp", "Temperature", "Humidity"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        while True:
            snmp_data = await fetch_snmp_data()

            if snmp_data:
                # Get the current timestamp in ISO format
                timestamp = datetime.now().isoformat()

                # Extract temperature and humidity values from the response
                temperature = snmp_data.get(TEMP_OID, "N/A")
                humidity = snmp_data.get(HUMIDITY_OID, "N/A")

                # Write the data to the CSV file
                writer.writerow({"Timestamp": timestamp, "Temperature": temperature, "Humidity": humidity})
                print(f"Logged data: {timestamp}, Temp: {temperature}, Humidity: {humidity}")

            # Wait for one hour (3600 seconds) before the next query
            await asyncio.sleep(60)

# Run the script
if __name__ == "__main__":
    asyncio.run(log_snmp_data())
