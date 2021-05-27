from flask import make_response, request, jsonify, session
import json

from data.db import Mydb
from . import api

def dataFormatter(bookings):
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

#取得尚未確認下單的預定行程列表
@api.route("/booking")
def get_booking_list():
    if session.get("user_info"):
        uid = session.get("user_info")[0]
        mydb = Mydb()
        bookings = mydb.getBookingsByUserId(uid)
        if bookings:
            data_list = dataFormatter(bookings)
            return jsonify({"data":data_list}), 200
        else:
            return jsonify({"data":None}), 200
        
    else:
        return jsonify({"error": True, "message":{"login":False}}), 403

#預定新行程
@api.route("/booking", methods=["POST"])
def create_booking():
    if session.get("user_info"):
        reservation = request.get_json()
        user_info = session.get("user_info")
    else:
        return jsonify({"error": True, "message":{"login":False}}), 403
    
    if reservation:
        # print(reservation)
        # print(user_info)
        if reservation["attractionId"]=="" or reservation["date"]=="" or reservation["time"]=="" or reservation["price"]=="":
            return jsonify({"error": True, "message":"預定資料不完整"}), 400
        else:
            mydb = Mydb()
            try:
                mydb.createBooking(reservation["attractionId"], reservation["date"], reservation["time"], reservation["price"], user_info[0])
            except Exception as e:
                return jsonify({"error": True, "message":f"伺服器內部錯誤:{e}"}), 500
            
            del mydb
            return jsonify({"ok": True}), 200
    else:
        return jsonify({"error": True, "message":"無資料"}), 500

#刪除目前的預定行程
@api.route("/booking", methods=["DELETE"])
def delete_booking():
    if session.get("user_info"):
        del_data = request.get_json()  # 前端傳來booking的id
        mydb = Mydb()
        mydb.delBookingById(del_data["bid"], session.get("user_info")[0])
        del mydb
        return jsonify({"ok": True}), 200
    else:
        return jsonify({"error": True, "message":{"login":False}}), 403