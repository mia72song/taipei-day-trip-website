# 將由資料庫取得的景點(attractions)，整理成dict格式
def attractionsFormatter(result):
    cols = ["id", "name", "category", "description", "address", "transport", "mrt", "latitude", "longitude", "images"]
    data_dict = dict(zip(cols, result))
    images = result[9].split(" ")
    data_dict["images"] = images[:-1]
    return data_dict

# 將由資料庫取得的預定行程列表(bookings)，整理成list格式
def bookingsFormatter(bookings):
    data_list=[]
    for b in bookings:
        if not b : break
        images = b[4].split(" ")
        reservation={
            "booking_id":b[0],
            "attraction": {
                "id": b[1],
                "name": b[2],
                "address": b[3],
                "image": images[0]
            },
            "date": b[5],
            "time": b[6],
            "price": b[7]
        }
        data_list.append(reservation)
    return data_list