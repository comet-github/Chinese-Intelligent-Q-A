import jieba
import re


# 汉语分词
def chinese_segmentation(text):
    seg_list = jieba.cut(text, cut_all=False)
    return " ".join(seg_list)


def is_all_chinese_without_punctuation_and_whitespace(s):
    # 使用正则表达式判断是否全是汉字且不包含标点符号或空格
    return bool(re.match(r'^[\u4e00-\u9fa5]+$', s))


# 使用method方法对chars进行times次筛选
def list_sift(chars, method, times):
    for i in range(times):
        for j in chars:
            if not method(j):
                chars.remove(j)
    return chars


def fenci(text):
    text = text
    seg_result = chinese_segmentation(text)
    lines = seg_result.split(" ")
    lines = list_sift(lines, is_all_chinese_without_punctuation_and_whitespace, 3)

    # 删除单个汉字和空
    single_chinese_chars = [char for char in lines if len(char) <= 1]
    for char in single_chinese_chars:
        lines.remove(char)

    return lines


if __name__ == '__main__':
    out = fenci("全流程做贷款变更、贷款开立时，提交时提示“关联贷款类型代码不匹配”；（注：关联贷款类型代码对应信贷资金管理方式）。" +
                "全流程做贷款变更、贷款开立时，提交时提示“关联贷款类型代码不匹配”；（注：关联贷款类型代码对应信贷资金管理方式）。")
    print(out)
