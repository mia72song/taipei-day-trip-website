from flask import make_response, request, redirect
import json

from model.db import Mydb
from model.data_formatter import attractionsFormatter
from . import api

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
            results = mydb.getAttractionsByKeyword(keyword, start_index, pageSize)
            attractions = []
            if results :
                if len(results)==pageSize:
                    nextPage = page+1
                else:
                    nextPage = None
                for r in results :
                    data_dict = attractionsFormatter(r)
                    attractions.append(data_dict)
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
        results =  mydb.getAttractionsByPage(start_index, pageSize)
        attractions = []
        if results :
            if len(results)==pageSize :
                nextPage = page+1
            else:
                nextPage = None
            
            for r in results:
                data_dict = attractionsFormatter(r)
                attractions.append(data_dict)
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
        result = mydb.getAttractionById(attractionid)
        if result:
            data_dict = attractionsFormatter(result)
            body = json.dumps({"data":data_dict}, ensure_ascii=False, indent=2)
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
