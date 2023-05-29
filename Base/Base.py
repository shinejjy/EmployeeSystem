import tkinter as tk
from tkinter import ttk


class BaseFrame(tk.Frame):
    def __init__(self, app, window, show=True, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.app = app
        self.window = window
        self.configure(bg="white")
        if not show:
            self.hide()

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()


class EditableTreeview(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Double-1>', self.edit_cell)
        self.entry = None
        self.entry_index = None

    def edit_cell(self, event):
        # 获取双击的单元格位置
        cell = self.identify('item', event.x, event.y)
        column = self.identify('column', event.x, event.y)
        if cell and column:
            value = self.item(cell)['values'][int(column[1:]) - 1]
            # 创建编辑框并定位到双击的单元格
            self.edit_entry(cell, column, value)

    def edit_entry(self, cell, column, value):
        # 如果已存在编辑框，先销毁
        if self.entry:
            self.entry.destroy()

        # 获取列的宽度
        column_width = self.column(column)["width"]

        # 创建编辑框并定位
        x, y, _, _ = self.bbox(cell, column)
        entry_text = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=entry_text)
        entry_text.set(value)
        self.entry.place(x=x, y=y, width=column_width)
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda event: self.save_entry(cell, column))
        self.entry.bind('<Escape>', lambda event: self.cancel_edit())

        # 记录编辑的单元格位置
        self.entry_index = (cell, column)

    def save_entry(self, cell, column):
        value = self.entry.get()
        self.set(cell, column, value)

        # 在这里添加将修改保存到数据库的逻辑
        # 根据cell和column获取对应的数据，并将修改的值保存到数据库

        self.entry.destroy()
        self.entry = None
        self.entry_index = None

    def cancel_edit(self):
        if self.entry:
            self.entry.destroy()
            self.entry = None
            self.entry_index = None

