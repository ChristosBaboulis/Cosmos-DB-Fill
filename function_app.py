import os
import re
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient

# Cosmos DB σύνδεση
COSMOS_URL = os.getenv("COSMOS_URL")
COSMOS_KEY = os.getenv("COSMOS_KEY")
cosmos_client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY)
cosmos_container = cosmos_client.get_database_client("traffic-db").get_container_client("vehicles")

# Regex για οχήματα
vehicle_pattern = re.compile(
    r"ID: (\d+) \| Type: (\w+) \| Direction: (\w+) \| Speed: ([\d.]+) km/h \| Time: (\d{2}:\d{2})"
)

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="test-logs/total.log", connection="AzureWebJobsStorage")
def insert_vehicles_to_cosmos(myblob: func.InputStream):
    logging.info(f"📥 Triggered by: {myblob.name} ({myblob.length} bytes)")

    content = myblob.read().decode("utf-8")
    if "=== Vehicle Details ===" not in content:
        logging.warning("⚠️ No vehicle details found in total.log")
        return

    details_section = content.split("=== Vehicle Details ===", 1)[-1].strip()
    lines = [line.strip() for line in details_section.splitlines() if line.strip()]

    added = 0
    for line in lines:
        match = vehicle_pattern.match(line)
        if match:
            vid, vtype, direction, speed, timestamp = match.groups()
            doc = {
                "id": vid,
                "vehicleId": vid,
                "type": vtype,
                "direction": direction,
                "speed": float(speed),
                "time": timestamp
            }
            cosmos_container.upsert_item(doc)
            added += 1

    logging.info(f"✅ Inserted {added} vehicles to Cosmos DB")
