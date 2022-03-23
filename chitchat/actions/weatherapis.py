# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:johnsondiao
@File: weatherapis.py
@Time: 2022-03-23 15:29
@Desc:用心知天气数据查询天气
"""
import requests
import json

KEY = 'rmhrne8hal69uwyv'  # API key(私钥)
UID = ""  # 用户ID, TODO: 当前并没有使用这个值,签名验证方式将使用到这个值

LOCATION = 'beijing'  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
API = 'https://api.seniverse.com/v3/weather/daily.json'  # API URL，可替换为其他 URL
UNIT = 'c'  # 单位
LANGUAGE = 'zh-Hans'  # 查询结果的返回语言


def fetch_weather(location, start=0, days=15):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT,
        'start': start,
        'days': days
    }, timeout=2)
    return result.json()


def get_weather_by_day(location, day=1):
    result = fetch_weather(location)
    normal_result = {
        "location": result["results"][0]["location"],
        "result": result["results"][0]["daily"][day]
    }
    return normal_result


if __name__ == '__main__':
    default_location = "深圳"
    result = fetch_weather(default_location)
    print(json.dumps(result, ensure_ascii=False))

    default_location = "广州"
    result = get_weather_by_day(default_location)
    print(json.dumps(result, ensure_ascii=False))