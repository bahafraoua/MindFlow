import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime
import streamlit as st

class FirebaseManager:
    """Firebase manager for MindFlow data storage"""
    
    def __init__(self):
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            if not firebase_admin._apps:
                service_account_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), 
                    'services', 
                    'mindflow-6b0b4-firebase-adminsdk-fbsvc-ffe846b06b.json'
                )
                
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                    self.db = firestore.client()
                    print("Firebase initialized successfully")
                else:
                    st.error("Firebase service account key not found")
                    return None
            else:
                self.db = firestore.client()
                
        except Exception as e:
            st.error(f"Error initializing Firebase: {str(e)}")
            return None

    def save_analysis(self, id,image, analysis_data, compression_info, analysis_type):
        try:
            if not self.db:
                return False
                
            doc_data = {
                'id': id,
                'image': image,
                'analysis_data': analysis_data,
                "compression_info": compression_info,
                'timestamp': datetime.now(),
            }

            doc_ref = self.db.collection(analysis_type).add(doc_data)
            return doc_ref[1].id
            
        except Exception as e:
            st.error(f"Error saving {analysis_type}: {str(e)}")
            return False


def get_firebase_manager():
    return FirebaseManager()