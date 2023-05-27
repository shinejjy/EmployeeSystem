import tkinter as tk
from Base.BaseFrame import BaseFrame


class EmployeeLoginFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        username_entry_text = tk.StringVar()
        password_entry_text = tk.StringVar()

        # 创建工号标签和输入框
        self.username_label = tk.Label(self, text="工号:", bg="white", font=("微软雅黑", 12))
        self.username_label.grid(row=0, column=0, pady=20, padx=10, sticky="e")
        self.username_entry = tk.Entry(self, font=("微软雅黑", 12), textvariable=username_entry_text)
        self.username_entry.grid(row=0, column=1, pady=20, padx=10)

        username_entry_text.set("XS001")

        # 创建密码标签和输入框
        self.password_label = tk.Label(self, text="密码:", bg="white", font=("微软雅黑", 12))
        self.password_label.grid(row=1, column=0, pady=20, padx=10, sticky="e")
        self.password_entry = tk.Entry(self, show="*", font=("微软雅黑", 12), textvariable=password_entry_text)
        self.password_entry.grid(row=1, column=1, pady=20, padx=10)

        password_entry_text.set("12345")

        # 创建登录按钮
        self.login_button = tk.Button(self, text="登录", command=self.login, font=("微软雅黑", 12))
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 创建结果标签
        self.result_label = tk.Label(self, text="", bg="white", font=("微软雅黑", 12))
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        # 获取输入的工号和密码
        username = self.username_entry.get()
        password = self.password_entry.get()

        # 构建SQL语句，用于查询密码是否匹配
        sql = f"""
        SELECT SPassWord
        FROM EmployeeInformation
        WHERE SID='{username}'
        """

        # 读取已注册用户信息
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()

        if result:
            if result[0] == password:
                # 登录成功，设置应用的用户名和模式，并显示成功页面
                self.app.username = username
                self.app.mode = "employee"
                self.app.show_main_frame()
            else:
                self.result_label.config(text="密码错误！", fg="red")
        else:
            self.result_label.config(text="工号不存在！", fg="red")
