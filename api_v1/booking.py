from flask import request, jsonify, session
import re
from datetime import datetime

from model.db import Mydb
from . import api

# pattern
price = {"morning":2000, "afternoon":2500}

# 將由資料庫取得的預定行程列表(bookings)，整理成list格式
def bookingsFormatter(bookings):
    data_list=[]
    for b in bookings:
        if not b : break
        images = b[4].split(" ")
        reservation={
            "booking_id":b[0],
            "attraction": {
                "id": b[1],
                "name": b[2],
                "address": b[3],
                "image": images[0]
            },
            "date": b[5],
            "time": b[6],
            "price": b[7]
        }
        data_list.append(reservation)
    return data_list

# 取得尚未確認下單的預定行程列表
@api.route("/booking")
def get_booking_list():
    if not session.get("user_info"):
        return jsonify({"error": True, "message":{"login":False}}), 403

    uid = session.get("user_info")[0]
    mydb = Mydb()
    bookings = mydb.getBookingsByUserId(uid)
    if bookings:
        data_list = bookingsFormatter(bookings)
        return jsonify({"data":data_list}), 200
    else:
        return jsonify({"data":None}), 200

# 預定新行程
@api.route("/booking", methods=["POST"])
def create_booking():
    if not session.get("user_info"):
        return jsonify({"error": True, "message":{"login":False}}), 403

    reservation = request.get_json()
    user_info = session.get("user_info")     
    if reservation:
        if reservation["attractionId"]=="" or reservation["date"]=="" or reservation["time"]=="" or reservation["price"]=="":
            return jsonify({"error": True, "message":"預定資料不完整"}), 400

        # 可預約日期驗證
        today = datetime.now().date() #<class 'datetime.date'>
        try:
            date = datetime.strptime(reservation["date"], "%Y-%m-%d").date() #<class 'datetime.date'>
            if today>=date :
                return jsonify({"error": True, "message":"非可供預約日期"}), 400
        except ValueError:
            return jsonify({"error": True, "message":"預定資料格式錯誤"}), 400
        
        # 時段及價格比對驗證
        if reservation["time"] not in price.keys() or price.get(reservation["time"])!=reservation["price"]:
            return jsonify({"error": True, "message":"預定資料格式錯誤"}), 400
                
        try:
            mydb = Mydb()
            mydb.createBooking(reservation["attractionId"], reservation["date"], reservation["time"], reservation["price"], user_info[0])
        except Exception as e:
            return jsonify({"error": True, "message":f"伺服器內部錯誤:{e}"}), 500
        
        del mydb
        return jsonify({"ok": True}), 200
    else:
        return jsonify({"error": True, "message":"無資料"}), 500

# 刪除目前的預定行程
@api.route("/booking", methods=["DELETE"])
def delete_booking():
    if not session.get("user_info"):
        return jsonify({"error": True, "message":{"login":False}}), 403

    del_data = request.get_json()  # 前端傳來booking的id
    mydb = Mydb()
    mydb.delBookingById(del_data["bid"], session.get("user_info")[0])
    del mydb
    return jsonify({"ok": True}), 200