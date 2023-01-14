# -*- coding:utf-8 -*-
from LoginPanel import LoginPanel
from MainPanel import MainPanel
from RegisterPanel import RegisterPanel
from Client import ChatClient
import MD5
from tkinter import messagebox
from threading import Thread
import time
from databaseTool import MySQLTool


db=MySQLTool()

def send_message():
    print("send message:")
    #获取输入框输入的内容
    content = main_frame.get_send_text()
    if content == "" or content == "\n":
        print("空消息，拒绝发送")
        return
    print(content)
    # 清空输入框
    main_frame.clear_send_text()
    gid = int(main_frame.group_select[0:1])
    time_msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db.send_message(content,main_frame.username,gid,time_msg)
    time.sleep(0.5)
    main_frame.sync_msg()


# def create_group(groupname):
#     print("create group:",groupname)
#     #获取输入框输入的内容
#      # 清空输入框
#     client.create_group(groupname)

# def join_group(groupid):
#     print("join group:")
#     #获取输入框输入的内容
#     #groupid = '1'#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#      # 清空输入框
#     client.join_group(user,groupid)

def exit_group():
    print("exit group:")
    #获取输入框输入的内容
    groupid = '1'#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
     # 清空输入框
    client.exit_group(user,groupid)
    
def join_action():
    join_group_ID = main_frame.get_join_group()
    print("JOIN:",join_group_ID)
    _group_ID = db.get_groupid()
    group_ID = [str(x['gid']) for x in _group_ID]
    if join_group_ID not in group_ID:
        messagebox.showerror("错误","该ID不存在!")
    else:
        client.join_group(main_frame.username,join_group_ID)
        main_frame.join_window.destroy()
    main_frame.sync_group_list()
    
def create_action():
    create_group_name = main_frame.get_create_group()
    if create_group_name == None:
        messagebox.showerror("错误","Group Name 不能为空!")
    else:
        client.create_group(create_group_name)
        time.sleep(0.5)
        group = db.get_groupid()
        group_ID = [str(x['gid']) for x in group]
        print(group_ID)
        client.join_group(main_frame.username,str(group_ID[-1]))
        print("*****************")
        time.sleep(1)
        main_frame.create_window.destroy()
    main_frame.sync_group_list()

def delete_action():
    delete_group_ID = main_frame.get_delete_group()
    _group_ID = db.get_all_groupinfo(main_frame.username)
    group_ID = [str(x['gid']) for x in _group_ID]
    # for g in _group_ID:
    #     group_ID.append(g['gid'])        
    print(group_ID)
    if delete_group_ID not in group_ID:
        messagebox.showerror("错误","该ID不存在!")
    else:
        client.exit_group(main_frame.username,delete_group_ID)
        main_frame.delete_window.destroy()
    main_frame.sync_group_list()



# def get_group_message():
#     print("get_group_message:")
#     gid = current_groupid#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     return db.get_group_message(gid)

# def get_group_member():
#     print("get_group_member:")
#     gid = current_groupid#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     return db.get_group_member(gid)

# 其实后面几个都是默认参数的，你可以只填前面几个参数（uid，密码，名字
# 他是在哪里加密的？输入的时候嘛 所以你这里是不是也得加密一下？
def alter_account():
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 從輸入框讀取信息
    uid="12"
    name="name"
    nickname="nickname"
    gender="gender"
    hobby="hobby"
    password= MD5.gen_md5("123")
    print(uid, name, nickname, gender, hobby, password)
    client.alter_account(uid, name, nickname, gender, hobby, password)

def get_all_history():
    uid="12"
    print(uid)
    res = client.get_all_history(uid)
    print(res)

def close_sk():
    print("尝试断开socket连接")
    client.sk.close()


def close_main_window():
    close_sk()
    main_frame.main_frame.destroy()


def close_login_window():
    close_sk()
    login_frame.login_frame.destroy()


# 关闭注册界面并打开登陆界面
def close_reg_window():
    reg_frame.close()
    #登录界面
    global login_frame
    login_frame = LoginPanel(login, register, close_login_window)
    login_frame.show()


# 关闭登陆界面前往主界面
def goto_main_frame(user):
    login_frame.close()
    global main_frame
    # 从MainPanel.py模块中调用
    main_frame = MainPanel(user, send_message, close_main_window, client,join_action,create_action,delete_action)
    # 新开一个线程专门负责接收并处理数据
    Thread(target=recv_data).start()
    main_frame.show()

# 登陆时需要进行的验证
def login():
    global user
    user, key = login_frame.get_input()
    print(user,key)
    #join_group()
    #print(get_all_groupinfo())
    #time.sleep(5)
    # print(get_group_message())
    # print(get_group_member())
    # exit_group()
    # 密码传md5,加密
    key = MD5.gen_md5(key)
    if user == "" or key == "":
        messagebox.showwarning(title="提示", message="用户名或者密码为空")
        return
    print("user: " + user + ", key: " + key)
    #验证密码是否正确
    if client.check_user(user, key):
        # 验证成功
        goto_main_frame(user)
    else:
        # 验证失败
        messagebox.showerror(title="错误", message="用户名或者密码错误")


# 登陆界面->注册界面
def register():
    login_frame.close()
    global reg_frame
    reg_frame = RegisterPanel(close_reg_window, register_submit, close_reg_window)
    reg_frame.show()


# 提交注册表单
def register_submit():
    user, key, confirm = reg_frame.get_input()
    if user == "" or key == "" or confirm == "":
        messagebox.showwarning("错误", "请完成注册表单")
        return
    if not key == confirm:
        messagebox.showwarning("错误", "两次密码输入不一致")
        return
    # 发送注册请求
    result = client.register_user(user, MD5.gen_md5(key))
    if result == "0":
        # 注册成功，跳往登陆界面
        messagebox.showinfo("成功", "注册成功")
        close_reg_window()
    elif result == "1":
        # 用户名重复
        messagebox.showerror("错误", "该用户名已被注册")
    elif result == "2":
        # 未知错误
        messagebox.showerror("错误", "发生未知错误")


# 处理消息接收的线程方法
def recv_data():
    # 暂停几秒，等主界面渲染完毕
    time.sleep(1)
    while True:
        try:
            # 首先获取数据类型
            _type = client.recv_all_string()
            print("recv type: " + _type)
            if _type == "#!onlinelist#!":
                print("获取在线列表数据")
                online_list = list()
                for _ in range(client.recv_number()):
                    #添加各个用户名
                    online_list.append(client.recv_all_string())
                    #显示在发送消息界面中
                main_frame.refresh_friends()
                #输出登录的用户名
                print(online_list)
            elif _type == "#!message#!":
                print("获取新消息")
                user = client.recv_all_string()
                print("user: " + user)
                content = client.recv_all_string()
                print("message: " + content)
                main_frame.recv_message(user, content)
        except Exception as e:
            print("接受服务器消息出错，消息接受子线程结束。" + str(e))
            break


def start():
    global client
    client = ChatClient()
    global login_frame
    login_frame = LoginPanel(login, register, close_login_window)
    #print("################test create group")
    #create_group()
    login_frame.show()
    



if __name__ == "__main__":
    start()