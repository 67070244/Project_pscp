#บอทพยากรณ์อากาศ เตือนให้พกร่ม
import requests

city = "Udon Thani" #input
api = "33486d92c9ef8a538e08fb13351385e6" #api key from openweatherapi
def get_weather(api, city):
    #ดึงข้อมูลอากาศของจังหวัด
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
    req = requests.get(url).json()
    print(req)
    
    temp = req["main"]["temp"] #get temperature
    print(temp)
    #print(req)
    
get_weather(api, city)
