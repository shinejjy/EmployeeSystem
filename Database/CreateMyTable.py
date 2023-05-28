import pandas as pd
from Database.SQL import EasySql


# 创建外贸部客户档案表
def create_ForeignTradeCustomerRecordsTable(db):
    df = pd.read_excel(
        io='辅料销售涉及主要表格例/2模板202303.xlsx',
        header=None,
        sheet_name=0,
        usecols="A:AM",
        # index_col=0,
        skiprows=5,
        nrows=9,
        na_values=[]
    )
    df = df.fillna("null")

    # 定义表格名和字段类型字典
    table_name = "ForeignTradeCustomerRecordsTable"
    type_dic = {
        "Salesperson": "VARCHAR(255)",
        "Level": "VARCHAR(255)",
        "DevDate": "DATE",
        "CompanyName": "VARCHAR(255)",
        "Country": "VARCHAR(255)",
        "Media": "VARCHAR(255)",
        "ProductName": "VARCHAR(255)",
        "SpecCode": "VARCHAR(255)",
        "SpecCodeRemarks": "VARCHAR(255)",
        "Usage": "VARCHAR(255)",
        "FollowUp": "VARCHAR(255)",
        "CompanyNature": "VARCHAR(255)",
        "CompanyProfile": "VARCHAR(255)",
        "CustomerContact": "VARCHAR(255)",
        "CustomerEmail": "VARCHAR(255)",
        "CustomerPhone": "VARCHAR(255)",
        "CustomerWebsite": "VARCHAR(255)",
        "Negotiation": "DATE",
        "Sample": "DATE",
        "Questionnaire": "DATE",
        "Deal": "DATE",
        "SupplierAudit": "DATE",
        "EstAnnualUsage": "VARCHAR(255)",
        "CurrManufacturer": "VARCHAR(255)",
        "Grade": "VARCHAR(255)",
        "Model": "VARCHAR(255)",
        "PricePerKg": "VARCHAR(255)",
        "Jan2023": "DATE",
        "Feb2023": "DATE",
        "Mar2023": "DATE",
        "Apr2023": "DATE",
        "May2023": "DATE",
        "Jun2023": "DATE",
        "Jul2023": "DATE",
        "Aug2023": "DATE",
        "Sep2023": "DATE",
        "Oct2023": "DATE",
        "Nov2023": "DATE",
        "Dec2023": "DATE"
    }

    # 创建表格
    db.createTable(table_name, type_dic)

    for index, row in df.iterrows():
        db.insertData("ForeignTradeCustomerRecordsTable", row)


# 创建客户流水表
def create_CustomerRecordsTable(db):
    table_name = "CustomerRecordsTable"
    type_dic = {
        "SalesDepartment": "VARCHAR(255)",
        "Province": "VARCHAR(255)",
        "City": "VARCHAR(255)",
        "EnterpriseName": "VARCHAR(255)",
        "EnterpriseType": "VARCHAR(255)",
        "EnterpriseScale": "VARCHAR(255)",
        "CompanyAddress": "VARCHAR(255)",
        "CustomerName": "VARCHAR(255)",
        "Phone": "VARCHAR(255)",
        "Label": "VARCHAR(255)",
        "Department": "VARCHAR(255)",
        "Position": "VARCHAR(255)",
        "PositionLevel": "VARCHAR(255)",
        "IsSamplePurchase": "VARCHAR(255)",
        "ContactCloseness": "VARCHAR(255)",
        "ContactPerson": "VARCHAR(255)",
        "IsOverlap": "VARCHAR(255)",
        "ContactInfo": "VARCHAR(255)",
        "InitialContactTime": "DATE",
        "FirstPromotionalMaterialTime": "DATE",
        "SummerFanGift2021": "BIT",
        "InjectableBook2021": "BIT",
        "YearEndGift2021": "BIT",
        "SummerGift2022": "BIT",
        "Book2022": "BIT",
        "LargeCustomerGift2022": "BIT",
        "YearEndGift2022": "BIT",
        "PreviousEmployer": "VARCHAR(255)"
    }

    # 创建表格
    db.createTable(table_name, type_dic)


# 创建客户跟进表
def create_CustomerFlowUpTable(db):
    # 定义表格名和字段类型字典
    table_name = "CustomerFlowUpTable"
    type_dic = {
        "Recorder": "VARCHAR(255)",
        "ActiveOrPassive": "VARCHAR(255)",
        "CompanyName": "VARCHAR(255)",
        "CompanyCategory": "VARCHAR(255)",
        "CustomerName": "VARCHAR(255)",
        "CustomerCategory": "VARCHAR(255)",
        "ProductInquiry": "BIT",
        "PriceInquiry": "BIT",
        "SampleRequest": "BIT",
        "Purchase": "BIT",
        "ElectronicDataProvider": "BIT",
        "PrintedMaterialPreparation": "BIT",
        "SampleTracking": "BIT",
        "UsageConsultationOrProblemInquiry": "BIT",
        "ProductName": "VARCHAR(255)",
        "SpecificationCode": "VARCHAR(255)",
        "Weight": "VARCHAR(255)",
        "PreparationOrPreparationCategory": "VARCHAR(255)",
        "Problem": "VARCHAR(255)",
        "Resolved": "BIT",
        "Solution": "VARCHAR(255)"
    }

    # 创建表格
    db.createTable(table_name, type_dic)


# 创建研发客户档案表
def create_Customer_template(db):
    # 定义表名和字段名
    table_name = '研发客户档案表A首部'
    columns = {
        '销售部': 'VARCHAR(255)',
        '省份': 'VARCHAR(255)',
        '研发实力': 'VARCHAR(255)',
        '企业名称': 'VARCHAR(255)',
        '法人': 'VARCHAR(255)',
        '总经理': 'VARCHAR(255)',
        '许可证号': 'VARCHAR(255)',
        'ＧＭＰ证书': 'VARCHAR(255)',
        '企业性质': 'VARCHAR(255)',
        '研究范围': 'VARCHAR(255)',
        '药品': 'VARCHAR(255)',
        '经营规模': 'VARCHAR(255)',
        '员工人数': 'VARCHAR(255)',
        '其他描述': 'VARCHAR(255)'
    }
    primary_key = '企业名称'  # 设置主键为"企业名称"

    # 创建表格
    db.createTable(table_name, columns, primary_key)

    # 创建 "研发客户档案表客户信息" 表时添加外键约束
    type_dict = {
        "企业名称": "VARCHAR(255)",
        "姓名": "VARCHAR(255)",
        "手机": "VARCHAR(255)",
        "部门": "VARCHAR(255)",
        "职级评估_ABC": "VARCHAR(255)",
        "初始联系时间": "DATETIME",
        "地址": "VARCHAR(255)"
    }
    foreign_keys = {
        "企业名称": "研发客户档案表A首部(企业名称)"
    }
    db.createTable("研发客户档案表B客户信息", type_dict, foreign_keys=foreign_keys)

    # 创建 "研发客户档案表赠样记录" 表
    type_dict = {
        "企业名称": "VARCHAR(255)",
        "时间": "DATETIME",
        "产品": "VARCHAR(255)",
        "型号": "VARCHAR(255)",
        "数量_g": "FLOAT",
        "用途": "VARCHAR(255)",
        "进展": "VARCHAR(255)"
    }
    foreign_keys = {
        "企业名称": "研发客户档案表A首部(企业名称)"
    }
    db.createTable("研发客户档案表C赠样记录", type_dict, foreign_keys=foreign_keys)

    # 创建 "研发客户档案表销售数据" 表
    type_dict = {
        "企业名称": "VARCHAR(255)",
        "时间": "DATETIME",
        "产品": "VARCHAR(255)",
        "规格": "VARCHAR(255)",
        "单价_元": "FLOAT",
        "数量_kg": "FLOAT",
        "金额": "FLOAT",
        "用途": "VARCHAR(255)",
        "进展": "VARCHAR(255)"
    }
    foreign_keys = {
        "企业名称": "研发客户档案表A首部(企业名称)"
    }
    db.createTable("研发客户档案表D销售数据", type_dict, foreign_keys=foreign_keys)


# 创建授权书总表
def create_authorization_letter(db):
    # 定义表名和字段名及其数据类型
    table_name = "授权书总表"
    columns = {
        "开具月份": "VARCHAR(7)",
        "品种": "VARCHAR(255)",
        "登记号": "VARCHAR(255)",
        "登记号状态": "VARCHAR(255)",
        "关联制剂厂家": "VARCHAR(255)",
        "关联制剂名称": "VARCHAR(255)",
        "给药途径": "VARCHAR(255)",
        "跟进人": "VARCHAR(255)",
        "受审情况": "VARCHAR(255)",
        "受理月份": "VARCHAR(7)",
        "在审月份": "VARCHAR(7)",
        "在审消失月份": "VARCHAR(7)",
        "备注": "VARCHAR(255)"
    }

    # 创建表
    db.createTable(table_name, columns)


def create_development_schedule(db):
    # 创建 "客户开发进度表_客户情况" 表格
    type_dict = {
        "开发状态": "VARCHAR(255)",
        "序号": "INT",
        "企业名称": "VARCHAR(255)",
        "省份": "VARCHAR(255)",
        "城市": "VARCHAR(255)",
        "部门": "VARCHAR(255)",
        "具体部门": "VARCHAR(255)",
        "负责人": "VARCHAR(255)",
        "客户名称": "VARCHAR(255)",
        "客户来源": "VARCHAR(255)"
    }
    db.createTable("客户开发进度表_A客户情况", type_dict, primary_key=["开发状态信息", "序号"])

    # 创建 "客户开发进度表_项目情况" 表格
    type_dict = {
        "开发状态": "VARCHAR(255)",
        "序号": "INT",
        "产品_一品一项目": "VARCHAR(255)",
        "对应规格编码": "VARCHAR(255)",
        "特殊需求": "VARCHAR(255)",
        "现有供应商__预估年用量": "FLOAT",
        "现有供应商__现用厂家": "VARCHAR(255)",
        "现有供应商__级别": "VARCHAR(255)",
        "现有供应商__型号_如有": "VARCHAR(255)",
        "现有供应商__单价_kg": "FLOAT",
        "申样___销售": "FLOAT",
        "是否重复项目": "VARCHAR(255)",
        "初次报价": "FLOAT",
        "数量": "FLOAT",
        "单价": "FLOAT",
        "金额": "FLOAT",
        "制剂名称": "VARCHAR(255)",
        "是否一致性评价品种": "VARCHAR(255)",
        "辅料用途": "VARCHAR(255)",
        "处方用量": "FLOAT",
        "起始开发日期": "DATE",
        "客户重要程度": "VARCHAR(255)"
    }
    primary_key = ["开发状态", "序号"]
    db.createTable("客户开发进度表_B项目情况", type_dict, primary_key=primary_key)

    # 创建 "客户开发进度表_项目跟进" 表格
    type_dict = {
        "开发状态": "VARCHAR(255)",
        "序号": "INT",
        "辅料检验": "DATE",
        "处方筛选": "DATE",
        "初步验证工艺_小试": "DATE",
        "中试验证": "DATE",
        "工艺验证": "DATE",
        "临床": "DATE",
        "拿到批文": "DATE",
        "正常采购": "VARCHAR(255)",
        "是否回复": "BIT",
        "进行中": "VARCHAR(255)",
        "备注_现状简报": "VARCHAR(255)"
    }
    primary_key = ["开发状态", "序号"]
    db.createTable("客户开发进度表_C项目跟进", type_dict, primary_key=primary_key)

    # 创建 "客户开发进度表_授权书情况" 表格
    type_dict = {
        "开发状态": "VARCHAR(255)",
        "序号": "INT",
        "中试前": "VARCHAR(255)",
        "申报前": "VARCHAR(255)",
        "开具时间": "DATE"
    }
    primary_key = ["开发状态", "序号"]
    db.createTable("客户开发进度表_D授权书情况", type_dict, primary_key=primary_key)

    # 创建 "客户开发进度表_落地转移情况" 表格
    type_dict = {
        "开发状态": "VARCHAR(255)",
        "序号": "INT",
        "落地企业名称": "VARCHAR(255)",
        "联系人": "VARCHAR(255)",
        "移交销售经理": "VARCHAR(255)",
        "移交时间": "DATE"
    }
    primary_key = ["开发状态", "序号"]
    db.createTable("客户开发进度表_E落地转移情况", type_dict, primary_key=primary_key)

    # 创建 "客户开发进度表_进度描述" 表格
    type_dict = {
        "开发状态": "VARCHAR(255)",
        "序号": "INT",
    }
    for year in range(2022, 2024):
        for month in range(1, 13):
            field_name = f"进度{year}_{month}"
            field_type = "VARCHAR(255)"
            type_dict[field_name] = field_type
    primary_key = ["开发状态", "序号"]
    db.createTable("客户开发进度表_F进度描述", type_dict, primary_key=primary_key)


def create_ProblemFeedbackFlowMeter(db):
    type_dict = {
        "年份": "INT",
        "月份": "INT",
        "日期": "INT",
        "部门": "VARCHAR(255)",
        "产品": "VARCHAR(255)",
        "对应制剂": "VARCHAR(255)",
        "信息": "VARCHAR(255)",
        "解决进度_解决状态": "VARCHAR(255)",
        "对接部门__负责人": "VARCHAR(255)",
        "详情": "VARCHAR(255)"
    }

    db.createTable("产品问题反馈流水表", type_dict)


if __name__ == '__main__':
    db = EasySql()
    create_Customer_template(db)
    create_authorization_letter(db)
    create_development_schedule(db)
    create_ProblemFeedbackFlowMeter(db)
