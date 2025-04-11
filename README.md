# Azure Function: Insert Vehicles to Cosmos DB

This is the **fourth component** of the *Vehicle Speed Calculation* project. It listens for the `total.log` file and inserts all vehicle details into **Azure Cosmos DB**.

## Trigger
Triggered automatically when `total.log` is uploaded to the `test-logs/` container in Azure Blob Storage.

## What It Does
- Parses the `=== Vehicle Details ===` section of `total.log`
- Extracts:
  - Vehicle ID
  - Type (e.g., car, truck)
  - Direction (Left/Right)
  - Speed
  - Time (hh:mm)
- Upserts each vehicle entry into the `vehicles` container in **Cosmos DB** (`traffic-db` database)

## Tech Stack
- Azure Functions (Python)
- Azure Blob Storage (trigger)
- Azure Cosmos DB (NoSQL)
- Regular Expressions for parsing
