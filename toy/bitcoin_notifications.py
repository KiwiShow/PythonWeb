import requests
import time
from datetime import datetime

# Please limit requests to no more than 30 per minute.
# Endpoints update every 5 minutes.

# 获取比特币价格的api
# CoinMarketCap Public API Documentation Version 2
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v2/ticker/1/'
# 触发IFTTT的api
# https://maker.ifttt.com/trigger/{event}/with/key/bjvkZ1gI-LkEK8nSUdKMYB
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/bjvkZ1gI-LkEK8nSUdKMYB'


def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return response_json['data']['quotes']['USD']['price']
    

# value 即是 比特币价格，用 json 格式发送
def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)
    

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)
    

# 比特币价格 10000刀以下 触发 IFTTT 通知，注意，不是在 telegram 里面发通知
BITCOIN_PRICE_THRESHOLD = 5000

def main():
    # 获取到 一定数量的 比特币价格 之后 用 dict 保存 在 list 中
    # 统一发送之后 再 清空列表
    bitcoin_history = []
    # while True:
    price = get_latest_bitcoin_price()
    date = datetime.now()
    bitcoin_history.append({'date': date, 'price': price})

    # 两种事件
    # bitcoin_price_emergency（IFTTT 发通知）
    # bitcoin_price_update （telegram 发信息）

    # Send an emergency notification
    if price < BITCOIN_PRICE_THRESHOLD:
        post_ifttt_webhook('bitcoin_price_emergency', price)

    # Send a Telegram notification
    if len(bitcoin_history) == 1:
        post_ifttt_webhook('bitcoin_price_update',
                           format_bitcoin_history(bitcoin_history))
        print(format_bitcoin_history(bitcoin_history))
        # bitcoin_history = []

        # 每4小时 获取一个 比特价格，一天获得6个值，然后统一发送给 telegram
        # 但是这样的话服务器 supervisorctl reload 又清空了。
        # 所以使用 schedule 定时
        # time.sleep(6)
    

if __name__ == "__main__":
    import schedule
    # 每天 12:30 发送一个
    schedule.every().day.at("12:30").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)


# 服务器 的 时区 不一样. 修改服务器的时区
# 时区的配置文件是/etc/sysconfig/clock。用tzselect命令就可以修改, 但是需要重启 服务器

# 出现的问题，没有/etc/sysconfig/clock

# tzselect 结束之后出现
# You can make this change permanent for yourself by appending the line
#         TZ='Asia/Shanghai'; export TZ
# to the file '.profile' in your home directory; then log out and log in again.
#
# Here is that TZ value again, this time on standard output so that you
# can use the /usr/bin/tzselect command in shell scripts:
# Asia/Shanghai

# .profile 没有 去找 .bashrc 修改完成之后 schedule的时间用的还是纽约时间，相差12小时。
#
# 所以设置环境变量是不行的
# 还得设置  系统时间
#
# lrwxrwxrwx   1 root root     33 May 19 19:47 localtime -> /usr/share/zoneinfo/Asia/Shanghai
# -rw-r--r--   1 root root     14 May 19 20:14 timezone

# 另外还得同步一下 硬件时间

