import tkinter as tk
from tkinter import messagebox

from Base.Base import BaseFrame
from Customer.PageFrame.MaterialsPage import MaterialsPage
from Customer.PageFrame.OrderListPage import OrderListPage
from Customer.PageFrame.OrderStatPage import OrderStatsPage


# 登录成功界面

class CustomerMainFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        # 创建界面上方菜单和基本信息框架
        self.create_menu_bar()

        self.order_list = []
        self.pages = []
        self.create_all_page()

    def create_menu_bar(self):
        self.menu_frame = tk.Frame(self, bg="white")
        self.menu_frame.pack(side=tk.TOP)

        # 创建菜单按钮
        self.menu_buttons = []
        menu_names = ["辅料查询", "订购查询", "统计", "退出登录"]
        for name in menu_names:
            button = tk.Button(self.menu_frame, text=name, command=lambda n=name: self.switch_page(n))
            button.pack(side=tk.LEFT, padx=0, ipadx=20)
            self.menu_buttons.append(button)

    def create_all_page(self):
        self.materials_page = MaterialsPage(self.app, self, show=False)
        self.pages.append(self.materials_page)
        self.order_list_page = OrderListPage(self.app, self, show=False)
        self.pages.append(self.order_list_page)
        self.order_stat_page = OrderStatsPage(self.app, self, show=False)
        self.pages.append(self.order_stat_page)

    def switch_page(self, page_name):
        self.clear_all_pages()
        if page_name == "辅料查询":
            self.materials_page.show()
        elif page_name == "订购查询":
            self.order_list_page.show()
        elif page_name == "统计":
            self.order_stat_page.show()
        elif page_name == '退出登录':
            self.app.window.geometry("500x300")
            self.app.show_customer_login_frame()
            self.hide()

    def place_order(self, material):
        # 获取选择的辅料信息
        pno, pna, ppr = material

        # 模拟订购辅料的操作，可以在此处添加相应的逻辑

        # 提示订购成功
        messagebox.showinfo("订购成功", f"已成功订购辅料：{pna}")

    def clear_all_pages(self):
        for page in self.pages:
            page.hide()
