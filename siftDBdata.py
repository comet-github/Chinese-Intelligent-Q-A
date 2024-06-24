import mysql.connector
from fenci1 import fenci
from databaseConnect import connect_db, close_db


def count_matched_item(main_list, tips_list):
    matched_set = set(main_list) & set(tips_list)
    # print("matched_set:", matched_set)
    num = 0
    return sum(tips_list.count(item) for item in matched_set)


def match_filter(main_list, list3, topNo=3, maxNum=5):
    matched_counts = [count_matched_item(main_list, lst[1]) for lst in list3]
    sorted_counts = [x for x in matched_counts if x != 0]  # 去除匹配数量0
    sorted_counts = sorted(list(set(sorted_counts)), reverse=True)  # 匹配数量去重排序
    ord_list = []
    print('匹配数量：', matched_counts)
    print('匹配数量排序：', sorted_counts)

    topNo = min(topNo, len(sorted_counts))

    if maxNum <= 0:  # 返回所有匹配的项
        for num in range(topNo):  # 选出匹配数量前topNo的项的序号
            indices = [index for index, element in enumerate(matched_counts) if element == sorted_counts[num]]
            ord_list = ord_list + indices
        return ord_list
    else:  # 返回最匹配的maxNum项
        for num in range(topNo):  # 选出匹配数量前topNo的项的序号
            # 控制选出的序号数量
            if len(ord_list) > maxNum:
                break
            indices = [index for index, element in enumerate(matched_counts) if element == sorted_counts[num]]
            ord_list = ord_list + indices
        # 控制选出的序号数量
        if len(ord_list) > maxNum:
            ord_list = ord_list[:maxNum]
        return ord_list


def return_answer(db, cursor, faqTable, fenciTable, question, topNo=3, maxNum=5):
    mydb, mycursor = db, cursor
    ATable = faqTable
    FTable = fenciTable
    question = question
    topNo, maxNum = topNo, maxNum
    # 执行查询
    mycursor.execute("SELECT * FROM {};".format(FTable))

    # 获取所有数据
    data = mycursor.fetchall()
    # print(type(data))
    # print(data)

    # 处理数据
    result = []
    for row in data:
        result.append([row[0], [part.strip() for part in row[1].split(',')]])

    tip_que = fenci(question)
    print('“{}”的分词是：'.format(question), tip_que)
    ordnum = match_filter(tip_que, result, topNo, maxNum)
    print('ordnum', ordnum)

    all_data_list = []

    if len(ordnum) < 1:
        return all_data_list
    elif len(ordnum) == 1:
        query_sql = "select ordnum,question,solution,maintenance from {} where ordnum={};".format(ATable, ordnum[0])
    elif len(ordnum) > 1:
        query_sql = "select ordnum,question,solution,maintenance from {} where ordnum in {} " \
                    "order by field({});".format(ATable, tuple(ordnum), 'ordnum,'+','.join(str(item) for item in ordnum))
    print('匹配的序号个数：', len(ordnum))
    print(query_sql)

    mycursor.execute(query_sql)
    # print(cursor.fetchall(),type(cursor.fetchall()))

    # 遍历查询结果，为每条数据创建一个单独的列表
    for row in mycursor.fetchall():
        data_list = list(row)  # 将结果转为列表格式
        all_data_list.append(data_list)

    print("all_data_list:", all_data_list)

    return all_data_list


if __name__ == '__main__':
    mydb, mycursor = connect_db(host="localhost", user="root", pw="mysql1234+", dbName="faqlist")
    question = '支付'
    answer_list = return_answer(mydb, mycursor, 'faqtab1', 'tab1fenci', question, maxNum=5)
    # print(answer_list[0])
    for i in range(len(answer_list)):
        print('第{}个：'.format(i + 1))
        for j in answer_list[i]:
            print(j)
    close_db(mydb, mycursor)
