import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Base.Base import BaseFrame, EditableTreeview
from Database.SQL import change_code


class WMCustomerPage(BaseFrame):
    def __init__(self, app, window, show):
        super().__init__(app, window, show)
        self.configure(bg="white")

        # 创建查询表的纵向滚动条
        scrollbar_y = ttk.Scrollbar(self)
        scrollbar_y.grid(row=0, column=1, sticky=tk.N + tk.S)

        # 创建查询表的横向滚动条
        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        scrollbar_x.grid(row=1, column=0, sticky=tk.E + tk.W)

        table_name = '2外贸部客户档案表'
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
        self.app.db.execute(query)
        columns = [column[0] for column in self.app.db.cursor.fetchall()]
        columns.insert(0, columns.pop())

        # 创建查询表格
        self.tree = EditableTreeview(self, columns=columns, show="headings", yscrollcommand=scrollbar_y.set,
                                     xscrollcommand=scrollbar_x.set)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # 设置查询表格的表头
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, minwidth=80)

        self.tree.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # 创建按钮
        self.add_button = tk.Button(self, text="添加", command=self.add_customer)
        self.delete_button = tk.Button(self, text="删除", command=self.delete_customer)

        self.add_button.grid(row=2, column=0, sticky=tk.W)
        self.delete_button.grid(row=2, column=0, sticky=tk.E)

        # 设置行列权重和填充
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.tree.bind('<Button-1>', self.update_filter_combobox)

        self.show_customer_page()

    def show_customer_page(self):
        # 清空表格内容
        self.tree.delete(*self.tree.get_children())

        # 查询客户档案信息
        if self.app.user_info['is_leader']:
            sql = "SELECT * FROM [2外贸部客户档案表]"
        else:
            sql = f"SELECT * FROM [2外贸部客户档案表] WHERE 业务员 = '{self.app.user_info['name']}'"

        self.app.db.execute(sql)
        customers = self.app.db.cursor.fetchall()

        # 将客户档案信息插入表格中
        for customer in customers:
            customer = list(change_code(customer))
            customer.insert(0, customer.pop())
            self.tree.insert("", tk.END, values=customer)

    def update_filter_combobox(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if item is None and column == '业务员':
            # 清除之前的筛选下拉框
            if hasattr(self, "filter_combobox"):
                self.filter_combobox.destroy()

            # 获取当前表头列名
            column_names = self.tree["columns"]

            if "业务员" in column_names:
                # 获取当前表格中的业务员列表
                current_values = set()
                for item in self.tree.get_children():
                    value = self.tree.item(item)["values"][column_names.index("业务员")]
                    current_values.add(value)

                # 创建筛选下拉框
                self.filter_combobox = ttk.Combobox(self, values=list(current_values))
                self.filter_combobox.grid(row=0, column=column_names.index("业务员"), sticky=tk.N + tk.S + tk.E + tk.W)
                self.filter_combobox.bind("<<ComboboxSelected>>", self.apply_filter)

    def apply_filter(self, event=None):
        selected_value = self.filter_combobox.get()

        # 清空表格内容
        self.tree.delete(*self.tree.get_children())

        # 查询客户档案信息
        if self.app.user_info['is_leader']:
            sql = f"SELECT * FROM [2外贸部客户档案表] WHERE 业务员 = '{selected_value}'"
        else:
            sql = f"SELECT * FROM [2外贸部客户档案表] WHERE 业务员 = '{self.app.user_info['name']}' AND 业务员 = '{selected_value}'"

        self.app.db.execute(sql)
        customers = self.app.db.cursor.fetchall()

        # 将客户档案信息插入表格中
        for customer in customers:
            customer = list(change_code(customer))
            customer.insert(0, customer.pop())
            self.tree.insert("", tk.END, values=customer)

    def add_customer(self):
        # 销毁修改框
        if self.tree.entry:
            self.tree.entry.destroy()
        # 获取当前最大的序号值
        sql = "SELECT MAX(序号) FROM [2外贸部客户档案表]"
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()
        max_index = result[0] if result[0] else 0

        # 生成新的序号值
        new_index = max_index + 1

        # 在数据库中执行插入操作
        sql = f"INSERT INTO [2外贸部客户档案表] (序号) VALUES ({new_index})"
        self.app.db.execute(sql)

        # 创建一个空白记录，包括序号值
        new_customer = [new_index] + [''] * (len(self.tree["columns"]) - 1)

        # 在表格末尾插入空白记录
        self.tree.insert("", tk.END, values=new_customer)
        self.show_customer_page()

    def delete_customer(self):
        # 销毁修改框
        if self.tree.entry:
            self.tree.entry.destroy()
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的客户")
            return

        confirm = messagebox.askyesno("确认", "确定要删除选中的客户吗？")
        if confirm:
            for item in selected_items:
                # 获取选中行的数据
                values = self.tree.item(item)['values']

                # 在数据库中执行删除操作
                sql = f"DELETE FROM [2外贸部客户档案表] WHERE 序号 = '{values[0]}'"
                self.app.db.execute(sql)

                # 从表格中删除对应行
                self.tree.delete(item)

            messagebox.showinfo("提示", "客户删除成功")
