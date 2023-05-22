from frame import easy_sql as es

db = es.EasySql()

table_name = '牛逼'
type_dic = {'姓名': 'VARCHAR(255)',
            'id': 'VARCHAR(255)'}

db.creatTable(table_name, type_dic)

variable_list = ["'5555'", "null"]

db.insertTable(table_name, variable_list)

