# print(" a    b ".replace(' ', ''))

import pymysql

def insertOne(series,first_n,second_n,thrid_n,sum_n,open_time,cash,is_win):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "bhy980226275", "kyc_server")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    sql = "insert into lucky_num(series,first_n,second_n,thrid_n,sum_n,open_time,cash,is_win) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        # 执行sql语句
        cursor.execute(sql,(series,first_n,second_n,thrid_n,sum_n,open_time,cash,is_win))
        # 执行sql语句
        db.commit()
        print("数据保存成功")
    except Exception as e:
        # 发生错误时回滚
        db.rollback()
        print(e)

    # 关闭数据库连接
    db.close()

def get_all(id):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "bhy980226275", "kyc_server")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from lucky_num where id > "+str(id)+" ORDER BY id"
    # sql = "SELECT * from lucky_num where id >((select max(id) from lucky_num)-60) ORDER BY id desc;"
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        return results
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接

# 获取最新的100条记录
def get_rec(limit):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "bhy980226275", "kyc_server")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from lucky_num ORDER BY id desc limit " + str(limit)
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        return results
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接

def get_cash():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "bhy980226275", "kyc_server")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select cash from lucky_num ORDER BY id desc limit 1"
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        return results
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接

def get_if_win():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "bhy980226275", "kyc_server")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select is_win from lucky_num ORDER BY id desc limit 1"
    try:
        cursor.execute(sql)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        return results
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接

def update_fore(fore,id):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "bhy980226275", "kyc_server")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "update lucky_num set forecast=" + str(fore) + " where id=" + str(id)
    try:
        cursor.execute(sql)  # 执行sql语句
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()  # 关闭连接

