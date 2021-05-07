from flask import make_response

from data.db import Mydb
from . import api

#取得尚未確認下單的預定行程列表
@api.route("/booking")
def get_booking_list():
    pass

#預定新行程
@api.route("/booking", methods=["POST", ])
def create_booking():
    pass

#刪除目前的預定行程
@api.route("/booking", methods=["DELETE", ])
def delete_booking():
    pass