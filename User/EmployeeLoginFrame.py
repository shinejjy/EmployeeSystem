import tkinter as tk
from tkinter import messagebox
from Base.Base import BaseFrame
from Database.SQL import change_code


class EmployeeLoginFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        username_entry_text = tk.StringVar()
        password_entry_text = tk.StringVar()

        # 创建工号标签和输入框
        self.username_label = tk.Label(self, text="工号:", bg="white", font=("微软雅黑", 12))
        self.username_label.grid(row=0, column=0, pady=20, padx=10, sticky="e")
        self.username_entry = tk.Entry(self, font=("微软雅黑", 12), textvariable=username_entry_text)
        self.username_entry.grid(row=0, column=1, pady=20, padx=10)

        username_entry_text.set("XS001")

        # 创建密码标签和输入框
        self.password_label = tk.Label(self, text="密码:", bg="white", font=("微软雅黑", 12))
        self.password_label.grid(row=1, column=0, pady=20, padx=10, sticky="e")
        self.password_entry = tk.Entry(self, show="*", font=("微软雅黑", 12), textvariable=password_entry_text)
        self.password_entry.grid(row=1, column=1, pady=20, padx=10)

        password_entry_text.set("12345")

        # 创建登录按钮
        self.login_button = tk.Button(self, text="登录", command=self.login, font=("微软雅黑", 12))
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 创建结果标签
        self.result_label = tk.Label(self, text="", bg="white", font=("微软雅黑", 12))
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.select_window = None

    def login(self):
        # 获取输入的工号和密码
        userid = self.username_entry.get()
        password = self.password_entry.get()

        # 构建SQL语句，用于查询密码是否匹配
        sql = f"""
        SELECT 密码, 职位, 状态, 部门, 姓名
        FROM [9员工信息表]
        WHERE 工号='{userid}'
        """

        # 读取已注册用户信息
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()
        result = change_code(result)

        if result:
            if result[0] == password:
                # 登录成功，设置应用的用户名和模式，并显示成功页面
                self.app.user_info['name'] = result[4]
                self.app.user_info['id'] = userid
                self.app.mode = "employee"
                if self.select_window is not None and self.select_window.winfo_exists():
                    # 如果之前已经打开了选择职位窗口，则先关闭之前的窗口
                    self.select_window.destroy()
                self.select_depart(result[1:4])
            else:
                self.result_label.config(text="密码错误！", fg="red")
        else:
            self.result_label.config(text="工号不存在！", fg="red")

    def select_depart(self, info_list):
        position, state, depart = info_list

        # self.app.is_leader = True if result[2] == 'L' else False

        depart_li = depart.split('兼')
        position_li = position.split('\n')
        if len(depart_li) == 1:
            self.app.user_info['login_position'] = position
            self.app.user_info['login_depart'] = self.app.user_info['id'][:2]
            self.app.user_info['is_leader'] = True if state == 'L' else False
            print(self.app.user_info['login_depart'])
            self.app.show_main_frame()
        else:
            # 创建一个新的Toplevel窗口来显示多个职位选择
            self.select_window = tk.Toplevel(self)
            self.select_window.title("选择职位")
            self.select_window.resizable(False, False)

            # 创建一个标签显示提示文本
            label = tk.Label(self.select_window, text="请选择您的职位：", font=("微软雅黑", 12))
            label.pack(pady=20)

            # 创建一个列表框来显示多个职位选项
            listbox = tk.Listbox(self.select_window, font=("微软雅黑", 12), height=len(position_li))
            listbox.pack()

            # 将职位选项添加到列表框中
            for position in position_li:
                listbox.insert(tk.END, position)

            depart_dic = {
                '营销中心': 'YX', '原辅料销售部': 'XS', '内务部': 'NW', '食品添加剂部': 'SP',
                '研发服务部': 'YF', '信管部': 'XG', '外贸部': 'WM', '市场推广部': 'TG',
                '产品管理部': 'CP'
            }

            def select_position():
                if listbox.curselection():
                    selected_position = listbox.get(listbox.curselection())
                    position_index = position_li.index(selected_position)
                    selected_depart = depart_li[position_index]
                    self.app.user_info['login_position'] = selected_position
                    self.app.user_info['login_depart'] = depart_dic[selected_depart]
                    self.app.user_info['is_leader'] = True if state.split('\n')[position_index] == 'L' else False
                    self.app.show_main_frame()
                    self.select_window.destroy()
                else:
                    # 如果没有选中职位，显示提示信息或采取其他操作
                    messagebox.showinfo("提示", "请先选择一个职位！", parent=self.select_window)

            # 创建一个确认按钮，点击后执行选择职位的操作
            confirm_button = tk.Button(self.select_window, text="确认", command=select_position, font=("微软雅黑", 12))
            confirm_button.pack(pady=20)

            # 获取当前窗体的左上角坐标
            self.update_idletasks()
            self_width = self.winfo_width()
            self_height = self.winfo_height()
            self_x = self.winfo_rootx()
            self_y = self.winfo_rooty()

            # 设置选择职位窗口相对于当前窗体的位置
            select_window_width = self.select_window.winfo_width()
            select_window_height = self.select_window.winfo_height()
            select_x = self_x + (self_width - select_window_width) // 2
            select_y = self_y + (self_height - select_window_height) // 2
            self.select_window.geometry(f"+{select_x}+{select_y}")

