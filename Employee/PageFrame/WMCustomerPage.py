from Base.Base import EditableTable


class WMCustomerPage(EditableTable):
    def __init__(self, app, window, show):
        super().__init__(app, window, show, '业务员', '2外贸部客户档案表', 0, '序号')
