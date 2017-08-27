#!/usr/bin/python3


import pymysql.cursors
import sys


class Mydb:
    host = ''
    username = ''
    password = ''
    port = 0
    db = ''
    coon = None

    def __init__(self, host, username, port, password, db):
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.db = db
        self._connectdb()

    def _connectdb(self):
        try:
            self.coon = pymysql.connect(host=self.host,
                                        user=self.username,
                                        port=self.port,
                                        password=self.password,
                                        db=self.db,
                                        charset='utf8'
                                        )
        except Exception as e:
            print(e)
            sys.exit()

    def select(self, sql, args=None):
        datas = None
        cursor = None
        try:
            self._connectdb()
            cursor = self.coon.cursor()
            cursor.execute(sql, args)
            datas = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            return datas

    def insertinto(self, sql, args=None):
        cursor = None
        rowcount = 0
        datas = None
        try:
            cursor = self.coon.cursor()
            cursor.executemany(sql, args)
            self.coon.commit()
            rowcount = cursor.rowcount
            # datas = cursor.fetchall()
            # if datas:
            #     print(datas)
        except Exception as e:
            print(e)
            self.coon.rollback()
        finally:
            if cursor:
                cursor.close()
            return rowcount

    def delete_db(self, sql, args=None):
        cursor = None
        rowcount = 0

        try:
            cursor = self.coon.cursor()
            cursor.execute(sql, args)
            self.coon.commit()
            cursor.fetchall()
            rowcount = cursor.rowcount
        except Exception as e:
            print(e)
            self.coon.rollback()
        finally:
            if cursor:
                cursor.close()
            return rowcount

    def update_db(self, sql, args=None):
        cursor = None
        rowcount = 0

        try:
            cursor = self.coon.cursor()
            cursor.execute(sql, args)
            self.coon.commit()
            rowcount = cursor.rowcount
        except Exception as e:
            print(e)
            self.coon.rollback()
        finally:
            if cursor:
                cursor.close()
            return rowcount

    def __del__(self):
        if self.coon is not None:
            self.coon.close()

    def gettables(self, sql):
        cursor = None
        tables = None
        try:
            cursor = self.coon.cursor()
            cursor.execute(sql)
            tables = cursor.fetchall()
            print(tables)
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            return tables
if __name__ == '__main__':
    mysql = Mydb('10.10.7.107', 'g_user', 2433, 'qqdba_changic', 'db_game_rh_0002')
    sql = "UPDATE t_u_player SET LEVEL = 13 WHERE  nickname in ('生命的麦凯伦', '墙的罗素')"
    rowcount = mysql.update_db(sql)
    print(rowcount)
