from tkinter import messagebox, ttk
import tkinter as tk

from Base.Base import EditableTreeview, BaseFrame
from Database.SQL import change_code


class CustomerDevelopSchedule(BaseFrame):
    def __init__(self, app, window, show, ):
        super().__init__(app, window, show)
        table_names = [
            '6客户开发进度表_A客户情况', '6客户开发进度表_B项目情况', '6客户开发进度表_C项目跟进',
            '6客户开发进度表_D授权书情况', '6客户开发进度表_E落地转移情况', '6客户开发进度表_F进度描述'
        ]
        search_columns = ['负责人'] * 6
        p_primary_key_tbss = [[0, 1]] * 6
        p_primary_key_dbss = [[0, 1]] * 6
        primary_keyss = [['开发状态', ' 序号']] * 6

        self.table_names = table_names
        self.table_info = [{
            'search_column': search_column,
            'table_name': table_name,
            'p_primary_key_tbs': p_primary_key_tbs,
            'p_primary_key_dbs': p_primary_key_dbs,
            'primary_keys': primary_keys
        } for search_column, table_name, p_primary_key_tbs, p_primary_key_dbs, primary_keys
            in zip(search_columns, table_names, p_primary_key_tbss, p_primary_key_dbss, primary_keyss)]
        self.table_info_current = self.table_info[0]

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

        # 创建查询表格
        self.tree = EditableTreeview(self.app.db, f"[{self.table_info_current['table_name']}]",
                                     self.table_info_current['p_primary_key_tbs'],
                                     self.table_info_current['primary_keys'],
                                     self.app.user_info['name'], self.table_info_current['search_column'], self,
                                     columns=columns, show="headings", yscrollcommand=scrollbar_y.set,
                                     xscrollcommand=scrollbar_x.set)
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
        # 设置查询表格的表头
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, minwidth=80)

        self.tree.primary_key = self.table_info_current['primary_keys']
        self.tree.p_primary_key_tb = self.table_info_current['p_primary_key_tbs']
        self.tree.search_column = self.table_info_current['search_column']
        self.tree.table_name = self.table_info_current['table_name']