import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

db_info = {
    "host":os.getenv("DB_HOST", default="localhost"),
    "port":3306,
    "user":os.getenv("DB_USER", default="root"),
    "password":os.getenv("DB_PASSWORD"),
    "database":os.getenv("DB_DATABASE"),
    "charset":"utf8"
}

class Mydb:
    def __init__(self, db_info=db_info):
        try:
            self.conn = pymysql.connect(
                host=db_info["host"], 
                port=db_info["port"],
                user=db_info["user"],
                password=db_info["password"],
                database=db_info["database"],
                charset=db_info["charset"]
            )
        except Exception as e:
            print(e)

        self.cur = self.conn.cursor()
        print("資料庫已開啟……")

    def insertAll(self, id, name, category, description, address, transport, mrt, latitude, longitude, images):
        sql = f'''INSERT INTO attractions VALUES (
            '{id}','{name}','{category}','{description}','{address}','{transport}','{mrt}','{latitude}','{longitude}','{images}'
        )'''
        self.cur.execute(sql)
        self.conn.commit()
        print("已存入")

    def getDataById(self, id):
        sql = f"SELECT * FROM attractions WHERE id={id}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data

    def getDataByPage(self, start_index, size):
        sql = f"SELECT * FROM attractions LIMIT {start_index}, {size}"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def getDataByKeyword(self, keyword, start_index, size):
        sql = f"SELECT * FROM attractions WHERE name LIKE '%{keyword}%' LIMIT {start_index}, {size}"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def __del__(self):
        self.cur.close()
        self.conn.close()
        print("資料庫已關閉!!")

if __name__ == "__main__":
    mydb = Mydb()
    result = mydb.getDataByKeyword("EFG", 36, 12)
    print(result)
    del mydb