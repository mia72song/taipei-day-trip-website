from flask import make_response, session

from data.db import Mydb
from . import api

#取得當前已登入的使用者資訊api
@api.route("/user")
def get_current_user():
    pass

#註冊新用戶api
@api.route("/user", methods=["POST", ])
def signup():
    pass

#驗證登入api
@api.route("/user", methods=["PATCH", ])
def login():
    pass

#登出api
@api.route("/user", methods=["DELETE", ])
def logout():
    pass