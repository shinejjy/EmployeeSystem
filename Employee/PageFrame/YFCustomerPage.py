import tkinter as tk
from tkinter import ttk

from Base.Base import EditableTable
from Database.SQL import change_code


class YFCustomerFlowUpPage(EditableTable):
    def __init__(self, app, window, show):
        super(YFCustomerFlowUpPage, self).__init__(app, window, show, ['记录人'], ['3研部客户对接表'], [-1], [0], ['序号'])


class YFCustomerRecordPage(EditableTable):
    def __init__(self, app, window, show):
        super(YFCustomerRecordPage, self).__init__(app, window, show, ['联系人'], ['3研部客户流水表'], [-1], [0], ['序号'])


class AuthorizationPage(EditableTable):
    def __init__(self, app, window, show):
        super(AuthorizationPage, self).__init__(app, window, show, ['跟进人'], ['5授权书总表'], [-1], [0], ['序号'])

    def show_customer_page(self):
        # 清空表格内容
        self.tree.delete(*self.tree.get_children())

        # 查询客户档案信息
        sql = f"SELECT * FROM [5授权书总表]"

        self.app.db.execute(sql)
        customers = self.app.db.cursor.fetchall()

        # 将客户档案信息插入表格中
        for customer in customers:
            customer = list(change_code(customer))
            customer.insert(0, customer.pop())
            self.tree.insert("", tk.END, values=customer)

        self.update_filter_combobox()

    def update_filter_combobox(self):
        if hasattr(self, "filter_combobox"):
            self.filter_combobox.destroy()

        # 获取当前表头列名
        column_names = self.tree["columns"]

        if self.table_info_current['search_column'] in column_names:
            # 获取当前表格中的业务员列表
            current_values = set()
            for item in self.tree.get_children():
                value = self.tree.item(item)["values"][column_names.index(self.table_info_current['search_column'])]
                current_values.add(value)

            current_values.add('显示全部')

            # 创建筛选下拉框
            self.filter_combobox = ttk.Combobox(self, values=list(current_values))
            self.filter_combobox.grid(row=2, column=0, sticky=tk.N + tk.S)
            self.filter_combobox.bind("<<ComboboxSelected>>", self.apply_filter)

    def apply_filter(self, event=None):
        selected_value = self.filter_combobox.get()

        # 清空表格内容
        self.tree.delete(*self.tree.get_children())

        # 查询客户档案信息
        if selected_value == '显示全部':
            sql = f"SELECT * FROM [5授权书总表]"
        else:
            sql = f"SELECT * FROM [5授权书总表] WHERE {self.table_info_current['search_column']} = '{selected_value}'"

        self.app.db.execute(sql)
        customers = self.app.db.cursor.fetchall()

        # 将客户档案信息插入表格中
        for customer in customers:
            customer = list(change_code(customer))
            customer.insert(0, customer.pop())
            self.tree.insert("", tk.END, values=customer)
