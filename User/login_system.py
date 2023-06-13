import tkinter as tk
from User.CustomerLoginFrame import CustomerLoginFrame
from User.EmployeeLoginFrame import EmployeeLoginFrame
from Customer.CustomerMainFrame import CustomerMainFrame
from Employee.EmployeeMainFrame import EmployeeMainFrame


class UserLoginSystem:
    def __init__(self, db):
        self.db = db
        self.window = tk.Tk()
        self.window.title("用户登录系统")
        self.window.geometry("500x300")
        self.window.resizable(False, False)
        self.window.configure(bg="white")

        self.user_info = {}

        self.login_frame = None
        self.success_frame = None

        self.create_frame()
        self.show_login_frame()

    def create_frame(self):
        # 创建员工主界面、客户主界面、员工登录界面、客户登录界面
        self.customer_login_frame = CustomerLoginFrame(self, self.window)
        self.employee_login_frame = EmployeeLoginFrame(self, self.window)

    def show_login_frame(self):
        # 显示登录界面（包含切换按钮）
        self.login_frame = tk.Frame(self.window)
        self.login_frame.pack()
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(1, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)

        customer_login_button = tk.Button(self.login_frame, text="客户登录", command=self.show_customer_login_frame)
        customer_login_button.grid(row=0, column=0)

        employee_login_button = tk.Button(self.login_frame, text="员工登录", command=self.show_employee_login_frame)
        employee_login_button.grid(row=0, column=1)

        # 默认为员工登录界面
        self.show_employee_login_frame()

    def show_customer_login_frame(self):
        self.mode = "customer"
        self.login_frame.pack()
        self.customer_login_frame.show()
        self.employee_login_frame.hide()

    def show_employee_login_frame(self):
        self.mode = "employee"
        self.login_frame.pack()
        self.customer_login_frame.hide()
        self.employee_login_frame.show()

    def show_main_frame(self):
        self.customer_login_frame.hide()
        self.employee_login_frame.hide()
        self.login_frame.pack_forget()
        if self.mode == 'employee':
            self.employee_main_frame = EmployeeMainFrame(self, self.window)
            self.window.geometry("600x600")
            self.employee_main_frame.show()
        else:
            self.customer_main_frame = CustomerMainFrame(self, self.window)
            self.window.geometry("600x600")
            self.customer_main_frame.show()

    def run(self):
        self.window.mainloop()
