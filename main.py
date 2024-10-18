"""บอทพยากรณ์อากาศ เตือนให้พกร่ม"""
from flask import Flask, request, abort
import requests
import json

app = Flask(__name__)
botid = "@736nacpz"
channel_secret = "f386a079fe2b14019432506b89fb2864"
line_access_token = "QVRlvdQy26KdOT8M0U9H6uY3jKqDfEAcO/3/7zL393n0B5mXOe14yr2/mhd9zIyzIeZwmEcv/2rhPZZkWhI6qm7YRFoz1difkx4POebgA+koA0quBBGHYUYr1mSopo/61pNIduEFDdGyRgx7gHIQwgdB04t89/1O/w1cDnyilFU="

def get_weather(city):
    """ดึงข้อมูลอากาศของจังหวัด"""
    web_api = "33486d92c9ef8a538e08fb13351385e6" # api key from openweatherapi
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={web_api}"
    req = requests.get(url).json()

    temp = req["main"]["temp"] #get temperature
    return f"{city}'s temp = {temp}"

@app.route("/webhook", methods=['POST','GET'])
def webhook():
    """Webhook"""
    if request.method == "POST":
        body = request.json
        print(body)
        replyToken = body['events'][0]['replyToken']
        text = body['events'][0]['message']['text']
        weather = get_weather(text)
        print(weather)
        reply_message(replyToken, weather)
        return request.json, 200
    if request.method == "GET":
        return 200
    abort(400)

def reply_message(replyToken, message):
    """ส่ง text reply user"""
    line_api = "https://api.line.me/v2/bot/message/reply"
    auth = f"Bearer {line_access_token}"
    print(auth)
    headers = {
        "Content-Type" : "application/json; charset=UTF-8",
        "Authorization" : auth
    }
    data = {
        "replyToken" : replyToken,
        "messages":[{
            "type":"text",
            "text": message
        }]
    }
    data = json.dumps(data)
    r = requests.post(line_api, headers=headers, data=data)
    print(r)

    return 200

if __name__ == "__main__":
    app.run(debug=True)
