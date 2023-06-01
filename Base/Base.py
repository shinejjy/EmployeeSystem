import tkinter as tk
from tkinter import ttk, messagebox

from Database.SQL import change_code


class BaseFrame(tk.Frame):
    def __init__(self, app, window, show=True, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.app = app
        self.window = window
        self.configure(bg="white")
        if not show:
            self.hide()

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()


class EditableTreeview(ttk.Treeview):
    def __init__(self, db, table_name, p_primary_key_tb, primary_key,
                 name=None, search_column=None, multi_keys=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Double-1>', self.edit_cell)
        self.entry = None
        self.entry_index = None
        self.db = db
        self.table_name = table_name
        self.p_primary_key_tb = p_primary_key_tb
        self.primary_key = primary_key
        self.multi_keys = multi_keys

        self.name = name
        self.search_column = search_column

    def edit_cell(self, event):
        # 获取双击的单元格位置
        cell = self.identify('item', event.x, event.y)
        column = self.identify('column', event.x, event.y)
        if cell and column:
            if self.name and self.search_column:
                if self.name != self.item(cell)['values'][self["columns"].index(self.search_column)]:
                    return
            value = self.item(cell)['values'][int(column[1:]) - 1]
            # 创建编辑框并定位到双击的单元格
            self.edit_entry(cell, column, value)

    def edit_entry(self, cell, column, value):
        # 如果已存在编辑框，先销毁
        if self.entry:
            self.entry.destroy()

        # 获取列的宽度
        column_width = self.column(column)["width"]

        # 创建编辑框并定位
        x, y, _, _ = self.bbox(cell, column)
        entry_text = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=entry_text)
        entry_text.set(value)
        self.entry.place(x=x, y=y, width=column_width)
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda event: self.save_entry(cell, column))
        self.entry.bind('<Escape>', lambda event: self.cancel_edit())

        # 记录编辑的单元格位置
        self.entry_index = (cell, column)

    def save_entry(self, cell, column):
        value = self.entry.get()
        self.set(cell, column, value)

        if not self.multi_keys:
            primary_key_value = self.item(cell)['values'][self.p_primary_key_tb]
            # 构建 UPDATE SQL 语句
            sql = f"""UPDATE [{self.table_name}] SET {self.column(column)['id']} = '{value}'
            WHERE {self.primary_key} = '{primary_key_value}'"""
        else:
            primary_key_values = [self.item(cell)['values'][position] for position in self.p_primary_key_tb]
            condition = " AND ".join([f"{primary_key} = '{primary_key_value}'"
                                      for primary_key, primary_key_value in zip(self.primary_key, primary_key_values)])
            sql = f"""UPDATE [{self.table_name}] SET {self.column(column)['id']} = '{value}'
            WHERE {condition}"""

        print(sql)

        self.db.execute(sql)
        self.entry.destroy()
        self.entry = None
        self.entry_index = None

    def cancel_edit(self):
        if self.entry:
            self.entry.destroy()
            self.entry = None
            self.entry_index = None


class EditableTable(BaseFrame):
    def __init__(self, app, window, show,
                 search_columns, table_names, p_primary_key_dbs,
                 p_primary_key_tbs, primary_keys, multi_primary=False):
        super().__init__(app, window, show)
        self.table_names = table_names
        self.table_info = [{
            'search_column': search_column,
            'table_name': table_name,
            'p_primary_key_tb': p_primary_key_tb,
            'p_primary_key_db': p_primary_key_db,
            'primary_key': primary_key
        } for search_column, table_name, p_primary_key_tb, p_primary_key_db, primary_key
            in zip(search_columns, table_names, p_primary_key_tbs, p_primary_key_dbs, primary_keys)]
        self.table_info_current = self.table_info[0]
        self.multi_primary = multi_primary

        self.table_combobox = ttk.Combobox(self, values=table_names)
        self.table_combobox.current(0)  # 默认选择第一个列表
        self.table_combobox.grid(row=0, column=0, sticky=tk.N + tk.S)
        self.table_combobox.bind("<<ComboboxSelected>>", self.switch_table)

        self.configure(bg="white")

        # 创建查询表的纵向滚动条
        scrollbar_y = ttk.Scrollbar(self)
        scrollbar_y.grid(row=1, column=1, sticky=tk.N + tk.S)

        # 创建查询表的横向滚动条
        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        scrollbar_x.grid(row=2, column=0, sticky=tk.E + tk.W)

        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self.table_info_current['table_name']}'"
        self.app.db.execute(query)
        columns = [column[0] for column in self.app.db.cursor.fetchall()]
        if not self.multi_primary:
            columns.insert(0, columns.pop())

        # 创建查询表格
        self.tree = EditableTreeview(self.app.db, f"[{self.table_info_current['table_name']}]",
                                     self.table_info_current['p_primary_key_tb'],
                                     self.table_info_current['primary_key'],
                                     self.app.user_info['name'], self.table_info_current['search_column'],
                                     self.multi_primary, self, columns=columns, show="headings",
                                     yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # 设置查询表格的表头
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, minwidth=80)

        self.tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # 创建按钮
        self.add_button = tk.Button(self, text="添加", command=self.add_customer)
        self.delete_button = tk.Button(self, text="删除", command=self.delete_customer)

        self.add_button.grid(row=3, column=0, sticky=tk.W)
        self.delete_button.grid(row=3, column=0, sticky=tk.E)

        # 设置行列权重和填充
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.show_customer_page()

    def show_customer_page(self):
        # 清空表格内容
        self.tree.delete(*self.tree.get_children())

        # 查询客户档案信息
        if self.app.user_info['is_leader']:
            sql = f"SELECT * FROM [{self.table_info_current['table_name']}]"
        else:
            sql = f"SELECT * FROM [{self.table_info_current['table_name']}] WHERE {self.table_info_current['search_column']} = '{self.app.user_info['name']}'"

        self.app.db.execute(sql)
        customers = self.app.db.cursor.fetchall()

        # 将客户档案信息插入表格中
        for customer in customers:
            customer = list(change_code(customer))
            if not self.multi_primary:
                customer.insert(self.table_info_current['p_primary_key_tb'],
                                customer.pop(self.table_info_current['p_primary_key_db']))
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

            if self.app.user_info['is_leader']:
                current_values.add('显示全部')

            # 创建筛选下拉框
            self.filter_combobox = ttk.Combobox(self, values=list(current_values))
            self.filter_combobox.grid(row=3, column=0, sticky=tk.N + tk.S)
            self.filter_combobox.bind("<<ComboboxSelected>>", self.apply_filter)

    def apply_filter(self, event=None):
        selected_value = self.filter_combobox.get()

        # 清空表格内容
        self.tree.delete(*self.tree.get_children())

        # 查询客户档案信息
        if self.app.user_info['is_leader']:
            if selected_value == '显示全部':
                sql = f"SELECT * FROM [{self.table_info_current['table_name']}]"
            else:
                sql = f"SELECT * FROM [{self.table_info_current['table_name']}] WHERE {self.table_info_current['search_column']} = '{selected_value}'"
        else:
            sql = f"""SELECT * FROM [{self.table_info_current['table_name']}] 
            WHERE {self.table_info_current['search_column']} = '{self.app.user_info['name']}' AND {self.table_info_current['search_column']} = '{selected_value}'"""

        self.app.db.execute(sql)
        customers = self.app.db.cursor.fetchall()

        # 将客户档案信息插入表格中
        for customer in customers:
            customer = list(change_code(customer))
            if not self.multi_primary:
                customer.insert(0, customer.pop())
            self.tree.insert("", tk.END, values=customer)

    def add_customer(self):
        # 销毁修改框
        if self.tree.entry:
            self.tree.entry.destroy()
        # 获取当前最大的序号值
        sql = f"SELECT MAX({self.table_info_current['primary_key']}) FROM [{self.table_info_current['table_name']}]"
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()
        max_index = result[0] if result[0] else 0

        # 生成新的序号值
        new_index = max_index + 1

        # 在数据库中执行插入操作
        sql = f"INSERT INTO [{self.table_info_current['table_name']}] ({self.table_info_current['primary_key']}) VALUES ({new_index})"
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
                sql = f"DELETE FROM [{self.table_info_current['table_name']}] WHERE {self.table_info_current['primary_key']} = '{values[0]}'"
                self.app.db.execute(sql)

                # 从表格中删除对应行
                self.tree.delete(item)

            messagebox.showinfo("提示", "客户删除成功")

    def switch_table(self, event=None):
        current_table = self.table_combobox.get()
        self.table_info_current = self.table_info[self.table_names.index(current_table)]
        self.update_table_frame()
        self.show_customer_page()

    def update_table_frame(self):
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self.table_info_current['table_name']}'"
        self.app.db.execute(query)
        columns = [column[0] for column in self.app.db.cursor.fetchall()]
        self.tree.configure(columns=columns)
        # 设置查询表格的表头
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, minwidth=80)

        self.tree.primary_key = self.table_info_current['primary_key']
        self.tree.p_primary_key_tb = self.table_info_current['p_primary_key_tb']
        self.tree.search_column = self.table_info_current['search_column']
        self.tree.table_name = self.table_info_current['table_name']
