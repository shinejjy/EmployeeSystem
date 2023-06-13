from tkinter import messagebox, ttk, simpledialog
import tkinter as tk

from Base.Base import EditableTreeview, BaseFrame, EditableTable
from Database.SQL import change_code


class NWCustomerPage(EditableTable):
    def __init__(self, app, window, show):
        table_names = [
            '8内贸部台账总表', '[8外贸部台账总表]'
        ]
        search_columns = ['业务员'] * 2
        p_primary_key_tbss = [[1, 40], [0, 44]]
        p_primary_key_dbss = [None] * 2
        primary_keyss = [['序号', '销售月份']] * 2
        super().__init__(app, window, show, search_columns, table_names, p_primary_key_dbss,
                         p_primary_key_tbss, primary_keyss, True)

    def add_customer(self):
        # 销毁修改框
        if self.tree.entry:
            self.tree.entry.destroy()

        # 弹出新页面，供员工选择开发状态
        status = self.get_development_status()
        if not status:
            # 员工取消选择，取消添加
            return

        # 获取当前最大的序号值
        sql = f"""SELECT MAX(序号)
         FROM [{self.table_info_current['table_name']}]
         WHERE 销售月份 = '{status}'
         """
        self.app.db.execute(sql)
        result = self.app.db.cursor.fetchone()
        max_index = result[0] if result[0] else 0

        # 生成新的序号值
        new_index = max_index + 1

        # 在表格末尾插入空白记录
        new_customer = [''] * len(self.tree['columns'])
        new_customer[self.tree['columns'].index('序号')] = new_index
        new_customer[self.tree['columns'].index('销售月份')] = status
        self.tree.insert("", tk.END, values=new_customer)

        # 在相应的表中插入新记录
        sql = f"INSERT INTO [{self.table_info_current['table_name']}] (序号, 销售月份) VALUES ({new_index}, '{status}')"
        self.app.db.execute(sql)

        # 更新页面和数据库
        self.show_customer_page()

    def get_development_status(self):
        status_options = ["2022.1月", "2022.2月"]

        status_var = tk.StringVar()
        status_var.set(status_options[0])

        dialog = tk.Toplevel(self.tree)
        dialog.title("填写销售月份")
        dialog.geometry("200x100")
        dialog.transient(self.tree)
        dialog.grab_set()

        label = tk.Label(dialog, text="请填写销售月份：")
        label.pack()

        combobox = ttk.Combobox(dialog, textvariable=status_var, values=status_options, state="readonly")
        combobox.pack()

        def confirm():
            selected_status = status_var.get()
            if selected_status in status_options:
                dialog.destroy()
                return selected_status
            else:
                messagebox.showerror("错误", "无效的销售月份！")
                return None

        confirm_button = tk.Button(dialog, text="确认", command=confirm)
        confirm_button.pack()

        dialog.wait_window()

        return status_var.get()

    def delete_customer(self):
        # 销毁修改框
        if self.tree.entry:
            self.tree.entry.destroy()
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的客户")
            return

        confirm = messagebox.askyesno("确认", "确定要删除选中的客户吗？")
        if confirm:
            for item in selected_items:
                # 获取选中行的数据
                values = [self.tree.item(item)['values'][self.tree['columns'].index('序号')],
                          self.tree.item(item)['values'][self.tree['columns'].index('销售月份')]]
                condition = " AND ".join([f"{primary_key} = '{primary_key_value}'"
                                          for primary_key, primary_key_value in zip(['序号', '销售月份'], values)])

                # 在数据库中执行删除操作
                sql = f"DELETE FROM [{self.table_info_current['table_name']}] WHERE {condition}"
                self.app.db.execute(sql)

                # 从表格中删除对应行
                self.tree.delete(item)

            messagebox.showinfo("提示", "客户删除成功")
