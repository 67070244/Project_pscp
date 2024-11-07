"""
บอทพยากรณ์อากาศ เตือนให้พกร่ม
Function
-ดึงข้อความจาก line /
-reply ข้อความในไลน์ /
-ดึงข้อมูลสภาพอากาศ /
-notify เตือนพกร่มอัตโนมัติ /
-เพิ่มรายละเอียด function umbrella /
"""

from flask import Flask, request, abort
import requests
import json

app = Flask(__name__)
botid = "@736nacpz"
channel_secret = "f386a079fe2b14019432506b89fb2864"
line_access_token = "QVRlvdQy26KdOT8M0U9H6uY3jKqDfEAcO/3/7zL393n0B5mXOe14yr2/mhd9zIyzIeZwmEcv/2rhPZZkWhI6qm7YRFoz1difkx4POebgA+koA0quBBGHYUYr1mSopo/61pNIduEFDdGyRgx7gHIQwgdB04t89/1O/w1cDnyilFU="

def umbrella(weather):
    """ดูว่าต้องพกร่มและออกจากบ้านหรือไม่"""
    if weather in ("Rain", "Thunderstorm", "Drizzle"):
        if weather in ("Thunderstorm"):
            return "อย่าลืมพกร่มด้วย! (แนะนำว่าไม่ควรออกไปข้างนอก)"
        return "อย่าลืมพกร่มด้วย!"
    return ""

def get_weather(city):
    """ดึงข้อมูลอากาศของจังหวัด"""
    web_api = "33486d92c9ef8a538e08fb13351385e6" # api key from openweatherapi
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={web_api}&units=metric&lang=th"
    weather_info = requests.get(url).json()

    try:
        status = weather_info["weather"][0]["main"] #สภาพอากาศ
        description = weather_info["weather"][0]["description"] #รายละเอียดอากาศ
        noti = umbrella(status) #เตือนพกร่ม
        return f"{description}\n{noti}"
    except:
        return "ขอโทษด้วย เราไม่พบสถานที่ที่คุณต้องการทราบข้อมูล (กรุณาเช็คให้มั่นใจว่าได้เขียนชื่อเต็มแล้ว)"

@app.route("/webhook", methods=['POST','GET'])
def webhook():
    """Webhook"""
    if request.method == "POST":
        body = request.json
        reply_token = body['events'][0]['replyToken']
        text = body['events'][0]['message']['text']
        weather = get_weather(text)
        reply_message(reply_token, weather)
        return request.json, 200
    if request.method == "GET":
        return 200
    abort(400)

def reply_message(reply_token, message):
    """ส่ง text reply user"""
    line_api = "https://api.line.me/v2/bot/message/reply"
    auth = f"Bearer {line_access_token}"
    headers = {
        "Content-Type" : "application/json; charset=UTF-8",
        "Authorization" : auth
    }
    data = {
        "replyToken" : reply_token,
        "messages":[{
            "type":"text",
            "text": message
        }]
    }
    data = json.dumps(data)
    requests.post(line_api, headers=headers, data=data)
    return 200

if __name__ == "__main__":
    app.run(debug=True)
