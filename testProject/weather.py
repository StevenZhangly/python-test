__author__ = 'Zhangly'

import requests

key = '&key=6ceb9e62da2142fca3f1b0b86937ffd1'
url_api_weather = 'https://devapi.qweather.com/v7/weather/'


def getWeather(api_type, location, is_proxy):
    target_url = url_api_weather + api_type + '?location=' + location + key
    resp = ''
    if is_proxy:
        proxy = '10.36.0.254:1080'
        proxies = {
            'http': 'socks5://' + proxy,
            'https': 'socks5://' + proxy
        }
        resp = requests.get(target_url, proxies=proxies)
    else:
        resp = requests.get(target_url)
    print('返回结果:%s' % resp.json())
    return resp.json()


if __name__ == '__main__':
    weather_info = getWeather('now', '101280605', 1)
    print('当前气温:%s℃，天气状况:%s，风向:%s' % (weather_info['now']['temp'], weather_info['now']['text'], weather_info['now']['windDir']))
