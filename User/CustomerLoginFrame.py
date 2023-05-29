import tkinter as tk
from Base.Base import BaseFrame


class CustomerLoginFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        # 创建手机号、密码和姓名标签和输入框
        self.username_label = tk.Label(self, text="手机号:", bg="white", font=("微软雅黑", 12))
        self.username_label.grid(row=0, column=0, pady=20, padx=10, sticky="e")
        self.username_entry = tk.Entry(self, font=("微软雅黑", 12))
        self.username_entry.grid(row=0, column=1, pady=20, padx=10)

        self.password_label = tk.Label(self, text="密码:", bg="white", font=("微软雅黑", 12))
        self.password_label.grid(row=1, column=0, pady=20, padx=10, sticky="e")
        self.password_entry = tk.Entry(self, show="*", font=("微软雅黑", 12))
        self.password_entry.grid(row=1, column=1, pady=20, padx=10)

        self.name_label = tk.Label(self, text="姓名:", bg="white", font=("微软雅黑", 12))
        self.name_label.grid(row=2, column=0, pady=20, padx=10, sticky="e")
        self.name_entry = tk.Entry(self, font=("微软雅黑", 12))
        self.name_entry.grid(row=2, column=1, pady=20, padx=10)

        # 初始密码不可见状态
        self.password_visibility = False

        # 创建切换密码可见性的按钮
        self.password_visibility_button = tk.Button(self, text="显示密码", command=self.toggle_password_visibility,
                                                    font=("微软雅黑", 12))
        self.password_visibility_button.grid(row=2, column=3, columnspan=1, pady=10)

        # 创建注册按钮
        self.register_button = tk.Button(self, text="注册", command=self.register, font=("微软雅黑", 12))
        self.register_button.grid(row=3, column=1, pady=20, padx=10)

        # 创建登录按钮
        self.login_button = tk.Button(self, text="登录", command=self.login, font=("微软雅黑", 12))
        self.login_button.grid(row=3, column=2, pady=20, padx=10)

        # 创建结果标签
        self.result_label = tk.Label(self, text="", bg="white", font=("微软雅黑", 12))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def toggle_password_visibility(self):
        # 切换密码可见性状态
        self.password_visibility = not self.password_visibility

        if self.password_visibility:
            self.password_entry.config(show="")
            self.password_visibility_button.config(text="隐藏密码")
        else:
            self.password_entry.config(show="*")
            self.password_visibility_button.config(text="显示密码")

    def register(self):
        # 获取输入的手机号、密码和姓名
        username = self.username_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()

        # 检查手机号是否已存在
        if self.check_phone_exist(username):
            self.result_label.config(text="该手机号已被注册！", fg="red")
            return

        # 插入注册信息到 CustomerInformation 表
        sql = f"INSERT INTO CustomerInformation (PN, PW, CN) VALUES ('{username}', '{password}', '{name}')"
        self.app.db.execute(sql)

        self.result_label.config(text="注册成功！", fg="green")

    def check_phone_exist(self, phone):
        # 检查手机号是否已存在于 CustomerInformation 表中
        sql = f"SELECT 1 FROM CustomerInformation WHERE PN = '{phone}'"
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()

        if result:
            return True
        else:
            return False

    def login(self):
        # 获取输入的手机号和密码
        username = self.username_entry.get()
        password = self.password_entry.get()

        # 检查手机号和密码是否匹配
        sql = f"SELECT 1 FROM CustomerInformation WHERE PN = '{username}' AND PW = '{password}'"
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()

        if result:
            # 登录成功，设置应用的用户名和模式，并显示成功页面
            self.app.username = username
            self.app.mode = "customer"
            self.app.show_main_frame()
        else:
            self.result_label.config(text="手机号或密码错误！", fg="red")
