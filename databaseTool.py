#databaseTool

#import pymysql
import  psycopg2

class MySQLTool():
    # 打开数据库连接
    def __init__(self):

        self.conn = psycopg2.connect(
            database="new", 
            user="gaussdb", 
            password="Okabe@163", 
            host="127.0.0.1", 
            port="15432")
#        self.conn = pymysql.connect(
#            host = "127.0.0.1",
#            port = 3306,
#            user = "root",
#            passwd = "####", # 修改为自己的数据库密码
#            db = "chat", # 连接chat数据库
#            charset = "utf8")


    def send_message(self,message, user, gid,time):
        cursor = self.conn.cursor()
        try:
            # SQL="INSERT INTO messages(mid, time, content) VALUES ('%s', '%s', '%s')" % (mid_input, time_input, content_input)
            SQL="insert into Message(contents,_timestamp) values('%s','%s')" % (message, time)
            print(SQL)
            cursor.execute(SQL)

            self.conn.commit()

            SQL="SELECT MAX(mid) FROM Message"
            cursor.execute(SQL)
            mid = cursor.fetchall()  # 返回所有消息记录

            self.conn.commit()
            print(mid)
            
            SQL="insert into _user_message(uid,mid) values('%s','%s')" % (user, mid[0][0])
            print(SQL)
            cursor.execute(SQL)

            self.conn.commit()


            SQL="insert into message_chatgroup(mid,gid) values('%s','%s')" % (mid[0][0],gid)
            print(SQL)
            cursor.execute(SQL)

            self.conn.commit()
            cursor.close()
            return True
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False
        


    def register_account(self, uid, password):
        '''注册账号
        :param uid: 待注册账号
        :param password: 待注册密码
        :return 0: '用户名存在'
        :return 1: '其他错误'
        :return 2: '添加用户成功'
        '''
        cursor = self.conn.cursor() # 获取游标
        try:
            print(uid,password)
            SQL="INSERT INTO _user(name,uid, passwd) VALUES (' ','%s', '%s')" % (uid, password)
            
            cursor.execute(SQL) # 执行SQL语句
            print("ex")
            cursor.close()  # 关闭游标
            print("QAQ")
            self.conn.commit() # 提交事务
            return "0"
        except psycopg2.Error as e:
            if e.args[0]==1062:
                print('账户已存在,不允许重复注册')
                return "1"
            else:
                return "2"

    def login_verify(self, uid_input, password_input):
        '''登录验证
        :param uid_input: 用户输入的账号
        :param password_input: 用户输入的密码
        :return True: 登录成功
        :return False: 登录失败(账号密码输入有误或数据库出错)
        '''
        cursor = self.conn.cursor()
        try:
            SQL="SELECT * FROM _user WHERE uid = '%s' AND passwd = '%s'" % (uid_input, password_input)
            print(SQL)
            cursor.execute(SQL)
            print("Dasd1")
            res = cursor.fetchone()  # 查询单条记录（由于用户ID唯一，所以没必要遍历整张表）
            cursor.close()
            self.conn.commit()
            print(res)
            if res==None:
                print('你输入的账号或密码有误')
                return False
            return True
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False
            
            
    def msg2database(self, mid_input, time_input, content_input):
        '''将消息存入数据库
        :param mid_input: 消息所属用户
        :param time_input: 消息发出时间
        :param content_input: 消息具体内容
        :return True: 成功存入数据库
        :return False: 数据库出错
        '''
        # 注：若需要对数据库自增主键id的起始值进行修改，可执行SQL语句 ALTER TABLE messages AUTO_INCREMENT= 1
        cursor = self.conn.cursor()
        try:
            # SQL="INSERT INTO messages(mid, time, content) VALUES ('%s', '%s', '%s')" % (mid_input, time_input, content_input)
            SQL="insert into Message(contents,_timestamp,from_uid) values('%s','%s','%s')" % (content_input, time_input, mid_input)
            print(SQL)
            cursor.execute(SQL)
            cursor.close()
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False
            
    def create_group(self, time_input, groupname_input):
        cursor = self.conn.cursor()
        try:
            # insert into chatgroup values(default,'abab','2003-04-12 04:05:06');
            print(time_input, groupname_input)
            SQL="INSERT INTO chatgroup(_timestamp,chatgroupname) VALUES ('%s', '%s')" % (time_input, groupname_input)
            print(SQL)
            cursor.execute(SQL)
            cursor.close()
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False
    def join_group( self,uid_input, gid_input):
        cursor = self.conn.cursor()
        try:
            # insert into chatgroup values(default,'abab','2003-04-12 04:05:06');
            print(uid_input, gid_input)
            all_info=self.get_all_groupinfo(uid_input)

            # print("gid:  ", gid_input ,"all gid:",all_info)
            flag1=0#查詢是否加入过这个组，没有加入过才可以插入
            # print('=====================')
            # print(type(gid_input))
            for tmp in all_info:
                # print(type(tmp['uid']))
                if (gid_input==str(tmp['gid'])):
                    flag1=1
                    break
            all_gid=self.get_groupid()
            flag2=0#查询是否存在这个组
            for tmp in all_gid:
                if (gid_input==str(tmp['gid'])):
                    flag2=1
                    break
            print("flag1 :",flag1,' flag2: ',flag2)
            if (flag1==0 and flag2==1):
                SQL="insert into  _user_chatgroup(uid,gid) values('%s','%s')" % (uid_input, gid_input)
                print(SQL)
                cursor.execute(SQL)
                cursor.close()
                self.conn.commit()
            else:
                return False#不存在这个组或者说以及加入过
            return True
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False

    def get_groupid(self):
        return_value= []
        message={
            'gid':'',
            'name':''
        }
        cursor = self.conn.cursor()
        try:
            # SQL="SELECT gid FROM _user_chatgroup where uid='%s'"%(uid) 
            SQL="SELECT gid, chatgroupname FROM chatgroup"
            cursor.execute(SQL)
            res = cursor.fetchall()  # 返回所有消息记录
            cursor.close()
            self.conn.commit()
            if res==():
                print('数据库中暂无记录')
                return []
            else:
                for i in res:
                    message=message.copy()
                    message['gid']=i[0]
                    message['name']=i[1]
                    return_value.append(message)
            return return_value
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False


    def exit_group_database( self,uid_input, gid_input):
        cursor = self.conn.cursor()
        try:
            # insert into chatgroup values(default,'abab','2003-04-12 04:05:06');
            print(uid_input, gid_input)
            all_info=self.get_all_groupinfo(uid_input)
            flag=0#查詢是否存在,存在才可以刪除
            # print('=====================')
            # print(type(gid_input))
            for tmp in all_info:
                # print(type(tmp['gid']))
                if (gid_input==str(tmp['gid'])):
                    flag=1
                    break
            # print('flag:   ',flag)
            # print('=====================')
            if (flag==1):
                SQL="delete from  _user_chatgroup where uid='%s'and gid='%s'" % (uid_input, gid_input)
                print(SQL)
                cursor.execute(SQL)
                cursor.close()
                self.conn.commit()
            else:
                return False#退出失败，没有加入过这个组
            return True
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False
    
    def get_all_groupinfo(self,uid):
        return_value= []
        message={
            'gid':'',
            'name':''
        }
        cursor = self.conn.cursor()
        try:
            # SQL="SELECT gid FROM _user_chatgroup where uid='%s'"%(uid) 
            SQL="SELECT chatgroup.gid,chatgroup.chatgroupname FROM _user_chatgroup ,chatgroup  where _user_chatgroup.uid='%s' and chatgroup.gid=_user_chatgroup.gid"%uid
            cursor.execute(SQL)
            res = cursor.fetchall()  # 返回所有消息记录
            cursor.close()
            self.conn.commit()
            if res==():
                print('数据库中暂无记录')
                return False
            else:
                for i in res:
                    message=message.copy()
                    message['gid']=i[0]
                    message['name']=i[1]
                    return_value.append(message)
            return return_value
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False

    def get_group_message(self,gid):
        '''获取当前群组的消息
        :return return_value: 从数据库中返回的值
        :return False: 数据库中无任何消息记录或数据库出错
        '''
        return_value= []
        message={
            'mid':'',
            'content':'',
            'time':'',
            'uid':''
        }
        cursor = self.conn.cursor()
        try:
            SQL="select DISTINCT Message.mid,Message.contents,Message._timestamp ,_user.uid from message_chatgroup,Message,_user,chatgroup,_user_message where Message.mid=_user_message.mid and _user_message.uid=_user.uid and message_chatgroup.mid=Message.mid and message_chatgroup.gid='%s'" %gid
            print(SQL)
            cursor.execute(SQL)
            res = cursor.fetchall()  # 返回所有消息记录
            cursor.close()
            self.conn.commit()
            if res==():
                print('数据库中暂无记录')
                return False
            else:
                for i in res:
                    message=message.copy()
                    message['mid']=i[0]
                    message['content']=i[1]
                    message['time']=i[2]
                    message['uid']=i[3]
                    return_value.append(message)
            return return_value
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False
     
    def get_group_member(self,gid):
        '''获取当前群组的成員
        :return return_value: 从数据库中返回的值
        :return False: 数据库中无任何消息记录或数据库出错
        '''
        return_value= []
        message={
            'uid':''
        }
        cursor = self.conn.cursor()
        try:
            SQL="select uid from _user_chatgroup where gid='%s'" %gid
            cursor.execute(SQL)
            res = cursor.fetchall()  # 返回所有消息记录
            cursor.close()
            self.conn.commit()
            if res==():
                print('数据库中暂无记录')
                return []
            else:
                for i in res:
                    message=message.copy()
                    message['uid']=i[0]
                    return_value.append(message)
            return return_value
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False


    def sync_messages(self):
        '''同步数据库中的消息
        :return return_value: 从数据库中返回的值
        :return False: 数据库中无任何消息记录或数据库出错
        '''
        return_value= []
        message={
            'mid':'',
            'time':'',
            'content':'',
        }
        cursor = self.conn.cursor()
        try:
            SQL="SELECT * FROM Message" 
            cursor.execute(SQL)
            res = cursor.fetchall()  # 返回所有消息记录
            cursor.close()
            self.conn.commit()
            if res==():
                print('数据库中暂无记录')
                return False
            else:
                for i in res:
                    message=message.copy()
                    message['mid']=str(i[3])
                    message['time']=str(i[2])
                    message['content']=i[1]
                    return_value.append(message)
            return return_value
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False
    
    def alter_account(self, uid, name, password, nickname = 'NULL', gender = 'NULL', hobby = 'NULL'):
        cursor = self.conn.cursor() # 获取游标
        try:
            print(uid, name, nickname, gender, hobby, password)
            SQL = "UPDATE _user SET name='%s',nickname='%s', passwd = '%s', gender = '%s', hobby = '%s' WHERE uid='%s'"%(name, nickname, password, gender, hobby, uid) 
            # 
            print(SQL)
            cursor.execute(SQL) # 执行SQL语句
            cursor.close()  # 关闭游标
            self.conn.commit() # 提交事务
            return True#修改成功
        except psycopg2.Error as e:
            return False#修改失败
    
    def get_all_history(self,uid):
        '''返回值：返回一个列表，对应着（文章名，时间）的元组'''
        return_value= []
        message={
            'name':'',
            'time':''
        }
        cursor = self.conn.cursor()
        try:
            SQL="SELECT article.name, history._timestamp FROM history, where uid='%s' AND history.uid = _user.uid "%(uid) 
            cursor.execute(SQL)
            res = cursor.fetchall()  # 返回所有消息记录
            cursor.close()
            self.conn.commit()
            if res==():
                print('数据库中暂无记录')
                return []
            else:
                for i in res:
                    message=message.copy()
                    message['name']=i[0]
                    message['time']=i[1]
                    return_value.append(message)
            return return_value
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False

    def post_article(self,uid,url,time):
        cursor = self.conn.cursor()
        try:
            # SQL="INSERT INTO messages(mid, time, content) VALUES ('%s', '%s', '%s')" % (mid_input, time_input, content_input)
            SQL="insert into articles(uid,content_url,_timestamp) values('%s','%s','%s')" % (uid,url,time)

            SQL="insert into _user_article(uid,aid) values('%s','%s')" % (uid,aid)
            print(SQL)
            cursor.execute(SQL)
            cursor.close()
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("op Error %d: %s" % (e.args[0], e.args[1]))
            return False
    
    # 关闭连接
    def conn_close(self):
        self.conn.close()