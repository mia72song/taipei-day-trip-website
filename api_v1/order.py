from flask import request, jsonify, session

from data.db import Mydb
from . import api

#建立新的訂單，並完成付款
@api.route("/orders", methods=["POST"])
def create_order():
    if not session.get("user_info"):
        return jsonify({"error": True, "message":{"login":False}}), 403

    order_data=request.get_json()
    if order_data:
        print(order_data)
        return jsonify({"ok":True, "message":"Got It"}), 200
    else:
        return jsonify({"error": True, "message":"無資料"}), 500

#根據訂單編號取得訂單資訊
@api.route("/order/<orderNumber>")
def get_order(orderNumber):
    pass