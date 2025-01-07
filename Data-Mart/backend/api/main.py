import asyncio
from databases import Database
import datetime
from fastapi import FastAPI

app = FastAPI()

# Verbindungs-URL für die Hauptdatenbank
MAIN_DB_URL = "postgresql://admin:Kennwort1@localhost/datawarehouse" 5432
# Verbindungs-URL für die Data Mart-Datenbank
DATAMART_DB_URL = "postgresql://user:password@localhost/datamart" 

# Initialisiere Datenbankverbindungen
main_db = Database(MAIN_DB_URL)
datamart_db = Database(DATAMART_DB_URL)

# Beispiel für das Abrufen von Wahldaten aus der Hauptdatenbank
async def fetch_election_data():
    query = "SELECT district_code, date, övp_votes, spö_votes, fpö_votes, grüne_votes, neos_votes, other_votes FROM election_data"
    result = await main_db.fetch_all(query)
    return result

# Beispiel für das Einfügen der Daten in die Data Mart-Datenbank
async def insert_election_data(data):
    query = """
    INSERT INTO election_fact (district_code, date, övp_votes, spö_votes, fpö_votes, grüne_votes, neos_votes, other_votes)
    VALUES (:district_code, :date, :övp_votes, :spö_votes, :fpö_votes, :grüne_votes, :neos_votes, :other_votes)
    """
    for row in data:
        await datamart_db.execute(query, values=row)

# Asynchrone Synchronisierungsfunktion
async def sync_data():
    # Fetch data from main database
    election_data = await fetch_election_data()

    # Insert data into Data Mart database
    await insert_election_data(election_data)

# Endpoint zum Starten der Synchronisierung
@app.get("/sync-data")
async def sync_data_endpoint():
    await sync_data()
    return {"message": "Data synchronized successfully"}

# Eventuelle asynchrone Aufgaben im Hintergrund starten
async def sync_periodically():
    while True:
        await sync_data()
        await asyncio.sleep(300)  # Alle 5 Minuten synchronisieren

# Starte die asynchrone Synchronisierung beim Starten der Anwendung
@app.on_event("startup")
async def startup():
    await main_db.connect()
    await datamart_db.connect()
    asyncio.create_task(sync_periodically())  # Periodische Synchronisierung starten

@app.on_event("shutdown")
async def shutdown():
    await main_db.disconnect()
    await datamart_db.disconnect()

