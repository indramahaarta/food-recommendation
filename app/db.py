import firebase_admin
from firebase_admin import credentials, firestore
from app.config import get_settings

settings = get_settings()

cred = credentials.Certificate(settings.firebase_config_path)
firebase_admin.initialize_app(cred)
db = firestore.client()