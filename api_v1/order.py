from flask import request, jsonify, session
import uuid
import requests
import json
import os
import re
from dotenv import load_dotenv

from model.db import Mydb
from . import api

load_dotenv()

# pattern
email_pattern = r'^[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$'
phone_pattern = r'^09\d{8}$'

# TapPay
def pay_by_prime(number, prime, amout, contact):
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    partner_key = os.getenv("TAPPAY_PARTNET_KEY")
    merchant_id = os.getenv("TAPPAY_MERCHANT_ID")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": partner_key
    }
    post_data = json.dumps({
        "prime": prime,
        "partner_key": partner_key,
        "merchant_id": merchant_id,
        "details":"One Day Trip",
        "amount": amout,
        "bank_transaction_id":str(number),
        "cardholder": {
            "phone_number": "+886"+contact["phone"][1:],
            "name": contact["name"],
            "email": contact["email"]
        },
        "remember": False
    }, ensure_ascii=False, indent=2)
    response = requests.post(url, headers=headers, data=post_data)
    #print(response.json())
    resp_text = response.json()
    if resp_text["status"]==0:
        return int(resp_text["bank_transaction_id"])
    else:
        print(resp_text)
        return None

# 將由資料庫取得的預定行程列表(bookings)，整理成list格式
def paidBookingsFormatter(bookings):
    data_list=[]
    for b in bookings:
        if not b : break
        images = b[3].split(" ")
        reservation={
            "attraction": {
                "id":b[0],
                "name": b[1],
                "address": b[2],
                "image": images[0]
            },
            "date": b[4],
            "time": b[5],
            "price": b[6]
        }
        data_list.append(reservation)
    return data_list

# 建立新的訂單，並完成付款
@api.route("/orders", methods=["POST"])
def create_order():
    if not session.get("user_info"):
        return jsonify({"error": True, "message":{"login":False}}), 403

    order_data=request.get_json()
    if order_data:
        contact = order_data["contact"]
        if order_data["prime"]=="" or order_data["price"]=="":
            return jsonify({"error": True, "message":"付款失敗：付款資料有誤"}), 400

        if contact["name"]=="" or contact["email"]=="" or contact["phone"]=="":
            return jsonify({"error": True, "message":"付款失敗：聯絡資料不得為空值"}), 400

        email_check = re.match(contact["email"], email_pattern)
        phone_check = re.match(contact["phone"], phone_pattern)
        if not email_check or not phone_check:
            return jsonify({"error": True, "message":"付款失敗：聯絡資料有誤。"}), 400

        number = str(uuid.uuid1().time)[4:]
        mydb = Mydb()
        try:
            mydb.createOrder(number, order_data["prime"], order_data["price"], contact["name"], contact["email"], contact["phone"])
            mydb.bookingToOrder(number, order_data["orders"])
            number_for_success = pay_by_prime(number, order_data["prime"], order_data["price"], contact)
            if number_for_success:
                mydb.updatePaidOrder(number_for_success, order_data["orders"])
            else:
                return jsonify({"error": True, "message":f"訂單編號：{number}，信用卡付款失敗，請洽客服"}), 400
            
        except Exception as e:
            return jsonify({"error": True, "message":f"伺服器內部錯誤：{e}"}), 500
        
        del mydb
        resp_data = {
            "number": number_for_success,
            "payment": {
                "status": 0,
                "message": "付款成功"
            }
        }
        return jsonify({"data":resp_data}), 200
    else:
        return jsonify({"error": True, "message":"無資料"}), 500

# 根據訂單編號取得訂單資訊
@api.route("/order/<int:orderNumber>")
def get_order(orderNumber):
    if not session.get("user_info"):
        return jsonify({"error": True, "message":{"login":False}}), 403
    
    uid = session.get("user_info")[0]
    mydb = Mydb()
    paid_bookings = mydb.getBookingsByOrderNumber(uid, orderNumber)
    if paid_bookings:
        data_list = paidBookingsFormatter(paid_bookings)
        return jsonify({"data":data_list}), 200
    else:
        return jsonify({"data":None}), 200