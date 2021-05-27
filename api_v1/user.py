from flask import request, jsonify, make_response, session

from model.db import Mydb
from . import api

#取得當前已登入的使用者資訊api
@api.route("/user")
def get_current_user():
    current_user = session.get("user_info")
    if current_user:
        return make_response(jsonify({
            "data":{
                "id":current_user[0],
                "name":current_user[1],
                "email":current_user[2]
            }
        }), 200)
    else:
        return make_response(jsonify({"data":None}), 200)

#註冊新用戶api
@api.route("/user", methods=["POST"])
def signup():
    signup_data = request.get_json()
    if signup_data:
        if signup_data["name"]=="" or signup_data["email"]=="" or signup_data["password"]=="":
            return make_response(
                jsonify({
                    "error": True,
                    "message": "資料皆不得為空值"
                }), 400
            )
        mydb = Mydb()
        if mydb.emailExists(signup_data["email"]):
            return make_response(
                jsonify({
                    "error": True,
                    "message": "此Email已註冊過"
                }), 400
            )
        else:
            try:
                mydb.createUser(signup_data["name"], signup_data["email"], signup_data["password"])
            except Exception as e:
                return make_response(jsonify({
                    "error":True,
                    "message":f"伺服器內部錯誤:{e}"
                }), 500)
            del mydb
            return make_response(jsonify({"ok": True}), 200)
    else:
        return make_response(
            jsonify({
                "error": True,
                "message": "無資料"
            }), 500
        )

#驗證登入api
@api.route("/user", methods=["PATCH"])
def login():
    login_data = request.get_json()
    if login_data:
        if login_data["email"]=="" or login_data["password"]=="":
            return make_response(
                jsonify({
                    "error": True,
                    "message": "資料皆不得為空值"
                }), 400
            )
        
        try:
            mydb = Mydb()
            user_info = mydb.getUser(login_data["email"], login_data["password"])
        except Exception as e:
            return make_response(jsonify({
                "error":True,
                "message":f"伺服器內部錯誤:{e}"
            }), 500)
        
        if user_info:
            session["user_info"] = user_info
            return make_response(
                jsonify({"ok": True}), 200
            )
        else:
            return make_response(
                jsonify({
                    "error": True,
                    "message": "帳號或密碼錯誤"
                }), 400
            )
    else:
        return make_response(
            jsonify({
                "error": True,
                "message": "無資料"
            }), 500
        )

#登出api
@api.route("/user", methods=["DELETE"])
def logout():
    if session.get("user_info"):
        del session["user_info"]
    return make_response(jsonify({"ok":True}), 200)