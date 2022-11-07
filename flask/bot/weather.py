# -*- coding: utf8 -*-
import requests
import json


def get(city):
    #這裡記得換成剛剛生成的 Token
    token = 'CWB-6377D646-7082-4E10-B500-09DF91706F85' 
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-031?Authorization=' + token + '&format=JSON&locationName=' + str(city)
    Data = requests.get(url)
    if Data.status_code != 200:
        raise ValueError('Token錯誤')
    return Data.text

def single_data(city, kind ):
    # 可查詢的種類
    data = json.loads(get(city))
    data = data['records']['locations'][0]['location'][0]['weatherElement']
    categorys = [i['description'] for i in data]
    update_data = []
    for i in data[categorys.index(kind)]['time']:
        i[kind] = i['elementValue'][0]['value'] if i['elementValue'][0]['value'].strip() else '無資料'
        del i['elementValue']
        update_data +=[i]
    return update_data

def muti_data(city, kinds:list = ['天氣現象', '最低溫度', '最高溫度', '12小時降雨機率']):
    entries = [single_data(city, i) for i in kinds]
    data_length = len(entries[0])
    final_data = []
    for fd_num in range(data_length):
        empty_dict = dict()
        for entry in entries:
            empty_dict.update(entry[fd_num])
        final_data +=[empty_dict]
    return final_data
            
        