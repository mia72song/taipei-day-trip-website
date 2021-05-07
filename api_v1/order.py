from flask import make_response

from data.db import Mydb
from . import api

#建立新的訂單，並完成付款
@api.route("/orders", methods=["POST", ])
def get_order_list():
    pass

#根據訂單編號取得訂單資訊
@api.route("/order/<orderNumber>")
def get_order(orderNumber):
    pass