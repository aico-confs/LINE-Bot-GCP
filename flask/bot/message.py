# -*- coding: utf8 -*-
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import datetime
#======自定義的函數庫==========
from weather import muti_data

#ImagemapSendMessage(組圖訊息)
def weather_predict(city):
    year = str(datetime.datetime.now().year)
    all_data = muti_data(city)
    city2id = dict([['太保市', '1001001'],
                    ['朴子市', '1001002'],
                    ['布袋鎮', '1001003'],
                    ['大林鎮', '1001004'],
                    ['民雄鄉', '1001005'],
                    ['溪口鄉', '1001006'],
                    ['新港鄉', '1001007'],
                    ['六腳鄉', '1001008'],
                    ['東石鄉', '1001009'],
                    ['義竹鄉', '1001010'],
                    ['鹿草鄉', '1001011'],
                    ['水上鄉', '1001012'],
                    ['中埔鄉', '1001013'],
                    ['竹崎鄉', '1001014'],
                    ['梅山鄉', '1001015'],
                    ['番路鄉', '1001016'],
                    ['大埔鄉', '1001017'],
                    ['阿里山鄉', '1001018']])
    return TemplateSendMessage(
                alt_text = city + '未來天氣預測',
                template = CarouselTemplate(
                    columns = [
                        CarouselColumn(
                            # thumbnail_image_url = 'https://i.imgur.com/Ex3Opfo.png',#https://i.imgur.com/NpYAJYK.png
                            title = f"{data['startTime']}\n ~ {data['endTime']}".replace('-', '/').replace(year+'/', ''),
                            text = f'天氣狀況：{data["天氣現象"]}\n溫度：{data["最低溫度"]} ~ {data["最高溫度"]} °C\n降雨機率：{data["12小時降雨機率"]}',
                            actions = [
                                URIAction(
                                    label = '詳細內容',
                                    uri = f'https://www.cwb.gov.tw/V8/C/W/Town/Town.html?TID={city2id[city]}'
                                )
                            ]
                        )for data in all_data[:10]
                    ]
                )
            )
def all_town():
    cities = ['大林鎮', '溪口鄉', '阿里山鄉', '梅山鄉', '新港鄉', '民雄鄉', '六腳鄉', '竹崎鄉', '東石鄉', '太保市', '番路鄉', '朴子市', '水上鄉', '中埔鄉', '布袋鎮', '鹿草鄉', '義竹鄉', '大埔鄉']
    height, width = 1040, 1040
    position = [(i, j) for j in [(height/6)*(h) for h in range(6)] for i in [(width/3)*(w) for w in range(3)]]
    action_data = list(zip(cities, position))
    message = ImagemapSendMessage(
        base_url="https://i.imgur.com/pR8lAX2.png?",
        alt_text='請選擇您要查詢的區域',
        base_size=BaseSize(height=height, width=width),
        actions=[MessageImagemapAction(
                text=data[0],
                area=ImagemapArea(
                    x=data[1][0], y=data[1][1], width=(width/3), height=(height/6)
                )
            ) for data in action_data]
    )
    return message
#關於LINEBOT聊天內容範例

