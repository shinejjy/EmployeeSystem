import tkinter as tk
from Base.BaseFrame import BaseFrame
from Database.SQL import change_code


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
