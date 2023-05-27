import tkinter as tk
from tkinter import ttk
from Base.BaseFrame import BaseFrame
from datetime import datetime


class OrderListPage(BaseFrame):
    def __init__(self, app, window, show):
        super().__init__(app, window, show)
        self.app = app
        self.window = window
        self.configure(bg="white")

        # 创建订单树
        columns = [ '辅料编号', '辅料名称', '辅料单价', '订购数量', '价格']
        self.orderTree = ttk.Treeview(self, columns=columns, show='tree headings', displaycolumns='#all')
        self.orderTree.heading('#0', text='时间戳+总价')
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

        # 获取订单列表
        order_list = self.window.order_list

        # 按时间戳从晚到早排序
        order_list.sort(key=lambda x: x["timestamp"], reverse=True)

        # 将订单信息插入订单树
        for order in order_list:
            timestamp = order["timestamp"]
            timestamp_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间戳
            Total_price = str(order['total_price'])
            f_str = timestamp_str + ' ' + Total_price

            # 添加时间戳作为树节点
            parent_node = self.orderTree.insert("", tk.END, text=f_str)

            purchase_list = order["purchase_list"]
            for purchase_item in purchase_list:
                self.orderTree.insert(parent_node, tk.END, values=purchase_item)
