//https://weather.yahoo.co.jp/weather/jp/26/6110.html
//https://ishi-tech.biz/python-scraping-yahoo-weather/

import requests
from datetime import datetime

def GetYahooWeather(AreaCode):
    url = "https://weather.yahoo.co.jp/weather/jp/26/"+str(AreaCode)+".html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    rs = soup.find(class_='forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    return rs[0] + "の天気は" +rs[1] + "、明日の天気は" + rs[19]+"です。"

GetYahooWeather("6110")
