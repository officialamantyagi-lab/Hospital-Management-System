import pymysql
import os

connection = pymysql.connect(
    host=os.environ.get("DB_HOST"),
    port=int(os.environ.get("DB_PORT")),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME"),
    ssl={
        "ca": "ca.pem"
    }
)

cursor = connection.cursor()

'''with open("HospitalDB.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cursor = connection.cursor()

for query in sql.split(";"):
    if query.strip():
        cursor.execute(query)

connection.commit()

print("Database imported successfully!")'''