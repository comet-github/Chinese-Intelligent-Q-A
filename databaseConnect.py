import pandas as pd
import mysql.connector
from fenci1 import fenci
from excelprocess import fenci_allExcelData


def connect_db(host, user, pw, dbName):
    # 建立 MySQL 数据库连接
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=pw,
        database=dbName
    )
    cursor = db.cursor()
    return db, cursor


def close_db(db, cursor):
    mydb, mycursor = db, cursor
    # 关闭数据库连接
    mycursor.close()
    mydb.close()
    print('数据库已断开')


def init_db_table_forExcel(tableName, db, cursor):
    # 创建数据表
    table_name = tableName
    db, cursor = db, cursor
    create_table_query = \
        """
    create table if not exists {}
    (
    ordnum int primary key,
    question text not null,
    solution text not null,
    field varchar(50),
    intersystem varchar(50),
    maintenance varchar(50),
    cue varchar(50),
    note varchar(100),
    mark varchar(20)
    );
    """.format(table_name)
    cursor.execute(create_table_query)

    # 清空指定表中的数据
    truncate_query = "TRUNCATE TABLE {}".format(table_name)
    cursor.execute(truncate_query)
    db.commit()
    print('已创建数据库”{}“及其下数据库表”{}“'.format(db.database, table_name))


def init_db_table_forList(tableName, db, cursor):
    # 创建数据表
    table_name = tableName
    db, cursor = db, cursor
    create_table_query = \
        """
    create table if not exists {}
    (
    ordnum int primary key,
    tips text not null
    );
    """.format(table_name)
    cursor.execute(create_table_query)

    # 清空指定表中的数据
    truncate_query = "TRUNCATE TABLE {}".format(table_name)
    cursor.execute(truncate_query)
    db.commit()
    print('已创建数据库”{}“及其下数据库表”{}“'.format(db.database, table_name))
    return "ordnum,tips"


# columns = "ordnum,question,solution,field,intersystem,maintenance,cue,note,mark"


# print(df.columns)
# print(", ".join(df.columns))

def excel2DB(excelName, sheetName, tableName, db, cursor):
    # 读取 Excel 文件
    df = pd.read_excel(excelName, sheet_name=sheetName)
    # 逐行读取数据并插入到MySQL数据表中
    for i, row in df.iterrows():
        values = []
        for val in row:
            if pd.isnull(val):  # 处理空数据
                values.append("NULL")
            else:
                if isinstance(val, str):
                    # 将包含单双引号的数据处理为转义形式
                    values.append("'" + str(val).replace("'", "''") + "'")
                else:
                    values.append(str(val))

        # print(type(values),values)
        # break
        insert_query = "INSERT INTO {} ({}) VALUES ({});".format(tableName, ", ".join(df.columns), ", ".join(values))
        cursor.execute(insert_query)
    db.commit()
    print('"{}"中"{}"的数据已成功导入到"{}.{}"数据库表中'.format(excelName, sheetName, db.database, tableName))


def list3toDB(dataList, tableName, db, cursor, columns):
    tableName = tableName
    columns = columns
    insert_query = "INSERT INTO {} ({}) VALUES (%s, %s)".format(tableName, columns)
    print("insert_query:", insert_query)
    for sublist in dataList:
        print("sublist:", sublist)
        cursor.execute(insert_query, (sublist[0][0], ', '.join(sublist[1])))
        db.commit()

    print('数据已成功导入到 "{}"."{}" 数据库表中'.format(db.database, tableName))


def load_excel_to_db(db, cursor, tabName, excelName, sheetName):
    mydb, mycursor = db, cursor
    tableName = tabName
    excelName = excelName
    sheetName = sheetName
    init_db_table_forExcel(tableName, mydb, mycursor)
    excel2DB(excelName, sheetName, tableName, mydb, mycursor)


def load_list_to_db(db, cursor, tabName, dataList):
    mydb, mycursor = db, cursor
    tableName = tabName
    columns = init_db_table_forList(tableName, mydb, mycursor)
    list3toDB(dataList, tableName, mydb, mycursor, columns)


if __name__ == '__main__':
    mydb, mycursor = connect_db(host="localhost", user="root", pw="mysql1234+", dbName="faqlist")
    load_excel_to_db(db=mydb, cursor=mycursor, tabName='faqtab1', excelName='List of FAQ 20220711.xlsx',
                     sheetName='Sheet2')
    dataList = fenci_allExcelData('List of FAQ 20220711.xlsx', 'Sheet2', fenci)
    print(dataList)
    load_list_to_db(db=mydb, cursor=mycursor, tabName='tab1fenci', dataList=dataList)
    close_db(mydb, mycursor)
