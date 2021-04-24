from flask import make_response, request, redirect
import json

from data.db import Mydb
from . import api

# 將已取得資料庫數據，整理成dict格式
def dictFormatter(result):
    images = result[9].split(" ")
    data = {
        "id":result[0],
        "name":result[1],
        "category":result[2],
        "description":result[3],
        "address":result[4],
        "transport":result[5],
        "mrt":result[6],
        "latitude":result[7],
        "longitude":result[8],
        "images":images[:len(images)-1]
    }
    return data

# 取得景點資料列表api
@api.route("/attractions")
def get_attractions():
    status_code = 0
    mydb = Mydb()
    pageSize = 12

    # 根據景點名稱的關鍵字篩選資料列表，未給定則不篩選(即不執行以下程序)
    if request.args.get("keyword"):
        keyword = request.args.get("keyword")
        page = request.args.get("page", 0)
        try:
            page = int(page)
            if page<0 :
                page = 0
        except ValueError:
            page = 0
        
        start_index = pageSize*page
        try:
            results = mydb.getDataByKeyword(keyword, start_index, pageSize)
            attractions = []
            if results :
                if len(results)==pageSize:
                    nextPage = page+1
                else:
                    nextPage = None
                for r in results :
                    data = dictFormatter(r)
                    attractions.append(data)
            else:
                nextPage = None
            
            status_code =200
            body = json.dumps({
                "nextPage":nextPage, 
                "data":attractions
            }, ensure_ascii=False, indent=2)
        
        except Exception as e:
            status_code = 500
            body = json.dumps({
                "error":True,
                "message":f"Server Error:{e}"
            }, ensure_ascii=False, indent=2)
        
        resp = make_response(body, status_code) # body應為json格式
        resp.headers["Content-Type"] = "application/json"
        return resp

    page = request.args.get("page", 0)
    try:
        page = int(page)
        if page<0 :
            return redirect("/api/attractions")
    except ValueError:
        return redirect("/api/attractions")

    start_index = pageSize*page
    try:
        results =  mydb.getDataByPage(start_index, pageSize)
        attractions = []
        if results :
            if len(results)==pageSize :
                nextPage = page+1
            else:
                nextPage = None
            
            for r in results:
                spot = dictFormatter(r)
                attractions.append(spot)
        else:
            nextPage = None
        
        status_code = 200
        body = json.dumps({
            "nextPage":nextPage,
            "data":attractions
        }, ensure_ascii=False, indent=2)
    
    except Exception as e:
        status_code = 500
        body = json.dumps({
            "error":True,
            "message":f"Server Error:{e}"
        }, ensure_ascii=False, indent=2)

    resp = make_response(body, status_code)  # body應為json格式
    resp.headers["Content-Type"] = "application/json"
    return resp

# 根據景點編號取得景點資料api
@api.route("/attraction/<int:attractionid>")
def get_attraction(attractionid):
    status_code = 0
    try:
        mydb = Mydb()
        result = mydb.getDataById(attractionid)
        if result:
            data = dictFormatter(result)
            body = json.dumps({"data":data}, ensure_ascii=False, indent=2)
            status_code = 200
        else:
            body = json.dumps({
                "error":True,
                "message":"Invalid Attraction Id"
            }, ensure_ascii=False, indent=2)            
            status_code = 400
    
    except Exception as e:
        body = json.dumps({
            "error":True,
            "message":f"Server Error：{e}"
        }, ensure_ascii=False, indent=2)
        status_code = 500
    
    resp = make_response(body, status_code)
    resp.headers["Content-Type"] = "application/json"
    return resp
