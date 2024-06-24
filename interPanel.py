import tkinter as tk
from databaseConnect import connect_db, close_db
from siftDBdata import return_answer


def get_question(textfield):
    question_entry = textfield
    question = question_entry.get("1.0", tk.END).replace("\n", "")
    print("查询问题:", type(question), question)
    return question


def clear_table(frame):
    table_frame = frame
    for widget in table_frame.winfo_children():
        widget.destroy()


def show_column_names(frame, widthDic):
    table_frame = frame
    column_width = widthDic
    clear_table(table_frame)
    for i, column_name in enumerate(["序号", "问题", "解决方案", "维护人"]):
        label = tk.Label(table_frame, text=column_name, borderwidth=1, relief="solid", font=("Arial", 10))
        label.grid(row=1, column=i, sticky="nsew")
        label.configure(bg="#FFD700", fg="#333333")  # 调整背景色和前景色
        table_frame.columnconfigure(i, minsize=column_width[column_name])

# 得到的数据全部显示
# def show_data(frame, widthDic, data_list):
#     table_frame = frame
#     column_width = widthDic
#     data_list = data_list
#     if len(data_list) == 0:
#         data_list = [['-1', '无对应数据', '无对应数据', '无对应数据']]
#     # print('data_list:', data_list)
#     for idx, sublist in enumerate(data_list):
#         for i, item in enumerate(sublist):
#             label = tk.Label(table_frame, text=item, borderwidth=1, relief="solid", font=("Arial", 10),
#                              wraplength=column_width[list(column_width.keys())[i]])
#             label.grid(row=idx + 2, column=i, sticky="nsew")
#             label.configure(bg="#FFFFFF", fg="#333333")  # 调整背景色和前景色

def show_data(frame, widthDic, data_list):
    table_frame = frame
    column_width = widthDic
    data_list = data_list or [['-1', '无对应数据', '无对应数据', '无对应数据']]  # 如果没有提供数据列表，则使用默认列表

    for idx, sublist in enumerate(data_list):
        row_data = []  # 用于存储当前行的数据片段
        # print("sublist:", sublist)
        for i, item in enumerate(sublist):
            # print("item:", item)
            if not isinstance(item, str):
                item = str(item)
            # 从 column_width 字典中获取相应列的宽度值
            col_width = column_width[i] if i in column_width else None  # 默认宽度值（如果没有特定设置）需要被设定为一个合适的默认值
            if col_width is None:  # 没有设置宽度的默认处理逻辑
                col_width = 15
            # 使用字符串格式化确保文本在指定宽度内显示并以省略号结尾
            truncated_item = item if len(item) <= col_width else item[:col_width] + "…"  # 注意这里的引号要和Python语法一致（使用了半角字符）
            row_data.append(truncated_item)  # 将截断后的数据添加到当前行的数据片段列表
            label = tk.Label(table_frame, text=truncated_item, borderwidth=1, relief="solid", font=("Arial", 10))  # 不再设置 wraplength 参数，因为我们控制了文本长度
            label.grid(row=idx + 2, column=i, sticky="nsew")  # 将标签放置在表格中
            label.configure(bg="#FFFFFF", fg="#333333", anchor="w")  # 设置背景色和前景色，并将文本左对齐
        # 如果一行内的数据片段数量不足，用空字符串填充剩余列（这部分代码看起来是正确的）
        for j in range(len(column_width), len(row_data)):  # 确保每一行的列数相同，不足的用空字符串填充
            row_data.append('')
        sublist[:] = row_data  # 更新原始子列表的内容，确保每一行都是完整的列表片段组合成的列表（包括可能的空字符串填充）


def init_main_window(title, minwidth, minheight):
    column_width = {"序号": 50, "问题": 250, "解决方案": 300, "维护人": 80}
    # 创建主窗口
    root = tk.Tk()
    root.title(title)
    # 设置窗口的最小尺寸（宽度x高度）为 720x540
    root.minsize(width=minwidth, height=minheight)
    root.geometry("800x600")
    root.configure(bg="#F5F5F5")  # 设置窗口背景色

    # 创建问题输入文本框
    question_entry = tk.Text(root, wrap="word", height=5, font=("Arial", 10), bg="#FFFFFF", fg="#000000",
                             insertbackground="#333333")
    question_entry.pack(pady=20)

    # 创建按钮框架
    button_frame = tk.Frame(root, bg="#F5F5F5")
    button_frame.pack()

    def query():
        nonlocal table_frame, question_entry, column_width
        question = get_question(question_entry)
        answer_list = return_answer(mydb, mycursor, 'faqtab1', 'tab1fenci', question, maxNum=5)
        if len(answer_list) == 0:
            answer_list = [['-1', '无对应数据', '无对应数据', '无对应数据']]
        show_column_names(table_frame, column_width)
        show_data(table_frame, column_width, answer_list)
        print("question:", question)
        print("answer_list:", answer_list)
        # print('table_frame:', type(table_frame))
        # print('canvas:', type(table_frame_scroll))

    def reset():
        nonlocal table_frame, column_width
        question_entry.delete('1.0', 'end')
        clear_table(table_frame)
        show_column_names(table_frame, column_width)

    # 创建查询按钮
    query_button = tk.Button(button_frame, text="查询", command=query, font=("Arial", 11),
                             bg="#228B22", fg="#000000", width=8, height=1)
    query_button.pack(side=tk.LEFT, padx=10, pady=10)

    # 创建重置按钮
    reset_button = tk.Button(button_frame, text="重置", command=reset,
                             font=("Arial", 11), bg="#A9A9A9", fg="#000000", width=8, height=1)
    reset_button.pack(side=tk.LEFT, padx=10, pady=10)

    # 创建表格框架
    table_frame = tk.Frame(root, bg="#FFFFFF")
    table_frame.pack(pady=20)

    # 创建表格列名
    show_column_names(table_frame, column_width)

    return root


if __name__ == '__main__':
    mydb, mycursor = connect_db(host="localhost", user="root", pw="mysql1234+", dbName="faqlist")
    root = init_main_window("问题查询解答", 720, 540)
    # 运行窗口
    root.mainloop()
    close_db(mydb, mycursor)
