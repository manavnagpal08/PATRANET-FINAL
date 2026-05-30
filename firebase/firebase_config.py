import os
import streamlit as st

# Force local mock mode to ensure 100% free offline operations without Firebase cloud billing
is_mock = True
db = None
bucket = None

def initialize_firebase():
    global db, bucket, is_mock
    # Operating strictly in local Mock DB/Storage mode for free hackathon usage
    return None, None, True

# Self-initialize
db, bucket, is_mock = initialize_firebase()

