import tkinter as tk
from Base.Base import BaseFrame
from Employee.PageFrame.InformationPage import InformationPage
from Employee.PageFrame.WMCustomerPage import WMCustomerPage


class EmployeeMainFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        # 创建界面上方菜单和基本信息框架
        self.pages = []
        self.create_all_pages()

    def create_menu_bar(self, menu_names):
        self.menu_frame = tk.Frame(self, bg="white")
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        # 创建三个菜单按钮
        self.menu_buttons = []
        for name in menu_names:
            button = tk.Button(self.menu_frame, text=name, command=lambda n=name: self.switch_page(n))
            button.pack(side=tk.LEFT, padx=0, ipadx=20)
            self.menu_buttons.append(button)

    def create_all_pages(self):
        menu_names = []
        self.information_page = InformationPage(self.app, self, show=False)
        menu_names.append('基本信息')
        self.pages.append(self.information_page)

        if self.app.user_info['login_depart'] == 'WM':
            self.wm_customer_page = WMCustomerPage(self.app, self, show=False)
            self.pages.append(self.wm_customer_page)
            menu_names.append('外贸部客户档案表')

        menu_names.append('退出登录')

        self.create_menu_bar(menu_names)

    def switch_page(self, page_name):
        self.clear_all_pages()
        if page_name == "基本信息":
            self.information_page.show()
        elif page_name == "外贸部客户档案表":
            self.wm_customer_page.show()
        elif page_name == "退出登录":
            self.app.show_employee_login_frame()
            self.hide()

    def clear_all_pages(self):
        for page in self.pages:
            page.hide()
