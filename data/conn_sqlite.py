# -=-=-=-=-=-=-=-=-=-=-=
# coding=UTF-8
# __author__='Guo Jun'
# Version 1.0.0
# -=-=-=-=-=-=-=-=-=-=-=
#import pymysql
import sqlite3

class SqliteDB():    
    def __init__(self, dbname):
        self.db_name = dbname
        self.conn = sqlite3.connect(self.db_name + '.db')
        self.cur = self.conn.cursor()
        
    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
    
    def commit(self):
        self.conn.commit()        
        
    def formatter(self,db_data):
        if len(db_data) == 0:
                return None
        else:           
            data_list = []            
            for i in db_data:
                if len(i) > 1:
                    data = []
                    for j in i:
                        data.append(j)
                    data_list.append(data)
                else:
                    data_list.append(i[0])
            return data_list
        
    def select(self,sql):
        try:
            self.cur.execute(sql)
            db_data = self.cur.fetchall()
            return self.formatter(db_data)
        except Exception as error:
            print(error)
            print(sql)
        
    def list_to_tuple(self,data):
        data_list = []
        if isinstance(data[0], list):
            for item in data:
                data_list.append(tuple(item))
            return tuple(data_list)
        elif isinstance(data, list):
            return tuple(data)
    
    def insert(self,table,data):
        data = self.list_to_tuple(data)
        for item in data:            
            insert_sql = 'INSERT INTO ' + table + ' VALUES {v}'.format(v=item)
            try:            
                self.cur.execute(insert_sql)                 
            except Exception as error:
                print(error)
                print(insert_sql)
        self.conn.commit() 
        
    def execute(self,sql):       
        try:            
            self.cur.execute(sql)
        except Exception as error:
            print(sql)
            print(error)
        self.conn.commit()

#def connDB():  # 连接数据库函数
#    conn = pymysql.connect(host='localhost', user='root', passwd='66196619', db='data', charset='utf8')
#    cur = conn.cursor();
#    return (conn, cur);
#
#
#def exeUpdate(cur, sql):  # 更新语句，可执行update,insert语句
#    sta = cur.execute(sql);
#    return (sta);
#
#def fill_data(query_sql):
#    conn, cur = connDB()
#    try:
#        cur.execute(query_sql)
#    except Exception as e:
#        print(e)
#        print(query_sql)
#    conn.commit()
#    conn.close();
#
#def exeDelete(cur, IDs):  # 删除语句，可批量删除
#    for eachID in IDs.split(' '):
#        sta = cur.execute('delete from relationTriple where tID =%d' % int(eachID));
#    return (sta);
#
#
#def exeQuery(cur, sql):  # 查询语句
#    cur.execute(sql);
#    return (cur);
#
#
#def connClose(conn, cur):  # 关闭所有连接
#    cur.close();
#    conn.commit();
#    conn.close();
#
#
#def get_data(items, table, symbol, startDate, endDate):
#    conn, cur = connDB()
#    query_sql = 'select ' + items + ' from data.' + table + ' where symbol in ('+ str(symbol).replace('[','').replace(']','') + ') and date between \'' + startDate + '\' and \'' + endDate + '\' order by symbol, date'
#    # print(query_sql)
#    try:
#        cur.execute(query_sql)
#        db_data = cur.fetchall()
#    except Exception as e:
#        print(e)
#        print(query_sql)
#    conn.commit()
#    connClose(conn, cur)
#    return (db_data)
#
#
#def get_all_data(items, table, condition):
#    conn, cur = connDB()
#    query_sql = 'select ' + items + ' from ' + table + ' ' + condition
#
#    try:
#        cur.execute(query_sql)
#        db_data = cur.fetchall()
#    except Exception as e:
#        print(e)
#        db_data =[]
#
#    connClose(conn, cur)
#    return (db_data)