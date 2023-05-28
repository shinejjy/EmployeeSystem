import pandas as pd
from Database.SQL import EasySql


def create_ForeignTradeCustomerRecordsTable(db):
    df = pd.read_excel(
        io='辅料销售涉及主要表格例/2外贸部客户档案表模板202303.xlsx',
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


if __name__ == '__main__':
    db = EasySql()
    create_CustomerFlowUpTable(db)
