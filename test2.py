import tkinter as tk
from tkinter import ttk
from tkinter.font import Font


def auto_adjust_width(treeview):
    # 获取所有列
    columns = treeview["columns"]

    # 遍历每一列
    for column in columns:
        # 设置列宽为列标题的宽度
        treeview.column(column, width=Font().measure(column))

        for item in treeview.get_children():
            print(treeview.bbox(item, column).keys)

        max_width = max(
            treeview.column(column)["width"]
            for item in treeview.get_children()
        )

        # 更新列宽度
        treeview.column(column, width=max_width)

def auto_adjust_height(treeview):
    # 获取所有列
    columns = treeview["columns"]

    # 获取最高的单元格内容高度
    max_height = max(
        treeview.bbox(item, column)["height"]
        for item in treeview.get_children()
        for column in columns
    )

    # 设置每一行的高度为最高单元格内容高度
    treeview.configure(height=max_height + 2)

# 创建一个示例窗口
root = tk.Tk()

# 创建一个Treeview对象
treeview = ttk.Treeview(root)

# 添加列和设置标题
treeview["columns"] = ("column1", "column2", "column3")
treeview.heading("column1", text="Column 1")
treeview.heading("column2", text="Column 2")
treeview.heading("column3", text="Column 3")

# 添加示例数据
for i in range(10):
    treeview.insert("", "end", text="Item {}".format(i), values=("Value 1", "Value 2", "Value 3"))

# 自动调节列宽和列高
auto_adjust_width(treeview)
auto_adjust_height(treeview)

# 显示Treeview
treeview.pack()

# 进入主循环
root.mainloop()
