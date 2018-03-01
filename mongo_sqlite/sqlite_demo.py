# 数据库通过 SQL 来操作数据
# SQL （ Structure Query Language 结构化查询语言）
# 操作数据库的接口 也就是操作数据库的方法
# 增加数据
# 删除数据
# 修改数据
# 查询数据
# CRUD
# create retrieve update delete

# 几种关系型数据库的用法和 sql 语法都极度相似
# 开发中一般会用 sqlite 数据库
# 部署到服务器上的时候才会使用 mysql 等数据库


import sqlite3


def create(conn):
    sql_create = '''
    CREATE TABLE `users`(
        `id`        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `username`  TEXT NOT NULL UNIQUE,
        `password`  TEXT NOT NULL,
        `email`     TEXT
        )'''
    conn.execute(sql_create)
    print('create success')


def insert(conn, username, password, email):
    sql_insert = '''
    INSERT INTO
        `users`(`username`,`password`,`email`)
    VALUES
        (?, ?, ?);
    '''
    # ? 是Python的库sqlite3的语法
    # 参数拼接要用 ?，execute 中的参数传递必须是一个 tuple 类型
    conn.execute(sql_insert, (username, password, email))
    print('insert success')


# def select(conn):  # bad examle
#     username = 'sql4'
#     # 演示SQL注入，所以不用拼接字符串的方法
#     #  甚至可能再增加恶心语句; DROP TABLE users
#     password = '" or "1"="1'
#     sql = '''
#     SELECT
#         *
#     FROM
#         users
#     WHERE
#         username="{}" and password="{}"
#     '''.format(username, password)
#     # cursor是可迭代的对象
#     # data = list(cursor)
#     # print(data)
#     cursor = conn.execute(sql)
#     for row in cursor:
#         print('查询结果: ', row)


def select(conn):
    username = 'sql4'
    # password = '" or "1"="1'
    password = '1234'
    sql = '''
    SELECT
        *
    FROM
        users
    WHERE
        username=? and password=?
    '''
    # ?会将 '"等转义
    # 用了框架不会有被注入的危险，但是有的PHP框架会有这个漏洞
    cursor = conn.execute(sql, (username, password))
    # cursor是可迭代的对象
    # data = list(cursor)
    # print(data)
    for row in cursor:
        print(row)


def delete(conn, user_id):
    sql_delete = '''
    DELETE FROM
        users
    WHERE 
        id=?
    '''
    conn.execute(sql_delete, (user_id,))


def update(conn, user_id, email):
    sql_update = '''
    UPDATE
        `users`
    SET
        `email`=?
    WHERE 
        `id`=?
    '''
    conn.execute(sql_update, (email, user_id))
    print('user_id:{} email:{} updated '.format(user_id, email))


def main():
    db_path = 'demo.sqlite'
    conn = sqlite3.connect(db_path)
    # print('打开了数据库')
    # create(conn)
    # insert(conn, 'sqlsdf', '1234', 'a@b.c')RRRRRRRRR
    # delete(conn, 2)
    # select 函数查询数据
    select(conn)
    update(conn, 1, 'sdfsa@sdf')
    select(conn)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
