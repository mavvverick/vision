# settings.py
import os
import json

if not os.getenv("ML_HOST"):
    from os.path import join, dirname
    from dotenv import load_dotenv
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

HOST = os.getenv("ML_HOST")
FOLDER_PATH = os.getenv("FOLDER_PATH")
BUCKET_NAME = os.getenv("BUCKET_NAME")
CRED_JSON = os.getenv("CRED_JSON")
MAX_WORKERS = int(os.getenv("MAX_WORKERS"))
