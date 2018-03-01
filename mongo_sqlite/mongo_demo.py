"""
注意，需要安装 pymongo 这个库
- 安装3部曲，如果使用遇到问题就重新安装一次
1. brew install mongodb
2. sudo mkdir -p /data/db  在 / 目录下
3. sudo mongod
- 进入MongoDB Shell
1. cd /usr/local/Cellar/mongodb/3.*.*/bin
2. mongo
"""

import pymongo
import random


client = pymongo.MongoClient('mongodb://localhost:27017')

print('access to mongodb OK!', client)

# 设置要使用的数据库
mongodb_name = 'web8test'
# 直接这样就使用数据库了，相当于一个字典
db = client[mongodb_name]
# 也可以这样用 db = client.web8


def insert():
    u = {
        'name': 'uo',
        'note': '奇异果',
        '随机值': random.randint(0, 3),
    }
    db.user.insert(u)
    # 相当于 db['user'].insert


def find():
    user_list = list(db.user.find())
    print('all users', user_list)


def find1():
    query = {
        '随机值': 1,
    }
    print('random 1', list(db.user.find(query)))

    query = {
        '随机值': {
            '$gt': 1
        },
    }
    print('random > 1', list(db.user.find(query)))

    query = {
        '$or': [
            {
                '随机值': 2,
            },
            {
                'name': 'kiwi',
            },
        ]
    }
    us = list(db.user.find(query))
    print('or query', us)
    # 此外还有 $lt $let $get $ne $ or 等条件


def find_cond():
    query = {}
    field = {
        'name': 1,
        '_id': 0,
    }
    print('部分查询，只查询以下字段', list(db.user.find(query, field)))


def update():
    query = {
        '随机值': 3,
    }
    form = {
        '$set': {
            'name': 'kiwikiwi',
        }
    }
    options = {
        'multi': True,
    }
    db.user.update(query, form, **options)


def remove():
    query = {
        '随机值': 3
    }
    db.user.remove(query)


def main():
    # insert()
    # find()
    # find1()
    # find_cond()
    update()
    # remove()


if __name__ == '__main__':
    main()
