import os

from common.database.firestore import FirestoreDatabase
from common.database.mongo import MongoDatabase

db = MongoDatabase() if os.getenv("ENVIRONMENT") == "local" else FirestoreDatabase()
