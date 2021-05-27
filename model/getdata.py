import json
from .db import Mydb

with open("taipei-attractions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

data = data["result"]["results"]
# print(len(data)) 總計319筆

count = 0
for d in data:
    aid = d["_id"]
    name = d["stitle"]
    category = d["CAT1"]
    
    # 處理因為'單引號，引起的1064的error
    description = d["xbody"]
    if description.find("\'")!=-1 :
        description = description.replace("\'", "`")
    
    address = d["address"]
    transport = d["info"]
    mrt = d["MRT"]
    latitude = d["latitude"]
    longitude = d["longitude"]
    images = d["file"].split("http:")
    images_string = ""
    for img in images:
        if img.upper().endswith(".JPG") or img.upper().endswith(".PNG"):
            images_string += "http:"+img+" "
    #print(images_string)
    
    mydb = Mydb()
    try:
        mydb.insertAttractions(aid, name, category, description, address, transport, mrt, latitude, longitude, images_string)
        count+=1
    except Exception as e:
        print(e)
    del mydb

print(f"總計存入{count}筆") #應有319筆