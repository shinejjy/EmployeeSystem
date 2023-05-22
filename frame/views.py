import tkinter as tk
from frame.easy_sql import change_code


class BaseFrame(tk.Frame):
    def __init__(self, app, window, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.app = app
        self.window = window
        self.configure(bg="white")

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()


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


class EmployeeLoginFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        # 创建工号标签和输入框
        self.username_label = tk.Label(self, text="工号:", bg="white", font=("微软雅黑", 12))
        self.username_label.grid(row=0, column=0, pady=20, padx=10, sticky="e")
        self.username_entry = tk.Entry(self, font=("微软雅黑", 12))
        self.username_entry.grid(row=0, column=1, pady=20, padx=10)

        # 创建密码标签和输入框
        self.password_label = tk.Label(self, text="密码:", bg="white", font=("微软雅黑", 12))
        self.password_label.grid(row=1, column=0, pady=20, padx=10, sticky="e")
        self.password_entry = tk.Entry(self, show="*", font=("微软雅黑", 12))
        self.password_entry.grid(row=1, column=1, pady=20, padx=10)

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


# 登录成功界面
class EmployeeMainFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        # 创建界面上方菜单和基本信息框架
        self.create_menu_bar()
        self.create_info_widgets()

        # 默认显示基本信息页面
        self.show_basic_info_page()

    def create_menu_bar(self):
        self.menu_frame = tk.Frame(self, bg="white")
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        # 创建三个菜单按钮
        self.menu_buttons = []
        menu_names = ["基本信息", "A", "退出登录"]
        for name in menu_names:
            button = tk.Button(self.menu_frame, text=name, command=lambda n=name: self.switch_page(n))
            button.pack(side=tk.LEFT, padx=0, ipadx=20)
            self.menu_buttons.append(button)

    def create_info_widgets(self):
        self.info_frame = tk.Frame(self, bg="white")
        self.info_frame.pack(fill=tk.BOTH, padx=20, pady=20)

        self.info_labels = {}

    def show_basic_info_page(self):
        # 重置基本信息页面
        self.clear_info_frame()

        # 查询员工基本信息
        sql = f"""
        SELECT DEPT,SN,SSex,SP,SID,SS
        FROM EmployeeInformation
        WHERE SID = '{self.app.username}'
        """

        self.app.db.execute(sql)
        info = self.app.db.cursor.fetchone()

        if info:
            # 转换编码形式
            info = change_code(info)
            info_data = {
                "部门": info[0],
                "姓名": info[1],
                "性别": info[2],
                "职位": info[3],
                "工号": info[4],
                "状态": info[5]
            }
        else:
            info_data = {
                "部门": '',
                "姓名": '',
                "性别": '',
                "职位": '',
                "工号": '',
                "状态": ''
            }

        # 将员工基本信息显示在基本信息页面中
        row = 0
        for key, value in info_data.items():
            label = tk.Label(self.info_frame, text=f"{key}: {value}", bg="white")
            label.grid(row=row, column=0, sticky="w")
            self.info_labels[key] = label
            row += 1

    def clear_info_frame(self):
        for label in self.info_labels.values():
            label.grid_forget()

    def switch_page(self, page_name):
        if page_name == "基本信息":
            self.show_basic_info_page()
        elif page_name == "A":
            # 切换到A页面的操作
            pass
        elif page_name == "退出登录":
            self.app.show_employee_login_frame()
            self.hide()

    def show(self):
        super(EmployeeMainFrame, self).show()
        self.show_basic_info_page()


class CustomMainFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        # 创建界面上方菜单和基本信息框架
        self.create_menu_bar()
        self.create_info_widgets()

        # 默认显示辅料查询页面
        self.show_materials_page()

    def create_menu_bar(self):
        self.menu_frame = tk.Frame(self, bg="white")
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        # 创建菜单按钮
        self.menu_buttons = []
        menu_names = ["辅料查询", "订购辅料", "开票付款", "订购查询", "统计"]
        for name in menu_names:
            button = tk.Button(self.menu_frame, text=name, command=lambda n=name: self.switch_page(n))
            button.pack(side=tk.LEFT, padx=0, ipadx=20)
            self.menu_buttons.append(button)

    def create_info_widgets(self):
        self.info_frame = tk.Frame(self, bg="white")
        self.info_frame.pack(fill=tk.BOTH, padx=20, pady=20)

        self.info_labels = {}

    def show_materials_page(self):
        # 重置辅料查询页面
        self.clear_info_frame()

        # 查询可订购辅料的详细情况
        sql = "SELECT PNO, PNA, PPR FROM MedicinalIngredients"
        self.app.db.execute(sql)
        materials = self.app.db.cursor.fetchall()

        # 将辅料信息显示在查询页面中
        row = 0
        for material in materials:
            material = change_code(material)
            pno, pna, ppr = material
            label = tk.Label(self.info_frame, text=f"辅料编号: {pno}\n辅料名称: {pna}\n辅料单价: {ppr}", bg="white")
            label.grid(row=row, column=0, sticky="w")
            self.info_labels[pno] = label

            # 创建订购按钮
            button = tk.Button(self.info_frame, text="订购", command=lambda m=material: self.place_order(m))
            button.grid(row=row, column=1)
            self.info_labels[pno + "_button"] = button

            row += 1

    def clear_info_frame(self):
        for label in self.info_labels.values():
            label.grid_forget()

    def switch_page(self, page_name):
        if page_name == "辅料查询":
            self.show_materials_page()
        elif page_name == "订购辅料":
            # 切换到订购辅料页面的操作
            pass
        elif page_name == "开票付款":
            # 切换到开票付款页面的操作
            pass
        elif page_name == "订购查询":
            # 切换到订购查询页面的操作
            pass
        elif page_name == "统计":
            # 切换到统计页面的操作
            pass

    def place_order(self, material):
        # 获取选择的辅料信息
        pno, pna, ppr = material

        # 模拟订购辅料的操作，可以在此处添加相应的逻辑

        # 提示订购成功
        tk.messagebox.showinfo("订购成功", f"已成功订购辅料：{pna}")

    def show(self):
        super(CustomMainFrame, self).show()
        self.show_materials_page()
