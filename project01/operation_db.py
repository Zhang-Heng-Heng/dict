"""
提供服务端的所有数据库操作
"""
import pymysql
import hashlib
SALT="#&AID_"#盐
class Database:
    def __init__(self,host='localhost',
                 port=3306,
                 user='root',
                 passwd='123456',
                 charset='utf8',
                 database='dict'):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.charset=charset
        self.database=database
        self.connect_db()#连接数据库
    def connect_db(self):
        self.db=pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            charset=self.charset,
            database=self.database)
    def create_cursor(self):
        self.cur=self.db.cursor()
    def close(self):
        self.db.close()
    def register(self,name,passwd):
        sql="select * from 登录 where name='%s'"%name
        self.cur.execute(sql)
        r=self.cur.fetchone()#如果有结果则name存在
        if r:
            return False
        #密码加密处理
        hash = hashlib.md5((name+SALT).encode())  # 生成对象
        hash.update(passwd.encode())  # 算法加密
        passwd = hash.hexdigest()  # 提取加密后的密码
        sql="insert into 登录 (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
    def login(self,name,passwd):
        hash = hashlib.md5((name + SALT).encode())  # 生成对象
        hash.update(passwd.encode())  # 算法加密
        passwd = hash.hexdigest()  # 提取加密后的密码
        sql="select * from 登录 where name='%s' and passwd='%s'"%(name,passwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()  # 如果有结果则name存在
        if r:
            return True
        else:
            return False
    def query(self,word):
        sql="select mena from words where word='%s'"%word
        self.cur.execute(sql)
        r=self.cur.fetchone()
        if r:
            return r[0]

    def insert_history(self,name,word):
        sql="insert into 历史记录 (name,word) values (%s,%s)"%(name,word)
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
    def history(self,name):
        sql="select name,word,time from hist where name='%s' order by time desc limit 10"%name
        self.cur.execute(sql)
        return self.cur.fetchall()
