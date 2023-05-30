import tkinter as tk
from tkinter import ttk
from Database.SQL import change_code
from Base.Base import BaseFrame


class InformationPage(BaseFrame):
    def __init__(self, app, window, show):
        super().__init__(app, window, show)
        # 创建表格
        self.treeview = ttk.Treeview(self, show="headings")
        self.treeview["columns"] = ("属性", "值")
        self.treeview.heading("属性", text="属性")
        self.treeview.heading("值", text="值")
        self.treeview.column("属性", width=100, anchor="center")
        self.treeview.column("值", width=200, anchor="w")
        self.treeview.grid(row=0, column=0, sticky="nsew")

        if show:
            self.show()

    def show(self):
        super(InformationPage, self).show()
        # 展示
        self.show_basic_info()

    def show_basic_info(self):
        # 清空表格
        self.treeview.delete(*self.treeview.get_children())

        # 查询基本信息
        sql = f"SELECT 部门, 姓名, 性别, 职位, 工号, 状态 FROM [9员工信息表] WHERE 工号 = '{self.app.user_info['id']}'"
        self.app.db.execute(sql)
        info = self.app.db.cursor.fetchone()

        if info:
            info = list(change_code(info))
            info[0] = self.app.user_info['login_depart']
            info[3] = self.app.user_info['login_position']
            info[-1] = self.app.user_info['is_leader']
            info_fields = ["部门", "姓名", "性别", "职位", "工号", "状态"]
            for field, value in zip(info_fields, info):
                self.treeview.insert("", "end", values=(field, value))

        # 自动调整表格高度
        self.treeview.bind("<Configure>", self.adjust_treeview_height)

    def adjust_treeview_height(self, event):
        height = self.treeview.winfo_height()
        self.treeview.configure(height=height)

    def clear_info_labels(self):
        self.treeview.delete(*self.treeview.get_children())
