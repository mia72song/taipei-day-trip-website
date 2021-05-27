from flask import request, jsonify, session
import uuid

from data.db import Mydb
from . import api

def pay_by_prime(prime, amout, number):
    partner_key = ""
    merchant_id = ""
    pass

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
            mydb.createOrder(order_data["prime"], order_data["price"], contact["name"], contact["email"], contact["phone"], number)
            mydb.bookingToOrder(order_data["prime"], order_data["orders"])
        except Exception as e:
            return jsonify({"error": True, "message":f"伺服器內部錯誤：{e}"}), 500
        
        del mydb
        return jsonify({"ok":True, "message":"Got It"}), 200
    else:
        return jsonify({"error": True, "message":"無資料"}), 500

#根據訂單編號取得訂單資訊
@api.route("/order/<orderNumber>")
def get_order(orderNumber):
    pass