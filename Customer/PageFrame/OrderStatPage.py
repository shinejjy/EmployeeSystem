import tkinter as tk
from collections import defaultdict
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Base.Base import BaseFrame
from Database.SQL import change_code


class OrderStatsPage(BaseFrame):
    def __init__(self, app, window, show):
        super().__init__(app, window, show)
        # 创建辅料名称和规格下拉框以及查询按钮
        self.material_label = tk.Label(self, text="辅料名称:", bg="white", font=("微软雅黑", 12))
        self.material_label.grid(row=0, column=0, pady=20, padx=10, sticky="e")

        # 创建辅料名称下拉框
        self.material_combo = ttk.Combobox(self, font=("微软雅黑", 12))
        self.material_combo.grid(row=0, column=1, pady=10, padx=10)
        self.material_combo.bind("<<ComboboxSelected>>", self.update_spec_options)

        self.spec_label = tk.Label(self, text="规格:", bg="white", font=("微软雅黑", 12))
        self.spec_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")

        # 创建规格编码下拉框
        self.spec_combo = ttk.Combobox(self, font=("微软雅黑", 12))
        self.spec_combo.grid(row=1, column=1, pady=10, padx=10)

        self.query_button = tk.Button(self, text="查询", command=self.query_orders, font=("微软雅黑", 12))
        self.query_button.grid(row=2, column=0, pady=10, padx=10)

        # 创建图表容器
        self.figure = Figure(figsize=(4, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.figure.patch.set_facecolor('white')  # 设置图表背景色为白色
        self.figure.set_facecolor('white')  # 设置子图背景色为白色

        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, ipadx=20, ipady=20)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 获取所有辅料名称和规格编码选项
        self.material_options = self.get_material_options()
        self.spec_options = []

        # 设置辅料名称下拉框选项
        self.material_combo["values"] = self.material_options

    def get_material_options(self):
        # 从数据库中获取所有辅料名称选项
        sql = "SELECT DISTINCT 品名 FROM [1药用辅料产品规格编码设置表]"
        self.app.db.execute(sql)
        return [change_code(row)[0] for row in self.app.db.cursor.fetchall()]

    def update_spec_options(self, event):
        # 根据选定的辅料名称更新规格编码下拉框选项
        selected_material = self.material_combo.get()

        if selected_material:
            # 从数据库中获取选定辅料名称的规格编码选项
            sql = f"SELECT 规格编码 FROM [1药用辅料产品规格编码设置表] WHERE 品名 = '{selected_material}'"
            self.app.db.execute(sql)
            self.spec_options = [change_code(row)[0] for row in self.app.db.cursor.fetchall()]
        else:
            self.spec_options = []

        # 设置规格编码下拉框选项
        self.spec_combo["values"] = self.spec_options

    def query_orders(self):
        material_name = self.material_combo.get()
        spec = self.spec_combo.get()

        # 根据查询条件从数据库中获取订单数据
        if material_name and spec:
            sql = f"""SELECT 时间戳, 订购数量, 价格
                      FROM 客户辅料订单
                      WHERE 辅料名称 = '{material_name}' AND 辅料编号 = '{spec}'
                   """
        elif material_name:
            sql = f"""SELECT 时间戳, 订购数量, 价格
                      FROM 客户辅料订单
                      WHERE 辅料名称 = '{material_name}'
                   """
        else:
            # 没有选择辅料名称，不执行查询操作
            return

        self.app.db.execute(sql)
        order_data = self.app.db.cursor.fetchall()
        if not order_data:
            # 订单数据为空，显示提示信息
            messagebox.showinfo("No Orders", "订单表中暂无此辅料")
            return

        # 统计数据
        order_dates = [data[0][:10] for data in order_data]
        order_quantities = [data[1] for data in order_data]
        order_prices = [float(data[2]) for data in order_data]

        # 利用字典统计相同日期的订单数量和订单总价
        quantity_by_date = defaultdict(float)
        price_by_date = defaultdict(float)

        for date, quantity, price in zip(order_dates, order_quantities, order_prices):
            quantity_by_date[date] += quantity
            price_by_date[date] += price

        # 提取统计后的数据
        aggregated_dates = list(quantity_by_date.keys())
        aggregated_quantities = list(quantity_by_date.values())
        aggregated_prices = list(price_by_date.values())

        # 清空图表
        self.figure.clear()

        # 创建包含两个子图的网格
        gs = self.figure.add_gridspec(1, 2, hspace=1)

        # 子图1：订单数量
        ax1 = self.figure.add_subplot(gs[0, 0])

        # 绘制当日统计柱状图（订单数量）
        ax1.bar(aggregated_dates, aggregated_quantities)
        ax1.set_ylabel('Quantity')
        ax1.set_title('Daily Quantity')

        # 子图2：订单总价
        ax2 = self.figure.add_subplot(gs[0, 1])

        # 绘制当日统计柱状图（订单总价）
        ax2.bar(aggregated_dates, aggregated_prices, color='r')
        ax2.set_ylabel('Price')
        ax2.set_title('Daily Price')

        # 调整子图之间的间距
        gs.tight_layout(self.figure)

        # 调整x轴刻度标签旋转角度
        self.figure.autofmt_xdate(rotation=10)

        # 刷新图表
        self.canvas.draw()







