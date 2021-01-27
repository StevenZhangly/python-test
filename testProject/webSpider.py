import requests
import pandas as pd
from bs4 import BeautifulSoup
import pymysql
import sshtunnel
import time


def sqlQueryFetchone(sql):
    # 使用sshtunnel跳转访问外网
    with sshtunnel.SSHTunnelForwarder(
            ('10.37.20.204', 22),
            ssh_username='admin',
            ssh_password='admin1234',
            remote_bind_address=('rm-wz9ol46kro5h2gbjqzo.mysql.rds.aliyuncs.com', 3306),
            local_bind_address=('127.0.0.1', 13306)
    ) as tunnel:
        # 打开数据库连接
        db = pymysql.connect(host="127.0.0.1", port=13306, user="zly", password="zly_1988", charset="utf8",
                             database="testdb")
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        print("Database version : %s" % result)
        db.close()


def sqlQueryFetchall(sql):
    # 使用sshtunnel跳转访问外网
    with sshtunnel.SSHTunnelForwarder(
            ('10.37.20.204', 22),
            ssh_username='admin',
            ssh_password='admin1234',
            remote_bind_address=('rm-wz9ol46kro5h2gbjqzo.mysql.rds.aliyuncs.com', 3306),
            local_bind_address=('127.0.0.1', 13306)
    ) as tunnel:
        # 打开数据库连接
        db = pymysql.connect(host="127.0.0.1", port=13306, user="zly", password="zly_1988", charset="utf8",
                             database="testdb")
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
        db.close()

def sqlExecute(sql, params, type):
    # 使用sshtunnel跳转访问外网
    with sshtunnel.SSHTunnelForwarder(
            ('10.37.20.204', 22),
            ssh_username='admin',
            ssh_password='admin1234',
            remote_bind_address=('rm-wz9ol46kro5h2gbjqzo.mysql.rds.aliyuncs.com', 3306),
            local_bind_address=('127.0.0.1', 13306)
    ) as tunnel:
        # 打开数据库连接
        db = pymysql.connect(host="127.0.0.1", port=13306, user="zly", password="zly_1988", charset="utf8",
                             database="testdb")
        cursor = db.cursor()
        if type == 'fetchone':
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
        elif type == 'fetchall':
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                print(row)
        elif type == 'executemany':
            result = cursor.executemany(sql, params)
            print(result)
        else:
            result = cursor.execute(sql, params)
            print(result)
        db.commit()
        db.close()


if __name__ == '__main__':
    #target = 'http://www.tianqihoubao.com/lishi/shenzhen/month/202012.html'
    target = 'http://www.tianqihoubao.com/weather/top/shenzhen.html'
    proxy = '10.36.0.254:1080'
    proxies = {
        'http': 'socks5://' + proxy,
        'https': 'socks5://' + proxy
    }
    # 获取网页源代码
    resp = requests.get(target, proxies=proxies)
    html = resp.content.decode('gbk')
    # 数据提取
    soup = BeautifulSoup(html, 'html.parser')
    tr_list = soup.find_all('tr')

    dates, conditions, temps, winds, params = [], [], [], [], []
    for data in tr_list[2:]:
        sub_data = data.text.split()
        print(sub_data)
        #print(time.strftime("%Y-%m-%d", time.strptime(sub_data[0], '%Y年%m月%d日')))
        date = sub_data[1]
        weather = sub_data[2]+'/'+sub_data[6]
        temp = sub_data[5]+'/'+sub_data[9]
        wind = sub_data[3]+sub_data[4]+'/'+sub_data[7]+sub_data[8]
        dates.append(date)
        conditions.append(weather)
        temps.append(temp)
        winds.append(wind)
        params.append((date, weather, temp, wind))
    _data = pd.DataFrame()
    _data['日期'] = dates
    _data['天气情况'] = conditions
    _data['气温'] = temps
    _data['风力风向'] = winds
    print(_data)

    # sqlExecute("SELECT VERSION()", '', 'fetchone')
    #
    # print(params)
    insertSql = "INSERT INTO `t_weather`( `date` , `weather` , `temperature` , `wind` , `createtime` , `remark` ) VALUES (%s, %s, %s, %s, SYSDATE(), '')"
    sqlExecute(insertSql, params, 'executemany')
    #
    #
    # sqlExecute("SELECT * FROM T_WEATHER", '', 'fetchall')
