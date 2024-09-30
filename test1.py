import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB URI
uri = "mongodb+srv://bao1712:bao1@cluster0.4qrdf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Load CSV data
csv_file_path = 'CB.csv'  
try:
    data = pd.read_csv(csv_file_path)
    print("CSV file loaded successfully!")
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit()


data_dict = data.to_dict(orient='records')

try:
    db = client['ca']  
    collection = db['caa']  
    # result = collection.insert_many(data_dict)
    # print(f"Data inserted successfully! Inserted IDs: {result.inserted_ids}")
    documents = collection.find()
    

    for doc in documents:
        print(doc)
except Exception as e:
    print(f"Error inserting data into MongoDB: {e}")
