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

    def save_analysis(self, user_id, analysis_id, image, analysis_data, compression_info, analysis_type):
        """
        Save analysis data to user's subcollection
        
        Structure: users/{user_id}/analysis/{analysis_id}
        
        Args:
            user_id: Unique user identifier
            analysis_id: Unique analysis identifier 
            image: Base64 encoded image
            analysis_data: Analysis results
            compression_info: Image compression metadata
            analysis_type: Type of analysis (facial_analysis, handwriting_analysis)
        """
        try:
            if not self.db:
                st.error("Firebase not initialized")
                return False
                
    
            doc_data = {
                'analysis_id': analysis_id,
                'image': image,
                'analysis_data': analysis_data,
                'compression_info': compression_info,
                'analysis_type': analysis_type,
                'timestamp': datetime.now(),
            }


            doc_ref = self.db.collection('users').document(user_id).collection('analysis').document(analysis_id)
            doc_ref.set(doc_data)
            
            return True
            
        except Exception as e:
            st.error(f"Error saving analysis: {str(e)}")
            return False

    def get_user_analyses(self, user_id, analysis_type=None):
        """
        Retrieve all analyses for a specific user
        
        Args:
            user_id: Unique user identifier
            analysis_type: Optional filter by analysis type
            
        Returns:
            List of analysis documents
        """
        try:
            if not self.db:
                return []
                
            query = self.db.collection('users').document(user_id).collection('analysis')
            
            if analysis_type:
                query = query.where('analysis_type', '==', analysis_type)
                
            docs = query.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
            
            analyses = []
            for doc in docs:
                data = doc.to_dict()
                data['doc_id'] = doc.id
                analyses.append(data)
                
            return analyses
            
        except Exception as e:
            st.error(f"Error retrieving analyses: {str(e)}")
            return []

    def delete_user_analysis(self, user_id, analysis_id):
        """
        Delete a specific analysis for a user
        
        Args:
            user_id: Unique user identifier
            analysis_id: Analysis document ID to delete
        """
        try:
            if not self.db:
                return False
                
            doc_ref = self.db.collection('users').document(user_id).collection('analysis').document(analysis_id)
            doc_ref.delete()
            
            st.success(f"✅ Analysis {analysis_id} deleted")
            return True
            
        except Exception as e:
            st.error(f"Error deleting analysis: {str(e)}")
            return False


def get_firebase_manager():
    return FirebaseManager()