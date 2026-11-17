import pymysql
import os

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    ssl={
        "ca": "ca.pem"
    }
)

cursor = connection.cursor()

with open("HospitalDB.sql", "r", encoding="utf-8") as f:
    sql = f.read()

for query in sql.split(";"):
    if query.strip():
        try:
            cursor.execute(query)
        except pymysql.err.ProgrammingError:
            pass
        except pymysql.err.OperationalError:
            pass

connection.commit()
cursor.close()
connection.close()

print("Database imported successfully!")