import pymysql


# 开发中一般会用 sqlite 数据库
# 部署到服务器上的时候才会使用 mysql 等数据库


def create(cur):
    sql_create = '''
    CREATE TABLE `users` (
        `id` INT(11) NOT NULL AUTO_INCREMENT,
        `email` VARCHAR(255) COLLATE utf8_bin NOT NULL,
        `password` VARCHAR(255) COLLATE utf8_bin NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
    AUTO_INCREMENT=1'''
    cur.execute(sql_create)
    print('create success')


def insert(cur, email, password):
    sql_insert = '''
    INSERT INTO
        `users`(`email`, `password`)
    VALUES
        (%s, %s);
    '''
    cur.execute(sql_insert, (email, password))
    print('insert success')


def select(cur):
    sql = '''
    SELECT 
        `id`, `password` 
    FROM 
        `users` 
    WHERE 
        `email`=%s
    '''
    cur.execute(sql, ('webmaster@python.org',))
    results = cur.fetchall()
    for r in results:
        print(r)


def delete(cur, user_id):
    sql_delete = '''
    DELETE FROM
        `users`
    WHERE 
        `id`=%s
    '''
    cur.execute(sql_delete, (user_id,))


def update(cur, user_id, email):
    sql_update = '''
    UPDATE
        `users`
    SET
        `email`=%s
    WHERE 
        `id`=%s
    '''
    cur.execute(sql_update, (email, user_id))


def main():
    connection = pymysql.connect(host="localhost",
                                 user="root",
                                 db="test_mysql",
                                 port=3306)
    try:
        with connection.cursor() as cur:
            # create(cur)
            insert(cur, 'webmaster@python.org', 'very-secret')
            # delete(cur, 2)
            select(cur)
            update(cur, 1, 'sdfsa@sdf')
            select(cur)
            connection.commit()
    finally:
        connection.close()


if __name__ == '__main__':
    main()
