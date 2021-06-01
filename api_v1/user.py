from flask import request, jsonify, session
import re

from model.db import Mydb
from . import api

# pattern
email_pattern = r'^[\w.-]+@[^@\s]+\.[a-zA-Z]{2,10}$'
pwd_pattern = r'^[A-Za-z0-9]{4,}$'  # 4碼以上英數字

# 取得當前已登入的使用者資訊api
@api.route("/user")
def get_current_user():
    current_user = session.get("user_info")
    if current_user:
        return jsonify({
            "data":{
                "id":current_user[0],
                "name":current_user[1],
                "email":current_user[2]
            }
        }), 200
    else:
        return jsonify({"data":None}), 200

# 註冊新用戶api
@api.route("/user", methods=["POST"])
def signup():
    signup_data = request.get_json()
    if signup_data:
        if signup_data["name"]=="" or signup_data["email"]=="" or signup_data["password"]=="":
            return jsonify({
                "error": True,
                "message": "資料皆不得為空值"
            }), 400
        
        email_check = re.match(email_pattern, signup_data["email"])
        pwd_check = re.match(pwd_pattern, signup_data["password"])
        if not email_check or not pwd_check:
            return jsonify({
                "error":True, 
                "message":"資料格式(Email或密碼)有誤"
            }), 400
        
        mydb = Mydb()
        if mydb.emailExists(signup_data["email"]):
            return jsonify({
                "error": True,
                "message": "此Email已註冊過"
            }), 400
        else:
            try:
                mydb.createUser(signup_data["name"], signup_data["email"], signup_data["password"])
            except Exception as e:
                return jsonify({
                    "error":True,
                    "message":f"伺服器內部錯誤:{e}"
                }), 500
            del mydb
            return jsonify({"ok": True}), 200
    else:
        return jsonify({
            "error": True,
            "message": "無資料"
        }), 500

# 驗證登入api
@api.route("/user", methods=["PATCH"])
def login():
    login_data = request.get_json()
    if login_data:
        if login_data["email"]=="" or login_data["password"]=="":
            return jsonify({
                "error": True,
                "message": "資料皆不得為空值"
            }), 400
        
        pwd_check = re.match(pwd_pattern, login_data["password"])
        if len(login_data["password"])<4 or not pwd_check:
            return jsonify({
                "error": True,
                "message": "Email或密碼輸入錯誤"
            }), 400
        
        try:
            mydb = Mydb()
            user_info = mydb.getUser(login_data["email"], login_data["password"])
        except Exception as e:
            return jsonify({
                "error":True,
                "message":f"伺服器內部錯誤:{e}"
            }), 500
        
        if user_info:
            session["user_info"] = user_info
            return jsonify({"ok": True}), 200

        else:
            return jsonify({
                "error": True,
                "message": "Email或密碼輸入錯誤"
            }), 400
    else:
        return jsonify({
            "error": True,
            "message": "無資料"
        }), 500

# 登出api
@api.route("/user", methods=["DELETE"])
def logout():
    if session.get("user_info"):
        del session["user_info"]
    return jsonify({"ok":True}), 200