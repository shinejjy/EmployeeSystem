import tkinter as tk
from tkinter import ttk, messagebox

from Base.Base import BaseFrame, EditableTreeview
from Database.SQL import change_code


class EmployeeManagementFrame(BaseFrame):
    def __init__(self, app, window, show, *args, **kwargs):
        super().__init__(app, window, show, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # 标题
        title_label = tk.Label(self, text="员工信息管理", font=("Arial", 16, "bold"), bg="white")
        title_label.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '9员工信息表'"
        self.app.db.execute(query)
        columns = [column[0] for column in self.app.db.cursor.fetchall()]
        print(columns)

        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(self, orient="vertical")
        scrollbar_y.grid(row=1, column=1, sticky=tk.N + tk.S)

        # 创建查询表的横向滚动条
        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        scrollbar_x.grid(row=2, column=0, sticky=tk.E + tk.W)

        # 创建TreeView
        self.treeview = EditableTreeview(self.app.db, '9员工信息表', 5, '工号', None, None, False,
                                         self, columns=columns, show="headings",
                                         xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        self.treeview.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        scrollbar_y.config(command=self.treeview.yview)
        scrollbar_x.config(command=self.treeview.xview)

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=120, minwidth=120)

        add_button = tk.Button(self, text="添加", command=self.add_employee)
        add_button.grid(row=3, column=0, padx=5, sticky=tk.W)

        delete_button = tk.Button(self, text="删除", command=self.delete_employee)
        delete_button.grid(row=3, column=0, padx=5, sticky=tk.E)

        # 创建查询输入框和按钮
        self.search_frame = tk.Frame(self)
        self.search_frame.grid(row=3, column=0)

        self.search_label = tk.Label(self.search_frame, text="查询：")
        self.search_label.grid(row=0, column=0)

        self.search_text = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_text)
        self.search_entry.grid(row=0, column=1)
        self.search_entry.bind("<Return>", self.search_employee)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.show_employee()

    def show_employee(self):
        # 清空表格内容
        self.treeview.delete(*self.treeview.get_children())

        sql = f"SELECT * FROM [9员工信息表]"
        self.app.db.execute(sql)
        employees = self.app.db.cursor.fetchall()

        # 将客户档案信息插入表格中
        for employee in employees:
            employee = list(change_code(employee))
            self.treeview.insert("", tk.END, values=employee)

    def add_employee(self):
        # 销毁修改框
        if self.treeview.entry:
            self.treeview.entry.destroy()
        # 获取当前最大的序号值
        sql = f"SELECT MAX(序号) FROM [9员工信息表]"
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()
        max_index = result[0] if result[0] else 0

        # 生成新的序号值
        new_index = max_index + 1

        # 创建弹出窗口
        popup_window = tk.Toplevel(self.window)
        popup_window.title("添加员工")
        popup_window.geometry("200x100")

        # 创建部门选择下拉框
        department_label = tk.Label(popup_window, text="部门:")
        department_label.pack()
        department_var = tk.StringVar()
        department_combobox = ttk.Combobox(popup_window, textvariable=department_var)
        department_combobox['values'] = ["产品管理部", "内务部", "食品添加剂部", "市场推广部", "外贸部", "信管部",
                                         "研发服务部", "原辅料销售部"]
        department_combobox.pack()

        # 创建确认按钮
        confirm_button = tk.Button(popup_window, text="确认",
                                   command=lambda: self.confirm_add_employee(new_index, department_var.get(),
                                                                             popup_window))
        confirm_button.pack()

    def confirm_add_employee(self, new_index, department, popup_window):
        # 查询部门为选择的部门或者以选择的部门开头的工号的最大值
        sql = f"SELECT MAX(工号) FROM [9员工信息表] WHERE 部门 = '{department}' OR 部门 LIKE '{department}%'"
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()
        max_employee_id = result[0] if result[0] else 0

        # 生成新的工号值
        new_employee_id = max_employee_id[:2] + str(int(max_employee_id[2:]) + 1).zfill(3)

        # 在数据库中执行插入操作
        sql = f"INSERT INTO [9员工信息表] (序号, 部门, 工号) VALUES ({new_index}, '{department}', '{new_employee_id}')"
        self.app.db.execute(sql)

        # 创建一个空白记录，包括序号值、部门和工号
        new_employee = [new_index, department] + [''] * 3 + [new_employee_id, 'Y', '12345']

        # 在表格末尾插入空白记录
        self.treeview.insert("", tk.END, values=new_employee)

        # 关闭弹出窗口
        popup_window.destroy()

    def delete_employee(self):
        # 销毁修改框
        if self.treeview.entry:
            self.treeview.entry.destroy()
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的员工")
            return

        confirm = messagebox.askyesno("确认", "确定要删除选中的员工吗？")
        if confirm:
            for item in selected_items:
                # 获取选中行的数据
                values = self.treeview.item(item)['values']

                # 在数据库中执行删除操作
                sql = f"DELETE FROM [9员工信息表] WHERE 序号 = '{values[0]}'"
                self.app.db.execute(sql)

                # 从表格中删除对应行
                self.treeview.delete(item)

            messagebox.showinfo("提示", "员工删除成功")

    def search_employee(self, event=None):
        keyword = self.search_text.get()

        # 清空表格内容
        self.treeview.delete(*self.treeview.get_children())

        # 查询匹配的辅料
        sql = f"""SELECT * FROM [9员工信息表]
         WHERE 序号 LIKE '%{keyword}%' OR 姓名 LIKE '%{keyword}%' OR 部门 LIKE '%{keyword}%' OR 状态 LIKE '%{keyword}%'
         OR 性别 LIKE '%{keyword}%' OR 职位 LIKE '%{keyword}%' OR 工号 LIKE '%{keyword}%'"""
        self.app.db.execute(sql)
        employees = self.app.db.cursor.fetchall()

        # 将辅料信息插入表格中
        for employee in employees:
            employee = list(change_code(employee))
            self.treeview.insert("", tk.END, values=employee)
