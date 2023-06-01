import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Base.Base import BaseFrame


class OrderStatsPage(BaseFrame):
    def __init__(self, app, window, show):
        super().__init__(app, window, show)
        # 创建辅料名称和规格输入框以及查询按钮
        self.material_label = tk.Label(self, text="辅料名称:", bg="white", font=("微软雅黑", 12))
        self.material_label.grid(row=0, column=0, pady=20, padx=10, sticky="e")
        self.material_entry = tk.Entry(self, font=("微软雅黑", 12))
        self.material_entry.grid(row=0, column=1, pady=20, padx=10)

        self.spec_label = tk.Label(self, text="规格:", bg="white", font=("微软雅黑", 12))
        self.spec_label.grid(row=1, column=0, pady=20, padx=10, sticky="e")
        self.spec_entry = tk.Entry(self, font=("微软雅黑", 12))
        self.spec_entry.grid(row=1, column=1, pady=20, padx=10)

        self.query_button = tk.Button(self, text="查询", command=self.query_orders, font=("微软雅黑", 12))
        self.query_button.grid(row=2, column=0, pady=20, padx=10)

        # 创建图表容器
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.figure.patch.set_facecolor('white')  # 设置图表背景色为白色
        self.figure.set_facecolor('white')  # 设置子图背景色为白色

        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=20, padx=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_rowconfigure(3, weight=0)

    def query_orders(self):
        material_name = self.material_entry.get()
        spec = self.spec_entry.get()

        # 根据查询条件从数据库中获取订单数据
        sql = f"""SELECT 时间戳, 订购数量, 价格
        From 客户辅料订单 WHERE 辅料名称 = '{material_name}' AND 辅料编号 = '{spec}'
        """
        self.app.db.execute(sql)

        # 假设获取的订单数据为以下格式的列表
        order_data = self.app.db.cursor.fetchall()
        print(order_data)

        # 统计数据
        order_dates = [data[0][:10] for data in order_data]
        order_quantities = [data[1] for data in order_data]
        order_prices = [float(data[2]) for data in order_data]

        # 清空图表
        self.figure.clear()

        # 创建子图
        ax1 = self.figure.add_subplot(2, 1, 1)
        ax2 = self.figure.add_subplot(2, 1, 2)

        # 绘制当日统计柱状图
        ax1.bar(order_dates, order_quantities)
        ax1.set_xlabel('date')
        ax1.set_ylabel('quantity')
        ax1.set_title('daily quantity')

        # 绘制当月统计折线图
        ax2.plot(order_dates, order_prices)
        ax2.set_xlabel('date')
        ax2.set_ylabel('money')
        ax2.set_title('daily money')

        # 更新图表
        self.canvas.draw()
