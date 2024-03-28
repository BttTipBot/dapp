
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK (replace 'path/to/your/credentials.json' with your actual credentials file)
cred = credentials.Certificate('db/firebase.json')
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()


    
