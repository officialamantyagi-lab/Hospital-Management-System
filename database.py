import pymysql

connection = pymysql.connect(
    host="mysql-307d0e1b-officialamantyagi-ddf6.i.aivencloud.com",
    port=13155,
    user="avnadmin",
    password="",
    database="HospitalDB",
    ssl={
        "ca": r"C:\Users\neha tyagi\Downloads\ca.pem"
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