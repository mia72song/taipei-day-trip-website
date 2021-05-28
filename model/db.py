import pymysql
import os
from werkzeug.security import generate_password_hash, check_password_hash
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

    def insertAttractions(self, id, name, category, description, address, transport, mrt, latitude, longitude, images):
        sql = f'''INSERT INTO attractions VALUES (
            '{id}','{name}','{category}','{description}','{address}','{transport}','{mrt}','{latitude}','{longitude}','{images}'
        )'''
        self.cur.execute(sql)
        self.conn.commit()
        print("已存入")

    def getAttractionById(self, id):
        sql = f"SELECT * FROM attractions WHERE id={id}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data

    def getAttractionsByPage(self, start_index, size):
        sql = f"SELECT * FROM attractions LIMIT {start_index}, {size}"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def getAttractionsByKeyword(self, keyword, start_index, size):
        sql = f"SELECT * FROM attractions WHERE name LIKE '%{keyword}%' LIMIT {start_index}, {size}"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def emailExists(self, email):
        sql = f"SELECT * FROM users WHERE email='{email}'"
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False

    def createUser(self, username, email, password):
        if not self.emailExists(email):
            password_hash = generate_password_hash(password)
            sql = f"INSERT INTO users (username, email, password) VALUES ('{username}','{email}','{password_hash}')"
            self.cur.execute(sql)
            self.conn.commit()
            print("新用戶已寫入")
        else:
            print("此email已註冊過")
    
    def getUser(self, email, password):
        sql = f"SELECT id, username, email, password FROM users WHERE email='{email}'"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        # print(data)
        if data and check_password_hash(data[3], password):
            return data[0], data[1], data[2]
        else:
            return None

    def updatePassword(self, email, password, username=None, phone=None):
        password_hash = generate_password_hash(password)
        sql=f"UPDATE users SET password='{password_hash}' WHERE email='{email}'"
        self.cur.execute(sql)
        self.conn.commit()
        print("密碼已更新")

    def createBooking(self, aid, date, period, price, uid):
        sql=f'''INSERT INTO bookings (date, period, price, attraction_id, user_id) 
            VALUES ('{date}', '{period}', {price}, {aid}, {uid})'''
        self.cur.execute(sql)
        self.conn.commit()
        print("預定行程已新增")

    def getBookingsByUserId(self, uid):
        sql=f'''SELECT b.id,
            a.id, a.name, a.address, a.images, 
            b.date, b.period, b.price
            FROM bookings AS b
            INNER JOIN attractions as a ON b.attraction_id=a.id 
            WHERE b.user_id={uid} and paid_order_number IS NULL
            ORDER BY create_datetime desc'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def delBookingById(self, bid, uid):
        paid = self.__bookingPaid(bid)
        if paid:
            print(f"編號：{bid} 付款完成，不可刪除")
        else:
            sql=f"DELETE FROM bookings WHERE id={bid} and user_id={uid} and paid_order_number IS NULL"
            self.cur.execute(sql)
            self.conn.commit()
            print(f"編號：{bid} 已刪除")

    def __bookingPaid(self, bid):
        sql=f"SELECT * FROM bookings WHERE paid_order_number IS NOT NULL and id={bid}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data
    
    def createOrder(self, number, prime, amount, contact_name, contact_email, contact_phone):
        sql=f'''INSERT INTO orders (number, prime, amount, contact_name, contact_email, contact_phone)
            VALUES ({number}, '{prime}', {amount}, '{contact_name}', '{contact_email}', '{contact_phone}')'''
        self.cur.execute(sql)
        self.conn.commit()
        print("待付款訂單已建立")

    def updatePaidOrder(self, number, booking_list):
        if booking_list!=[] and number:
            sql_order=f"UPDATE orders SET paid=1, update_datetime=NOW() WHERE number={number}"
            self.cur.execute(sql_order)
            self.conn.commit()
            for bid in booking_list:
                sql_booking=f"UPDATE bookings SET paid_order_number={number}, update_datetime=NOW() WHERE id={bid}"
                self.cur.execute(sql_booking)
                self.conn.commit()
            print(f"訂單編號{number}已付款完成。")

    def bookingToOrder(self, number, booking_list):
        for bid in booking_list:
            sql=f"INSERT INTO booking_to_order (booking_id, order_number) VALUES ({bid}, {number})"
            self.cur.execute(sql)
            self.conn.commit()
        print(f"訂單編號{number}中繼表建立完成")

    def getBookingsByOrderNumber(self, uid, number):
        sql=f'''SELECT a.id, a.name, a.address, a.images,
            b.date, b.period, b.price
            FROM bookings AS b
            INNER JOIN attractions AS a ON b.attraction_id=a.id
            WHERE b.user_id={uid} and b.paid_order_number={number}
            ORDER BY create_datetime desc'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def __del__(self):
        self.cur.close()
        self.conn.close()
        print("資料庫已關閉!!")

if __name__ == "__main__":
    mydb = Mydb()
    data = mydb.getBookingsByOrderNumber(1, 14839455960560)
    print(data)
    del mydb