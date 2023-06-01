import tkinter as tk
from tkinter import messagebox

from Base.Base import BaseFrame


class CustomerLoginFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        # 创建手机号、密码标签和输入框
        self.id_label = tk.Label(self, text="账号或手机号:", bg="white", font=("微软雅黑", 12))
        self.id_label.grid(row=0, column=0, pady=20, padx=10, sticky="e")
        self.id_entry = tk.Entry(self, font=("微软雅黑", 12))
        self.id_entry.grid(row=0, column=1, pady=20, padx=10)

        self.password_label = tk.Label(self, text="密码:", bg="white", font=("微软雅黑", 12))
        self.password_label.grid(row=1, column=0, pady=20, padx=10, sticky="e")
        self.password_entry = tk.Entry(self, show="*", font=("微软雅黑", 12))
        self.password_entry.grid(row=1, column=1, pady=20, padx=10)

        # self.name_label = tk.Label(self, text="姓名:", bg="white", font=("微软雅黑", 12))
        # self.name_label.grid(row=2, column=0, pady=20, padx=10, sticky="e")
        # self.name_entry = tk.Entry(self, font=("微软雅黑", 12))
        # self.name_entry.grid(row=2, column=1, pady=20, padx=10)

        # 初始密码不可见状态
        self.password_visibility = False

        # 创建切换密码可见性的按钮
        self.password_visibility_button = tk.Button(self, text="显示密码", command=self.toggle_password_visibility,
                                                    font=("微软雅黑", 12))
        self.password_visibility_button.grid(row=1, column=2, pady=10)

        # 创建注册按钮
        self.register_button = tk.Button(self, text="注册", command=self.register, font=("微软雅黑", 12))
        self.register_button.grid(row=2, column=1, pady=20, padx=10)

        # 创建登录按钮
        self.login_button = tk.Button(self, text="登录", command=self.login, font=("微软雅黑", 12))
        self.login_button.grid(row=2, column=2, pady=20, padx=10)

        # 创建结果标签
        self.result_label = tk.Label(self, text="", bg="white", font=("微软雅黑", 12))
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

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
        # 创建注册窗口
        register_window = tk.Toplevel(self)
        register_window.title("注册")

        # 创建手机号、姓名和密码标签和输入框
        phone_label = tk.Label(register_window, text="手机号:", bg="white", font=("微软雅黑", 12))
        phone_label.grid(row=0, column=0, pady=20, padx=10, sticky="e")
        phone_entry = tk.Entry(register_window, font=("微软雅黑", 12))
        phone_entry.grid(row=0, column=1, pady=20, padx=10)

        name_label = tk.Label(register_window, text="姓名:", bg="white", font=("微软雅黑", 12))
        name_label.grid(row=1, column=0, pady=20, padx=10, sticky="e")
        name_entry = tk.Entry(register_window, font=("微软雅黑", 12))
        name_entry.grid(row=1, column=1, pady=20, padx=10)

        password_label = tk.Label(register_window, text="密码:", bg="white", font=("微软雅黑", 12))
        password_label.grid(row=2, column=0, pady=20, padx=10, sticky="e")
        password_entry = tk.Entry(register_window, show="*", font=("微软雅黑", 12))
        password_entry.grid(row=2, column=1, pady=20, padx=10)

        # 创建确认注册按钮
        confirm_button = tk.Button(register_window, text="确认注册",
                                   command=lambda: self.confirm_register(register_window, phone_entry.get(),
                                                                         name_entry.get(), password_entry.get()),
                                   font=("微软雅黑", 12))
        confirm_button.grid(row=3, column=1, pady=20, padx=10)

    def confirm_register(self, register_window, phone, name, password):
        # 检查手机号和密码是否为空
        if not phone or not password:
            messagebox.showerror("错误", "手机号和密码不能为空！")
            register_window.lift()
            return

        # 检查手机号的唯一性
        sql = f"SELECT 1 FROM 客户数据表 WHERE 手机号 = '{phone}'"
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()
        if result:
            messagebox.showerror("错误", "手机号已被注册，请选择其他手机号！")
            register_window.lift()
            return

        # 查询客户数据表中的账号最大值
        sql = "SELECT MAX(账号) FROM 客户数据表"
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()
        max_account = result[0] if result[0] else 0

        # 生成新的账号
        new_account = max_account[0] + str(int(max_account[1:]) + 1).zfill(6)

        # 在数据库中执行插入操作
        sql = f"INSERT INTO 客户数据表 (账号, 手机号, 姓名, 密码) VALUES ('{new_account}', '{phone}', '{name}', '{password}')"
        print(sql)
        self.app.db.execute(sql)

        # 关闭注册窗口
        register_window.destroy()

        messagebox.showinfo("成功", f"注册成功！\n您的账号是{new_account}")

    def login(self):
        # 获取输入的手机号和密码
        username = self.id_entry.get()
        password = self.password_entry.get()

        # 检查手机号和密码是否匹配
        sql = f"SELECT 账号 FROM 客户数据表 WHERE (账号 = '{username}' OR 手机号 = '{username}') AND 密码 = '{password}'"
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()

        if result:
            # 登录成功，设置应用的用户名和模式，并显示成功页面
            self.app.username = result[0]
            self.app.mode = "customer"
            self.app.show_main_frame()
        else:
            self.result_label.config(text="手机号或密码错误！", fg="red")
