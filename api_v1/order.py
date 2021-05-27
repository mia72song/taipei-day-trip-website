from flask import request, jsonify, session
import uuid
import requests
import json

from model.db import Mydb
from . import api

def pay_by_prime(number, prime, amout, contact):
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    partner_key = "partner_ktQgBPDeaOKAThHqAd3p16aBM9hMmqMqjcZKLPaUI2czNXeIYPvXMtGK"
    merchant_id = "mia72song_CTBC"
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
    #print(type(response.json()))
    resp_text = response.json()
    if resp_text["status"]==0:
        #print(resp_text)
        return int(resp_text["bank_transaction_id"])
    else:
        return None

#建立新的訂單，並完成付款
@api.route("/orders", methods=["POST"])
def create_order():
    if not session.get("user_info"):
        return jsonify({"error": True, "message":{"login":False}}), 403

    order_data=request.get_json()
    if order_data:
        print(order_data)
        contact = order_data["contact"]
        number = uuid.uuid1().time
        mydb = Mydb()
        try:
            mydb.createOrder(number, order_data["prime"], order_data["price"], contact["name"], contact["email"], contact["phone"])
            mydb.bookingToOrder(number, order_data["orders"])
            number_for_success = pay_by_prime(number, order_data["prime"], order_data["price"], contact)
            if number_for_success:
                mydb.updatePaidOrder(number, order_data["orders"])
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

#根據訂單編號取得訂單資訊
@api.route("/order/<orderNumber>")
def get_order(orderNumber):
    pass