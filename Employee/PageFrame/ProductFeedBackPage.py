from Base.Base import EditableTable


class ProductFeedBackPage(EditableTable):
    def __init__(self, app, window, show):
        super(ProductFeedBackPage, self).__init__(app, window, show, [None], ['7产品问题反馈流水表'], [-1], [0], ['产品问题质量编码'])
