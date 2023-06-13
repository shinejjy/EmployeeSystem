import tkinter as tk
from tkinter import ttk
from Base.Base import BaseFrame
from datetime import datetime

from Database.SQL import change_code


class OrderListPage(BaseFrame):
    def __init__(self, app, window, show):
        super().__init__(app, window, show)
        self.app = app
        self.window = window
        self.configure(bg="white")

        # 创建订单树
        columns = ['辅料编号', '辅料名称', '辅料单价', '订购数量', '价格']
        self.orderTree = ttk.Treeview(self, columns=columns, show='tree headings', displaycolumns='#all')
        self.orderTree.heading('#0', text='订单号')
        self.orderTree.column('#0', width=180)
        for col in columns:
            self.orderTree.heading(col, text=col)
            self.orderTree.column(col, width=65)
        self.orderTree.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # 创建滚动条
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.orderTree.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.orderTree.configure(yscrollcommand=scrollbar.set)

        update_button = tk.Button(self, text='更新', command=self.load_order_list)
        update_button.grid(row=1, column=0)

    def load_order_list(self):
        # 清空订单树
        self.orderTree.delete(*self.orderTree.get_children())

        # 查询客户辅料订单表，获取订单列表
        sql = "SELECT DISTINCT(时间戳) FROM 客户辅料订单"
        self.app.db.execute(sql)
        order_list = self.app.db.cursor.fetchall()
        # 按时间戳从晚到早排序
        order_list.sort(reverse=True)

        # 将订单信息插入订单树
        for order in order_list:
            timestamp = order[0]

            sql = f"SELECT * FROM 客户辅料订单 WHERE 时间戳 = '{timestamp}'"
            self.app.db.execute(sql)
            purchase_list = self.app.db.cursor.fetchall()
            order_name = str(purchase_list[0][1])

            # 添加时间戳作为树节点
            parent_node = self.orderTree.insert("", tk.END, text=order_name)

            for purchase_item in purchase_list:
                purchase_item = change_code(purchase_item)
                values = purchase_item[5:]
                self.orderTree.insert(parent_node, tk.END, values=values)

            self.orderTree.insert(parent_node, tk.END, values=('', '', '', '总价', str(purchase_list[0][3])))
