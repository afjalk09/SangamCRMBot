import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="kodama.proxy.rlwy.net",
        port=33948,
        user="root",
        password="juiHKpMkPxxHbqWPrspxQDkAybZOXQFk",
        database="railway"
    )