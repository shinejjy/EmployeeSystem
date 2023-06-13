import tkinter as tk
from Base.Base import BaseFrame
from Employee.PageFrame.InformationPage import InformationPage
from Employee.PageFrame.WMCustomerPage import WMCustomerPage
from Employee.PageFrame.YFCustomerPage import YFCustomerFlowUpPage, YFCustomerRecordPage, AuthorizationPage
from Employee.PageFrame.CustomerDevelopSchedule import CustomerDevelopSchedule
from Employee.PageFrame.ProductFeedBackPage import ProductFeedBackPage
from Employee.PageFrame.NWCustomerPage import NWCustomerPage
from Employee.PageFrame.EmployeeManagement import EmployeeManagementFrame


class EmployeeMainFrame(BaseFrame):
    def __init__(self, app, window):
        super().__init__(app, window)

        # 创建界面上方菜单和基本信息框架
        self.pages = []
        self.create_all_pages()

    def create_menu_bar(self, menu_names):
        self.menu_frame = tk.Frame(self, bg="white")
        self.menu_frame.pack(side=tk.TOP)

        # 创建菜单按钮
        self.menu_buttons = []
        row = 0
        col = 0
        for name in menu_names:
            button = tk.Button(self.menu_frame, text=name, command=lambda n=name: self.switch_page(n))
            button.grid(row=row, column=col, padx=5, pady=5, sticky=tk.W + tk.E)
            self.menu_buttons.append(button)

            # 更新行和列的值
            col += 1
            if col >= 4:
                col = 0
                row += 1

    def create_all_pages(self):
        menu_names = []
        self.information_page = InformationPage(self.app, self, show=False)
        menu_names.append('基本信息')
        self.pages.append(self.information_page)

        # 外贸部权限
        if self.app.user_info['login_depart'] == 'WM' or \
                self.app.user_info['login_depart'] == 'YX':
            self.wm_customer_page = WMCustomerPage(self.app, self, show=False)
            self.pages.append(self.wm_customer_page)
            menu_names.append('外贸部客户档案表')

        # 研发服务部权限
        if self.app.user_info['login_depart'] == 'YF' or \
                self.app.user_info['login_depart'] == 'YX':
            self.yf_customer_flow_up_page = YFCustomerFlowUpPage(self.app, self, show=False)
            self.pages.append(self.yf_customer_flow_up_page)
            menu_names.append('研部客户对接表')

            self.yf_customer_record_page = YFCustomerRecordPage(self.app, self, show=False)
            self.pages.append(self.yf_customer_record_page)
            menu_names.append('研部客户流水表')

            self.authorization_page = AuthorizationPage(self.app, self, show=False)
            self.pages.append(self.authorization_page)
            menu_names.append('授权书总表')

        # 销售部权限
        if self.app.user_info['login_depart'] == 'XS' or \
                self.app.user_info['login_depart'] == 'YX':
            self.customer_develop_schedule = CustomerDevelopSchedule(self.app, self, show=False)
            self.pages.append(self.customer_develop_schedule)
            menu_names.append('客户开发进度表')

        # 产品管理部权限
        if self.app.user_info['login_depart'] == 'CP' or \
                self.app.user_info['login_depart'] == 'YX':
            self.product_feedback_page = ProductFeedBackPage(self.app, self, show=False)
            self.pages.append(self.product_feedback_page)
            menu_names.append('产品问题反馈流水表')

        # 内务部权限
        if self.app.user_info['login_depart'] == 'NW' or \
                self.app.user_info['login_depart'] == 'YX':
            self.nw_customer_page = NWCustomerPage(self.app, self, show=False)
            self.pages.append(self.nw_customer_page)
            menu_names.append('台账总表')

        if self.app.user_info['login_depart'] == 'YX':
            self.employee_management_page = EmployeeManagementFrame(self.app, self, show=False)
            self.pages.append(self.employee_management_page)
            menu_names.append('员工管理')

        menu_names.append('退出登录')

        self.create_menu_bar(menu_names)

    def switch_page(self, page_name):
        self.clear_all_pages()
        if page_name == "基本信息":
            self.information_page.show()
        elif page_name == "外贸部客户档案表":
            self.wm_customer_page.show()
        elif page_name == "研部客户对接表":
            self.yf_customer_flow_up_page.show()
        elif page_name == "研部客户流水表":
            self.yf_customer_record_page.show()
        elif page_name == "授权书总表":
            self.authorization_page.show()
        elif page_name == "客户开发进度表":
            self.customer_develop_schedule.show()
        elif page_name == "产品问题反馈流水表":
            self.product_feedback_page.show()
        elif page_name == "台账总表":
            self.nw_customer_page.show()
        elif page_name == "员工管理":
            self.employee_management_page.show()
        elif page_name == "退出登录":
            self.app.window.geometry("500x300")
            self.app.show_employee_login_frame()
            self.hide()

    def clear_all_pages(self):
        for page in self.pages:
            page.hide()
