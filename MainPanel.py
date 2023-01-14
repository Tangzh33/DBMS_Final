import tkinter
from tkinter import *
import time
import customtkinter
import os
from PIL import Image
from databaseTool import MySQLTool

db = MySQLTool()

class MainPanel():

    # 四个按钮, 使用全局变量, 方便创建和销毁
    b1, b2, b3, b4 = None, None, None, None
    # 将图片打开存入变量中
    p1,p2,p3,p4 = None, None, None, None
    
    # 用字典将标记与表情图片一一对应, 用于后面接收标记判断表情贴图
    dic = None
    ee = 0  # 判断表情面板开关的标志

    def __init__(self, username, send_func, close_callback, client, join_action, create_action, delete_action):
        super().__init__()
        print("初始化主界面")
        self.username = username
        self.send_func = send_func
        self.close_callback = close_callback
        self.main_frame = None
        self.client = client
        self.join_action = join_action
        self.create_action = create_action
        self.delete_action = delete_action

    def show(self):
        global ee,b1,b2,b3,b4
        self.main_frame = customtkinter.CTk()
        self.main_frame.protocol("WM_DELETE_WINDOW", self.close_callback)                
        self.main_frame.title("Sun Yat-sen Chatroom")
        self.main_frame.geometry("700x450")

        # set grid layout 1x2
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image 基本logo
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./image")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "wx_logo.png")), size=(30, 30))
        
        self.face_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path,"face_light.png")),
                                                 dark_image=Image.open(os.path.join(image_path,"face_dark.png")),size=(30,30))
        
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "user_light.png")), size=(20, 20))
        self.moments_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "moments_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "moments_light.png")), size=(20, 20))

        # create navigation frame 导肮
        self.navigation_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  SysChat", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=17, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home", font=customtkinter.CTkFont(size=15),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Chats", font=customtkinter.CTkFont(size=15),
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")
        
        self.frame_1_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Moments", font=customtkinter.CTkFont(size=15),
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.moments_image, anchor="w", command=self.frame_1_button_event)
        self.frame_1_button.grid(row=3, column=0, sticky="ew")
        
        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Me", font=customtkinter.CTkFont(size=15),
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0,columnspan=2, padx=20, pady=20)

        self.home_text = customtkinter.CTkTextbox(self.home_frame)
        self.home_text.grid(row=1,column=0,padx=(20,5), pady=5,sticky="nsew")
        self.home_text.insert("0.0", "Sun Yat-sen Chatroom.\nBuild with Python & Opengauss.\n")
        self.home_text.configure(state="disabled")
        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self.home_frame)
        self.radiobutton_frame.grid(row=1, column=1, padx=(5, 20), pady=5, sticky="nsew")
        self.radiobutton_frame.grid_columnconfigure(0, weight=1)
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Please rate our app:")
        self.label_radio_group.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame,text="full marks", variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame,text="full marks", variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame,text="full marks", variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        
        
        # create first fram
        self.first_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        

        
        # create second frame
        self.second_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0,weight=1)
        self.second_frame.grid_rowconfigure((0,2,3),weight=1)
        
        # group chat view in second frame 
        self.group_tabview = customtkinter.CTkTabview(self.second_frame,command=self.select_group_tab)
        self.group_tabview.grid(row=0, column=0,padx=20, pady=5, sticky="nsew")
        #-------------------------------------------------------
        
        self.group_list = db.get_all_groupinfo(self.username)
               
        for g in self.group_list:
            self.group_tabview.add(str(g['gid'])+":"+str(g['name']))

        # self.group_tabview.add("Global")
        # self.group_tabview.add("Group1")
        # self.group_tabview.add("Group2")
        #----------------------------
        self.global_chatroom = None
        self.global_list = None
        
        self.select_group_tab()
        
        self.group_entry = customtkinter.CTkTextbox(self.second_frame,width=120,height=100,border_width=2,corner_radius=10)
        self.group_entry.grid(row=2, column=0,padx=20, pady=5, sticky="nsew")
        
        self.enter_bar = customtkinter.CTkFrame(self.second_frame,corner_radius=0,fg_color="transparent")
        self.enter_bar.grid_columnconfigure((0,1,2,3,4,6,7),weight=1)
        self.enter_bar.grid_rowconfigure(0,weight=1)
        self.enter_bar.grid(row=3,column=0,padx=(0,20),pady=(5,10),sticky="nsew")
        
        # 表情相关
        global b1,b2,b3,b4,p1,p2,p3,p4,dic,ee
        ee = 0
        # 将图片打开存入变量中
        p1 = tkinter.PhotoImage(file='./emoji/facepalm.png')
        p2 = tkinter.PhotoImage(file='./emoji/smirk.png')
        p3 = tkinter.PhotoImage(file='./emoji/concerned.png')
        p4 = tkinter.PhotoImage(file='./emoji/smart.png')
        dic = {'aa**': p1, 'bb**': p2, 'cc**': p3, 'dd**': p4}
        # 发送表情图标记的函数, 在按钮点击事件中调用
        
        # 四个对应的函数
        def bb1():
            mark('aa**')


        def bb2():
            mark('bb**')


        def bb3():
            mark('cc**')


        def bb4():
            mark('dd**')

        def mark(mes):  # 参数是发的表情图标记, 发送后将按钮销毁
            global ee,b1
            #发送给服务器
            self.client.send_message(mes)
            b1.destroy()
            b2.destroy()
            b3.destroy()
            b4.destroy()
            ee = 0
            
        def express():
            global b1, b2, b3, b4, ee
            if ee == 0:
                ee = 1  # 表情面板开关的标志，=1表示已经打开了
                b1 = tkinter.Button(self.main_frame, command=bb1, image=p1, relief=tkinter.FLAT, bd=0)
                b2 = tkinter.Button(self.main_frame, command=bb2, image=p2, relief=tkinter.FLAT, bd=0)
                b3 = tkinter.Button(self.main_frame, command=bb3, image=p3, relief=tkinter.FLAT, bd=0)
                b4 = tkinter.Button(self.main_frame, command=bb4, image=p4, relief=tkinter.FLAT, bd=0)

                b1.place(x=400, y=720)
                b2.place(x=470, y=720)
                b3.place(x=540, y=720)
                b4.place(x=610, y=720)
            else:
                ee = 0
                b1.destroy()
                b2.destroy()
                b3.destroy()
                b4.destroy()
                # 创建表情按钮       
        
        self.face_button = customtkinter.CTkButton(self.enter_bar, command=express,
                                                   text="",width=3,fg_color="transparent",image=self.face_image)
        self.face_button.grid(row=0,column=0,padx=(0,5),pady=0,sticky="ns")
        self.clear_button = customtkinter.CTkButton(self.enter_bar,command=self.clear_send_text,
                                                    text="Clear",font=customtkinter.CTkFont(size=14), corner_radius=5,width=5)
        self.clear_button.grid(row=0,column=6,padx=5,pady=0,sticky="ew")       
        self.send_button = customtkinter.CTkButton(self.enter_bar,command=self.send_func,
                                                   text="Send",font=customtkinter.CTkFont(size=14, weight="bold"),corner_radius=5,width=5)
        self.send_button.grid(row=0,column=7,padx=5,pady=0,sticky="ew")
        
        # create third frame
        self.third_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure((0,1),weight=1)
        self.third_frame.grid_rowconfigure(0,weight=1)
        
        self.group_frame = customtkinter.CTkFrame(self.third_frame,corner_radius=10)
        self.group_frame.grid(row=0,column=0,padx=(20,5),pady=20,sticky="nsew")
        self.group_frame.grid_columnconfigure(0,weight=1)
        self.group_frame.grid_rowconfigure(1,weight=1)
        self.group_label = customtkinter.CTkLabel(self.group_frame, text="Your Groups", font=customtkinter.CTkFont(size=16),anchor="center")
        self.group_label.grid(row=0,column=0,padx=20,pady=10,sticky="nsew")
        
        #self.group_list = tkinter.Listbox(self.group_frame, bd=0, bg = "#e7e9eb")
        self.group_list = customtkinter.CTkTextbox(self.group_frame, state = "disabled")
        self.group_list.grid(row=1,column=0,padx=20, pady=(5,10),sticky="nsew")
        
        
        self.add_group_button = customtkinter.CTkButton(self.group_frame,command=self.join_group_button,
                                                        text="Join Group",corner_radius=5,width=100)
        self.add_group_button.grid(row=2,column=0,padx=20,pady=5,sticky="ns")
        
        self.create_group_button = customtkinter.CTkButton(self.group_frame,command=self.create_group_button,
                                                        text="Create Group",corner_radius=5,width=100)
        self.create_group_button.grid(row=3,column=0,padx=20,pady=5,sticky="ns")        
    
              
        self.del_group_button = customtkinter.CTkButton(self.group_frame,command=self.delete_group_button,
                                                        text="Exit Group",corner_radius=5, width=100)
        
        self.del_group_button.grid(row=4,column=0,padx=20,pady=(5,10),sticky="ns")   
        
        
        self.me_frame = customtkinter.CTkFrame(self.third_frame,corner_radius=10)
        self.me_frame.grid(row=0,column=1,padx=(5,20),pady=20,sticky="nsew")
        self.me_frame.grid_rowconfigure(0,weight=1)
        self.me_frame.grid_columnconfigure(0,weight=1)
        
        self.me_label = customtkinter.CTkLabel(self.me_frame, text="About Me", font=customtkinter.CTkFont(size=18,weight="bold"),anchor="center")
        self.me_label.grid(row=0,column=0,padx=20,pady=10,sticky="nsew")
        
        
        self.account_label = customtkinter.CTkLabel(self.me_frame, text="Account:  "+ "okabe" ,font=customtkinter.CTkFont(size=15),anchor="w")
        self.account_label.grid(row=1,column=0,padx=20,pady=(0,10),sticky="ew")   
        
        self.nickname_label = customtkinter.CTkLabel(self.me_frame, text="Nickname:  "+ "Okabe" ,font=customtkinter.CTkFont(size=15),anchor="w")
        self.nickname_label.grid(row=2,column=0,padx=20,pady=(0,10),sticky="ew") 
        
        self.gender_label = customtkinter.CTkLabel(self.me_frame, text="Gender:  "+ "Girl" ,font=customtkinter.CTkFont(size=15),anchor="w")
        self.gender_label.grid(row=3,column=0,padx=20,pady=(0,10),sticky="ew")

        self.hobby_label = customtkinter.CTkLabel(self.me_frame, text="Hobby:  "+ "Ball" ,font=customtkinter.CTkFont(size=15),anchor="w")
        self.hobby_label.grid(row=4,column=0,padx=20,pady=(0,10),sticky="ew")
        
        self.define_button = customtkinter.CTkButton(self.me_frame,text="Modify",command=self.define_me,corner_radius=5,height=30,width=100)
        self.define_button.grid(row=5,column=0,padx=20,pady=10,sticky="ns")        
        
        self.history_button = customtkinter.CTkButton(self.me_frame,text="Access History",corner_radius=5,height=30,width=100)
        self.history_button.grid(row=6,column=0,padx=20,pady=10,sticky="ns")

        # select default frame
        self.select_frame_by_name("home")
            
        self.main_frame.mainloop()
            
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_1_button.configure(fg_color=("gray75", "gray25") if name == "frame_1" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_1":
            self.first_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.first_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
            self.group_tabview.destroy()
            
            self.group_tabview = customtkinter.CTkTabview(self.second_frame,command=self.select_group_tab)
            self.group_tabview.grid(row=0, column=0,padx=20, pady=5, sticky="nsew")
                    
            group_list = db.get_all_groupinfo(self.username)
                
            for g in group_list:
                self.group_tabview.add(str(g['gid'])+":"+str(g['name']))

            # self.group_tabview.add("Global")
            # self.group_tabview.add("Group1")
            # self.group_tabview.add("Group2")
            #----------------------------
            self.select_group_tab()
            self.sync_msg()
            
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.sync_group_list()
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def select_group_tab(self):
        self.group_select = self.group_tabview.get()
        if self.group_select == '':
            return
        self.group_tabview.tab(self.group_select).grid_rowconfigure(0,weight=1)
        self.group_tabview.tab(self.group_select).grid_columnconfigure(0, weight=1)

        self.global_chatroom = customtkinter.CTkTextbox(self.group_tabview.tab(self.group_select),height=240,state="disabled")
        self.global_chatroom.grid(row=0,column=0,padx=0,pady=0,sticky="nsew")
        self.global_chatroom.tag_config("greencolor", foreground="green")
        self.global_chatroom.tag_config("bluecolor", foreground="#0060bf")

        # self.global_list = tkinter.Listbox(self.group_tabview.tab("Global"), bd=0, bg = "#e7e9eb")
        self.global_list = customtkinter.CTkTextbox(self.group_tabview.tab(self.group_select),width=70,state = "disabled",text_color=("black","white"))
        self.global_list.grid(row=0,column=1,padx=(5,0),pady=0,sticky="nsew")
        self.global_list.tag_config("greencolor", foreground="green")

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_1_button_event(self):
        self.select_frame_by_name("frame_1")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # 刷新在线列表
    def refresh_friends(self):
        names = db.get_group_member(int(self.group_select[0]))
        self.global_list.configure(state=NORMAL)
        self.global_list.delete(0.0,END)
        for name in names:
            self.global_list.insert(0.0, str(name['uid'] +"\n")) 
        self.global_list.configure(state=DISABLED)
        # self.friend_list.delete(0, END)
        # for name in names:
        #     self.friend_list.insert(0, name)

    # 接受到消息，在文本框中显示，自己的消息用绿色，别人的消息用蓝色
    def recv_message(self, user, content):
        try:
            self.global_chatroom.configure(state=NORMAL)
            global dic
            title = user + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
            if user == self.username:
                self.global_chatroom.insert(END, title, 'greencolor')
            else:
                self.global_chatroom.insert(END, title, 'bluecolor')
            # 判断是否为表情

            self.global_chatroom.insert(END, content + "\n")
            self.global_chatroom.configure(state=DISABLED)
        # 滚动到最底部
            self.global_chatroom.see(END)
        except Exception as e:
            print('接收方发送错误：'+str(e))



    # 清空消息输入框
    def clear_send_text(self):
        self.group_entry.delete('0.0',END)
        #self.send_text.delete('0.0', END)

    # 获取消息输入框内容
    def get_send_text(self):
        return self.group_entry.get('0.0',END)
        #return self.send_text.get('0.0', END)

    # 同步数据库中的消息记录
    def sync_msg(self):
        return
        self.global_chatroom.configure(state=NORMAL)
        # 清空面板内所有内容
        self.global_chatroom.delete(1.0, "end")
        # 同步数据库中的所有数据
        gid = int(self.group_select[0:1])
        global dic
        db_messages=db.get_group_message(gid)
        if db_messages==False:
            print("同步失败")
            # customtkinter.CTkTextbox.showerror("同步失败", "数据中无任何消息记录\n或在同步过程中出现错误")
        else:
            for message in db_messages:
                # 判断消息是否应该显示给当前用户
                title = str(message['uid']) + " " + str(message['time']) + "\n"
                if str(message['uid']) == str(self.username):
                    self.global_chatroom.insert(END, title, 'greencolor')
                else:
                    self.global_chatroom.insert(END, title, 'bluecolor')

                self.global_chatroom.insert(END, message['content'] + "\n")
        # 滚动到最底部
        self.global_chatroom.see(END)
        self.global_chatroom.configure(state=DISABLED)
        
    def sync_group_list(self):
        ll = db.get_all_groupinfo(self.username)
        self.group_list.configure(state=NORMAL)
        self.group_list.delete(0.0,END)
        for group in ll:
            self.group_list.insert(0.0, "ID:"+str(group['gid'])+"    Name:"+group['name']+"\n")   
        self.group_list.configure(state=DISABLED)        

        
    def join_group_button(self):
        self.join_window = customtkinter.CTkToplevel(self.main_frame)
        self.join_window.geometry("240x160")
        self.join_window.grid_rowconfigure((0,1),weight=1)
        self.join_window.grid_columnconfigure(0,weight=1) # font=customtkinter.CTkFont(size=15, weight="bold")
        self.join_group_id  = tkinter.StringVar()
        group_entry = customtkinter.CTkEntry(self.join_window, textvariable=self.join_group_id,
                                             placeholder_text="Enter the group ID", width=150,border_width=2,corner_radius=10)
        group_entry.grid(row=0,column=0,padx=(10,10),pady=(20,5),sticky="nsew")        
        join_button = customtkinter.CTkButton(self.join_window, text="Add", command=self.join_action,font=customtkinter.CTkFont(size=14,weight="bold"),corner_radius=10,width=70)        
        join_button.grid(row=1, column=0,padx=(10,10),pady=(5,20),sticky="nsew")
        
    def create_group_button(self):
        self.create_window = customtkinter.CTkToplevel(self.main_frame)
        self.create_window.geometry("240x160")
        self.create_window.grid_rowconfigure((0,1),weight=1)
        self.create_window.grid_columnconfigure(0,weight=1) # font=customtkinter.CTkFont(size=15, weight="bold")
        self.create_group_name  = tkinter.StringVar()
        group_entry = customtkinter.CTkEntry(self.create_window, textvariable=self.create_group_name,
                                             placeholder_text="Enter the group name", width=150,border_width=2,corner_radius=10)
        group_entry.grid(row=0,column=0,padx=(10,10),pady=(20,5),sticky="nsew")        

        create_button = customtkinter.CTkButton(self.create_window, text="Create", command=self.create_action, font=customtkinter.CTkFont(size=14,weight="bold"),corner_radius=10,width=70)
        create_button.grid(row=1, column=0,padx=(10,10),pady=(5,20),sticky="nsew")
        
    def delete_group_button(self):
        self.delete_window = customtkinter.CTkToplevel(self.main_frame)
        self.delete_window.geometry("240x160")
        self.delete_window.grid_rowconfigure((0,1),weight=1)
        self.delete_window.grid_columnconfigure(0,weight=1) # font=customtkinter.CTkFont(size=15, weight="bold")
        self.delete_group_ID  = tkinter.StringVar()
        group_entry = customtkinter.CTkEntry(self.delete_window, textvariable=self.delete_group_ID,
                                             placeholder_text="Enter the group ID", width=150,border_width=2,corner_radius=10)
        group_entry.grid(row=0,column=0,padx=(10,10),pady=(20,5),sticky="nsew")        

        delete_button = customtkinter.CTkButton(self.delete_window, text="Delete", command=self.delete_action, font=customtkinter.CTkFont(size=14,weight="bold"),corner_radius=10,width=70)
        delete_button.grid(row=1, column=0,padx=(10,10),pady=(5,20),sticky="nsew")
    
    def get_join_group(self):
        return self.join_group_id.get()
    
    def get_create_group(self):
        return self.create_group_name.get()
    
    def get_delete_group(self):
        return self.delete_group_ID.get()
        
    def define_me(self):
        self.define_window = customtkinter.CTkToplevel(self.main_frame)
        self.define_window.geometry("320x240")
        # self.delete_window.grid_rowconfigure((0,1),weight=1)
        self.define_window.grid_columnconfigure((0,1),weight=1) # font=customtkinter.CTkFont(size=15, weight="bold")
        self.nickname  = tkinter.StringVar()
        self.gender  = tkinter.StringVar()
        self.hobby  = tkinter.StringVar()
        self.nickname_label = customtkinter.CTkLabel(self.define_window, text=" Nickname:",font=customtkinter.CTkFont(size=15, weight="bold") )
        self.nickname_label.grid(row=1,column=0,padx=(20,5),pady=(20,5),sticky="e")
        self.nickname_enter = customtkinter.CTkEntry(self.define_window,textvariable=self.nickname, placeholder_text="Enter your NickName",width=150,border_width=2,corner_radius=10)
        self.nickname_enter.grid(row=1,column=1,padx=(5,20),pady=5,sticky="w")

        self.gender_label = customtkinter.CTkLabel(self.define_window, text=" Gender:",font=customtkinter.CTkFont(size=15, weight="bold") )
        self.gender_label.grid(row=2,column=0,padx=(20,5),pady=5,sticky="e")
        self.gender_enter = customtkinter.CTkEntry(self.define_window,textvariable=self.gender, placeholder_text="Enter your Gender",width=150,border_width=2,corner_radius=10)
        self.gender_enter.grid(row=2,column=1,padx=(5,20),pady=5,sticky="w")
        
        self.hobby_label = customtkinter.CTkLabel(self.define_window, text=" Hobby:",font=customtkinter.CTkFont(size=15, weight="bold") )
        self.hobby_label.grid(row=3,column=0,padx=(20,5),pady=5,sticky="e")
        self.hobby_enter = customtkinter.CTkEntry(self.define_window,textvariable=self.hobby, placeholder_text="Enter your Hobby",width=150,border_width=2,corner_radius=10)
        self.hobby_enter.grid(row=3,column=1,padx=(5,20),pady=5,sticky="w")

        Modify_button = customtkinter.CTkButton(self.define_window, text="Modify", command=self.sync_per, font=customtkinter.CTkFont(size=14,weight="bold"),corner_radius=10,width=70)
        Modify_button.grid(row=4, column=0,columnspan=2,padx=(10,10),pady=(5,20),sticky="nsew")
    
    def sync_per(self):
        self.account_label.configure(text="Account:  "+ "okabe")
  
        self.nickname_label.configure(text="Nickname:  "+ self.nickname.get())
        
        self.gender_label.configure(text="Gender:  "+ self.gender.get())

        self.hobby_label.configure(text="Hobby:  "+ self.hobby.get())
        
        self.define_window.destroy()
        
    
        
            


# if __name__ == "__main__":
#     app = MainPanel(None,None,None,None)
#     app.show()


