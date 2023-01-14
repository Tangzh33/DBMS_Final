import tkinter
import customtkinter

import os
from PIL import Image

class LoginPanel:
    def __init__(self, login_func, reg_func, close_callback):
        super().__init__()
        print("初始化登录界面类")
        self.login_func = login_func #登录函数
        self.reg_func = reg_func #注册函数
        self.close_callback = close_callback #用于退出关闭socket
        
        self.login_frame = None
        self.user = None
        self.key = None        
        
    def show(self):        
        self.login_frame = customtkinter.CTk()
        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        self.login_frame.protocol("WM_DELETE_WINDOW",self.close_callback)
        self.login_frame.title("Login to SysChat")
        self.login_frame.geometry("360x270")
        # set grid layout 4x2
        self.login_frame.grid_rowconfigure((0,1,2,3),weight=1)
        self.login_frame.grid_columnconfigure((0,1),weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./image")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "wx_logo.png")), size=(35, 35))      
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "user_light.png")), size=(20, 20))          
        
        self.key_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "key_light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "key_dark.png")), size=(20, 20))
        
        self.wx_label = customtkinter.CTkLabel(self.login_frame, text="  SysChat", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.wx_label.grid(row=0, column=0,columnspan=2, padx=20, pady=(20,10))

        self.user = tkinter.StringVar()
        self.key = tkinter.StringVar()
        
        self.user_label = customtkinter.CTkLabel(self.login_frame, text=" Accout:",image = self.add_user_image,compound="left",font=customtkinter.CTkFont(size=15, weight="bold") )
        self.user_label.grid(row=1,column=0,padx=(20,5),pady=5,sticky="e")
        
        self.user_enter = customtkinter.CTkEntry(self.login_frame,textvariable=self.user, placeholder_text="Enter your account ID",width=150,border_width=2,corner_radius=10)
        self.user_enter.grid(row=1,column=1,padx=(5,20),pady=5,sticky="w")
        
        self.passw_label = customtkinter.CTkLabel(self.login_frame, text=" Password:",image = self.key_image,compound="left",font=customtkinter.CTkFont(size=15, weight="bold") )
        self.passw_label.grid(row=2,column=0,padx=(20,5),pady=5,sticky="e")
        
        self.passw_enter = customtkinter.CTkEntry(self.login_frame, show="*", textvariable=self.key, placeholder_text="Enter your password",width=150,border_width=2,corner_radius=10)
        self.passw_enter.grid(row=2,column=1,padx=(5,20),pady=5,sticky="w")
        
        self.bar = customtkinter.CTkFrame(self.login_frame,corner_radius=0,fg_color="transparent")
        self.bar.grid(row=3,column=0,columnspan=2,padx=20,pady=(5,20))
        
        self.regis_button = customtkinter.CTkButton(self.bar, text='Register', command=self.reg_func,
                                                    font=customtkinter.CTkFont(size=14,weight="bold"), corner_radius=10,width=70)
        self.regis_button.grid(row=3,column=0,padx=(20,10),pady=5,sticky="e")        
        self.login_button = customtkinter.CTkButton(self.bar, text='Login', command=self.login_func,
                                                    font=customtkinter.CTkFont(size=14, weight="bold"), corner_radius=10,width=70)
        self.login_button.grid(row=3, column=1,padx=(10,20),pady=5,sticky="w")
        self.login_frame.mainloop()

    def close(self):
        if self.login_frame == None:
            print("未成功显示界面")
        else:
            self.login_frame.destroy()
    def get_input(self):
        return self.user.get(), self.key.get()
        

# if __name__ == "__main__":
#     app = LoginPanel(None,None,None)
#     app.show()
#     print(app.get_input())




# app = customtkinter.CTk()  # create CTk window like you do with the Tk window
# app.geometry("400x240")

# def button_function():
#     print("button pressed")

# # Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# app.mainloop()