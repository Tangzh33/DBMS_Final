import tkinter
import customtkinter

import os
from PIL import Image

class RegisterPanel:
    def __init__(self, quit_func, reg_func, close_callback):
        super().__init__()
        print("初始化注册界面类")
        self.reg_frame = None
        self.user = None
        self.key = None
        self.confirm = None
        self.quit_func = quit_func #返回函数
        self.reg_func = reg_func #注册函数
        self.close_callback = close_callback #退出函数

    def show(self):
        self.reg_frame = customtkinter.CTk()
        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        self.reg_frame.protocol("WM_DELETE_WINDOW",self.close_callback)
        self.reg_frame.title("Register for SysChat")
        self.reg_frame.geometry("360x270")
        
        # set grid layout 5x2
        self.reg_frame.grid_rowconfigure((0,1,2,3),weight=1)
        self.reg_frame.grid_columnconfigure((0,1),weight=1)
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./image")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "wx_logo.png")), size=(35, 35))      
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "user_light.png")), size=(20, 20))          
        
        self.key_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "key_light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "key_dark.png")), size=(20, 20))
        
        self.wx_label = customtkinter.CTkLabel(self.reg_frame, text="  SysChat", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.wx_label.grid(row=0, column=0,columnspan=2, padx=20, pady=(20,10))
        

        self.user = tkinter.StringVar()
        self.key = tkinter.StringVar()
        self.confirm = tkinter.StringVar()
        
        self.user_label = customtkinter.CTkLabel(self.reg_frame, text=" Accout:",image = self.add_user_image,compound="left",font=customtkinter.CTkFont(size=15, weight="bold") )
        self.user_label.grid(row=1,column=0,padx=(20,5),pady=5,sticky="e")
        
        self.user_enter = customtkinter.CTkEntry(self.reg_frame, textvariable=self.user,
                                                 placeholder_text="Enter your account ID",width=150,border_width=2,corner_radius=10)
        self.user_enter.grid(row=1,column=1,padx=(5,20),pady=5,sticky="w")
        
        self.passw_label = customtkinter.CTkLabel(self.reg_frame, text=" Password:",image = self.key_image,compound="left",font=customtkinter.CTkFont(size=15, weight="bold") )
        self.passw_label.grid(row=2,column=0,padx=(20,5),pady=5,sticky="e")
        
        self.passw_enter = customtkinter.CTkEntry(self.reg_frame,show="*", textvariable=self.key,
                                                  placeholder_text="Enter your password",width=150,border_width=2,corner_radius=10)
        self.passw_enter.grid(row=2,column=1,padx=(5,20),pady=5,sticky="w")

        self.passw_relabel = customtkinter.CTkLabel(self.reg_frame, text=" Confirm:",image = self.key_image,compound="left",font=customtkinter.CTkFont(size=15, weight="bold") )
        self.passw_relabel.grid(row=3,column=0,padx=(20,5),pady=5,sticky="e")

        self.passw_renter = customtkinter.CTkEntry(self.reg_frame,show="*", textvariable=self.confirm,
                                                   placeholder_text="Enter password again",width=150,border_width=2,corner_radius=10)
        self.passw_renter.grid(row=3,column=1,padx=(5,20),pady=5,sticky="w")
        
        self.bar = customtkinter.CTkFrame(self.reg_frame,corner_radius=0,fg_color="transparent")
        self.bar.grid(row=4,column=0,columnspan=2,padx=20,pady=(5,20))
        self.regis_button = customtkinter.CTkButton(self.bar, text='Back',command=self.quit_func, font=customtkinter.CTkFont(size=14,weight="bold"), corner_radius=10,width=70)
        self.regis_button.grid(row=4,column=0,padx=(20,5),pady=5,sticky="e")        
        self.login_button = customtkinter.CTkButton(self.bar, text='Register',command=self.reg_func, font=customtkinter.CTkFont(size=14,weight="bold"), corner_radius=10,width=70)
        self.login_button.grid(row=4, column=1,padx=(5,20),pady=5,sticky="w")
        self.reg_frame.mainloop()

        
    def close(self):
        if self.reg_frame == None:
            print("未显示界面")
        else:
            self.reg_frame.destroy()

    # 获取输入的用户名、密码、确认密码
    def get_input(self):
        return self.user.get(), self.key.get(), self.confirm.get()


# if __name__ == "__main__":
#     app = RegisterPanel(None,None,None)
#     app.show()

