import tkinter as tk
from Base.BaseFrame import BaseFrame
from Employee.PageFrame.InformationPage import InformationPage


class EmployeeMainFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        # 创建界面上方菜单和基本信息框架
        self.create_menu_bar()
        self.pages = []

        self.create_all_pages()

    def create_menu_bar(self):
        self.menu_frame = tk.Frame(self, bg="white")
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        # 创建三个菜单按钮
        self.menu_buttons = []
        menu_names = ["基本信息", "A", "退出登录"]
        for name in menu_names:
            button = tk.Button(self.menu_frame, text=name, command=lambda n=name: self.switch_page(n))
            button.pack(side=tk.LEFT, padx=0, ipadx=20)
            self.menu_buttons.append(button)

    def create_all_pages(self):
        self.information_page = InformationPage(self.app, self, show=False)
        self.pages.append(self.information_page)

    def switch_page(self, page_name):
        self.clear_all_pages()
        if page_name == "基本信息":
            self.information_page.show()
        elif page_name == "A":
            # 切换到A页面的操作
            pass
        elif page_name == "退出登录":
            self.app.show_employee_login_frame()
            self.hide()

    def clear_all_pages(self):
        for page in self.pages:
            page.hide()
