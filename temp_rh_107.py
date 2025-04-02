import asyncio
import csv
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime
import time
import os

# Define SNMP OIDs
TEMP_OID = "1.3.6.1.3.2019.5.1.2"  # Replace with your actual OID for temperature
HUMIDITY_OID = "1.3.6.1.3.2019.5.1.5"  # Replace with your actual OID for humidity

# SNMP target details
SNMP_HOST = "192.168.1.107"  # Replace with your SNMP device IP
COMMUNITY = "public"  # Replace with your community string

# Generate a unique CSV filename with the script launch date
LAUNCH_DATE = datetime.now().strftime("%Y-%m-%d")
CSV_DIR = "/home/guest/.registros"
CSV_FILE_PATH = os.path.join(CSV_DIR, f"temp_rh_107_{LAUNCH_DATE}.csv")

async def fetch_snmp_data():
    snmpEngine = SnmpEngine()
    oids = [TEMP_OID, HUMIDITY_OID]

    iterator = get_cmd(
        snmpEngine,
        CommunityData(COMMUNITY, mpModel=0),
        await UdpTransportTarget.create((SNMP_HOST, 161)),
        ContextData(),
        *[ObjectType(ObjectIdentity(oid)) for oid in oids]
    )

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    if errorIndication:
        print(f"Error: {errorIndication}")
        return None

    if errorStatus:
        print(f"{errorStatus.prettyPrint()} at {errorIndex}")
        return None

    snmp_data = {str(varBind[0]): varBind[1] for varBind in varBinds}
    snmpEngine.close_dispatcher()
    return snmp_data

async def log_snmp_data():
    os.makedirs(CSV_DIR, exist_ok=True)  # Ensure directory exists

    with open(CSV_FILE_PATH, mode="a", newline="") as csvfile:
        fieldnames = ["Timestamp", "Temperature", "Humidity"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        while True:
            snmp_data = await fetch_snmp_data()
            if snmp_data:
                timestamp = datetime.now().isoformat()
                temperature = snmp_data.get(TEMP_OID, "N/A")
                humidity = snmp_data.get(HUMIDITY_OID, "N/A")

                writer.writerow({"Timestamp": timestamp, "Temperature": temperature, "Humidity": humidity})
                print(f"Logged data: {timestamp}, Temp: {temperature}, Humidity: {humidity}")

            await asyncio.sleep(3600)  # Wait for one minute before the next query

if __name__ == "__main__":
    asyncio.run(log_snmp_data())

