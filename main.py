import logging
from os import environ
import io

import openai
import pg8000
import sqlalchemy
from flask import Flask, request
from flask_cors import CORS
from google.cloud import storage
from google.cloud.sql.connector import Connector, IPTypes
from openai import OpenAI
from sqlalchemy import UUID, Column, MetaData, String, Table

app = Flask(__name__)
CORS(app)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROJECT_ID = environ.get("PROJECT_ID")
BUCKET_NAME = environ.get("BUCKET_NAME")


def generate_image():
    """ """

    prompt = ""
    open_ai_client = OpenAI()
    try:
        response = open_ai_client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        print(response.data[0].url)

    except openai.OpenAIError as e:
        print(e.http_status)
        print(e.error)


def read_and_return_image(image_name):
    storage_client = storage.Client(PROJECT_ID)
    file_obj = io.BytesIO()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.get_blob(f"images/{image_name}")
    blob.download_to_file(file_obj)
    file_obj.seek(0)
    return file_obj


def connect_to_db():
    db_user = environ.get("DB_USER")
    db_pass = environ.get("DB_PASS")
    db_name = environ.get("DB_NAME")
    connection_name = environ.get("CONNECTION_NAME")
    ip_type = IPTypes.PUBLIC

    connector = Connector()

    def getconn():
        conn: pg8000.dbapi.Connection = connector.connect(
            connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,  # 30 seconds
        pool_recycle=1800,  # 30 minutes
    )
    return pool

# 
# Run db migration while bringing app online.
# 

db = connect_to_db()
metadata_obj = MetaData()

game_table = Table(
    "games",
    metadata_obj,
    Column("game_guid", UUID),
    Column("user_id", String),
    Column("displayed_image", String),
    Column("generated_image", String),
    Column("description", String),
    Column(
        "timestamp",
    ),
)
metadata_obj.create_all()