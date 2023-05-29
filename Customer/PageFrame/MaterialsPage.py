import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Base.Base import BaseFrame
from Database.SQL import change_code
import qrcode
from PIL import ImageTk, Image
import time


class MaterialsPage(BaseFrame):
    def __init__(self, app, window, show):
        super().__init__(app, window, show)

        # 创建查询表的滚动条
        scrollbar1 = ttk.Scrollbar(self)
        scrollbar1.grid(row=0, column=1, sticky=tk.N + tk.S)

        # 创建查询表格
        columns1 = ("辅料编号", "辅料名称", "辅料单价", "点击选购吧！")
        self.searchTree = ttk.Treeview(self, columns=columns1, show="headings", yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=self.searchTree.yview)
        # 设置查询表格的表头
        for col in columns1:
            self.searchTree.heading(col, text=col)
            self.searchTree.column(col, width=125)
        self.searchTree.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # 创建订购表的滚动条
        scrollbar2 = ttk.Scrollbar(self)
        scrollbar2.grid(row=1, column=1, sticky=tk.N + tk.S)

        # 创建订购表格
        columns2 = ("辅料编号", "辅料名称", "辅料单价", "选购数量", "价格")
        self.purchaseTree = ttk.Treeview(self, columns=columns2, show="headings", yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=self.purchaseTree.yview)
        # 设置订购表格的表头
        for col in columns2:
            self.purchaseTree.heading(col, text=col)
            self.purchaseTree.column(col, width=100)
        self.purchaseTree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # 创建总价显示
        self.priceLabel = tk.Label(self, text="总和：0.0元", background='white', font=("Arial", 20))
        self.priceLabel.grid(row=2, column=0, sticky=tk.E)

        # 创建支付按钮
        self.payButton = tk.Button(self, text="支付", font=("Arial", 20), bg="blue", fg="white",
                                   command=self.open_payment_window)

        self.payButton.grid(row=3, column=0, sticky=tk.E)

        # 设置行列权重和填充
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.show_materials_page()

        self.purchase_window_open = False

    def show_materials_page(self):
        # 清空表格内容
        self.searchTree.delete(*self.searchTree.get_children())

        # 查询可订购辅料的详细情况
        sql = "SELECT PNO, PNA, PPR FROM MedicinalIngredients"
        self.app.db.execute(sql)
        materials = self.app.db.cursor.fetchall()

        # 将辅料信息插入表格中
        for material in materials:
            material = change_code(material)
            pno, pna, ppr = material
            item_id = self.searchTree.insert("", tk.END, values=(pno, pna, ppr, "[选购]",))

            # 为选购按钮绑定点击事件处理函数
            self.searchTree.set(item_id, "#4")  # 存储辅料编号

        # 绑定选购按钮的点击事件
        self.searchTree.bind("<Button-1>", self.select_material)

    def select_material(self, event):
        item = self.searchTree.identify_row(event.y)
        column = self.searchTree.identify_column(event.x)
        if item and column == "#4":
            pno = self.searchTree.set(item, "#1")
            pna = self.searchTree.set(item, "#2")
            ppr = self.searchTree.set(item, "#3")
            self.open_purchase_window(pno, pna, ppr)

    def open_purchase_window(self, pno, pna, ppr):
        if self.purchase_window_open:
            return  # 如果窗口已经打开，则不再创建新窗口

        purchase_window = tk.Toplevel(self.window)
        purchase_window.title("选购辅料")
        purchase_window.geometry("200x150")

        # 创建选购窗口的控件，包括回显框、增加和减少按钮、确认按钮等
        quantity = tk.IntVar()
        quantity.set(1)  # 默认数量为1

        text_label = f"辅料编号\t辅料名称\t单价（元/g）\n{pno}\t{pna}\t{ppr}\n选购数量:"
        label = tk.Label(purchase_window, text=text_label)
        label.pack()

        entry = tk.Entry(purchase_window, textvariable=quantity)
        entry.pack()

        def increase_quantity():
            # 增加辅料数量
            quantity.set(quantity.get() + 1)

        def decrease_quantity():
            # 减少辅料数量
            if quantity.get() > 1:
                quantity.set(quantity.get() - 1)

        def confirm_purchase():
            # 计算选购辅料的总价格
            total_price = float(ppr) * float(quantity.get())

            self.purchase_window_open = False
            # 销毁选购窗口
            purchase_window.destroy()

            # 更新已选购辅料表格
            purchase_list = [pno, pna, ppr, quantity.get(), total_price]
            self.update_purchaseTree(purchase_list)

            # 更新总价Label的文本
            self.update_total_price()

        def on_purchase_window_close():
            self.purchase_window_open = False
            purchase_window.destroy()

        increase_button = tk.Button(purchase_window, text="+", command=increase_quantity)
        increase_button.pack(side=tk.LEFT)

        decrease_button = tk.Button(purchase_window, text="-", command=decrease_quantity)
        decrease_button.pack(side=tk.LEFT)

        confirm_button = tk.Button(purchase_window, text="确认", command=confirm_purchase)
        confirm_button.pack()

        purchase_window.protocol("WM_DELETE_WINDOW", on_purchase_window_close)

        self.purchase_window_open = True

    def update_purchaseTree(self, purchase_list):
        if purchase_list:
            self.purchaseTree.insert("", tk.END, values=purchase_list)

    def update_total_price(self):
        total_price = 0.0
        for child in self.purchaseTree.get_children():
            total_price += float(self.purchaseTree.set(child, "#5"))

        self.priceLabel["text"] = f"总和：{total_price}元"

    def open_payment_window(self):
        payment_window = tk.Toplevel(self.window)
        payment_window.title("支付")
        payment_window.geometry("400x400")

        total_price = 0.0
        for child in self.purchaseTree.get_children():
            total_price += float(self.purchaseTree.set(child, "#5"))

        # 显示总价
        total_price_label = tk.Label(payment_window, text=f"总价：{total_price}元")
        total_price_label.pack()

        # 生成二维码图像
        qr_code = qrcode.make(str(total_price))
        qr_code_image = ImageTk.PhotoImage(qr_code)

        # 显示二维码图像
        qr_code_label = tk.Label(payment_window, image=qr_code_image)
        qr_code_label.image = qr_code_image  # 保持引用，防止图像被垃圾回收
        qr_code_label.pack()

        def scan_qr_code():
            # 模拟扫码操作，这里假设扫描的结果为total_price的字符串形式
            scanned_result = str(total_price)

            # 检查扫描结果与总价的匹配
            if scanned_result == str(total_price):
                if scanned_result == "0.0":
                    result_label.config(text="您未选购任何商品！")
                    return
                result_label.config(text="支付成功")

                order_info = {
                    "timestamp": time.time(),
                    "total_price": total_price,
                    "purchase_list": self.get_purchase_list()
                }
                self.window.order_list.append(order_info)

                print(self.window.order_list)

                self.purchaseTree.delete(*self.purchaseTree.get_children())
                self.priceLabel.configure(text="总价：0.0元")
                payment_window.destroy()
            else:
                result_label.config(text="支付失败")

        # 添加扫码按钮和回显标签
        scan_button = tk.Button(payment_window, text="扫码", command=scan_qr_code)
        scan_button.pack()
        result_label = tk.Label(payment_window, text="")
        result_label.pack()

        payment_window.mainloop()

    def get_purchase_list(self):
        purchase_list = []
        for child in self.purchaseTree.get_children():
            pno = self.purchaseTree.set(child, "#1")
            pna = self.purchaseTree.set(child, "#2")
            ppr = self.purchaseTree.set(child, "#3")
            quantity = self.purchaseTree.set(child, "#4")
            total_price = self.purchaseTree.set(child, "#5")
            purchase_item = [pno, pna, ppr, quantity, total_price]
            purchase_list.append(purchase_item)
        return purchase_list
