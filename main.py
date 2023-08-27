from dotenv import dotenv_values
from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from routes.ledgerRoute import router as ledger_router

config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    try:
        app.mongodb_client = MongoClient(config["DB_URI"])
        app.database = app.mongodb_client[config["DB_NAME"]]
        print("Connected to the MongoDB database!")
    except (ConnectionError, ConnectionRefusedError, ConnectionFailure) as e:
        print("Failed to connect to the MongoDB database!")
        print(e)
    except:
        print("Unexcepted error occured")
        print(e)


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(ledger_router, tags=["ledgers"], prefix="/ledger")
