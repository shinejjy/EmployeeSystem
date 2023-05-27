from tkinter import *
from tkinter import ttk

main = Tk()
data = [(1, "小明", 23, '男', '2021-09-21'), (2, "小强", 23, '男', '2021-09-21'),
        (3, "小红", 23, '女', '2021-09-21'), (4, "铁头", 23, '男', '2021-09-21')]
tree = ttk.Treeview(main, columns=('id', 'name', 'age', 'sex', 'birth'), show="tree", displaycolumns="#all")
tree.heading("#0", text="学校", anchor=W)
tree.heading('id', text="编号", anchor=W)
tree.heading('name', text="姓名", anchor=W)
tree.heading('age', text="年龄", anchor=W)
tree.heading('sex', text="性别", anchor=W)
tree.heading('birth', text="出生日期", anchor=W)
stu_root = tree.insert("", END, text="学生")
man = tree.insert(stu_root, END, text="男")
wom = tree.insert(stu_root, END, text="女")
for itm in data:
    if itm[3] == "男":
        tree.insert(man, END, text=itm[1], values=itm)
    else:
        tree.insert(wom, END, text=itm[1], values=itm)
tree.pack(expand=1, fill=BOTH)
main.mainloop()
