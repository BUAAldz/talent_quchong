# -*- coding:utf-8 -*-
import pymongo
import json
import hashlib
import codecs

#*******************数据库配置***************************
user = "ldz"  # 数据库用户名
password = "ldz"  # 数据库密码
host = "192.168.171.193"  # 服务器外网地址
uri = "mongodb://%s:%s@%s:27017" % ("ldz", "ldz", "192.168.171.193")
# uri = "mongodb://127.0.0.1:27017"  # mongo服务器
DBNAME = "expert_db_v3"  # 库名
DBNAME2 = "expert_db_test"  # 库名
# ****************链接数据库****************************
client = pymongo.MongoClient(uri)  # mongo服务器
db = client[DBNAME]  # 库名
db2 = client[DBNAME2]  # 库名

# 原数据库
expert = db["expert_tongyi"]#所有的人的基本信息
paper = db["expert_paper_tongyi"]#
patent = db["expert_patent_tongyi"]
project = db["expert_project_tongyi"]
award = db["expert_award_tongyi"]
book = db["expert_book_tongyi"]
edu = db["expert_edu_tongyi"]
work = db["expert_work_tongyi"]
news = db['expert_news_tongyi']
tags = db['expert_tags_tongyi']
evaluate = db['expert_evaluate_tongyi']

#new 数据库·
big_table = db2["expert_big_table"]#存储同名人的大表信息
big_table_v2 = db2["expert_big_table_v2"]#存储已去重的人的大表信息
new_paper = db2["expert_paper"]
new_patent = db2["expert_patent"]
new_project = db2["expert_project"]
new_award = db2["expert_award"]
new_book = db2["expert_book"]
new_edu = db2["expert_edu"]
new_work = db2["expert_work"]
new_news = db2['expert_news']
new_tags = db2['expert_tags']
new_evaluate = db2['expert_evaluate']


#存储json文件
def save_json(file_name, save_list):
    with open(file_name, "w", encoding="utf-8")as f:
        json.dump(save_list, f, indent=1, ensure_ascii=False)

#取json文件
def open_json(file_name):
    with open(file_name, "r", encoding="utf-8")as f:
        load_json = json.load(f)
    return load_json


# 从字典里取数据，加以判断，若为其他情况 返回“空”
def get_data(dict_t, dict_key):
    if dict_key in dict_t.keys():
        if dict_t[dict_key] != None and dict_t[dict_key] != "":
            return str(dict_t[dict_key])
        else:
            return "空"


# 从字典里取数据， 加以判断，若为其他情况 返回"",主要用于两属性相加，
def get_data2(dict_t, dict_key):
    if dict_key in dict_t.keys():
        if dict_t[dict_key] != None and dict_t[dict_key] != "":
            return str(dict_t[dict_key])
        else:
            return ""
    else:
        return ""


# 判断该行字段串是否包含中文字符
def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


# 判断这个论文题目是否在当前论文列表里
def is_exist(list1, title):
    """

    :param list1: 论文列表
    :param title:  论文题目
    :return:
    """
    for line in list1:
        if is_contain_chinese(title):

            if line["titleCn"] != None and line["titleCn"] != "":
                if title in line["titleCn"] or line["titleCn"] in title:
                    return True
                else:
                    continue
            elif line["titleEn"] != None and line["titleEn"] != "":
                if title in line["titleEn"] or line["titleEn"] in title:
                    return True
                else:
                    continue
            else:
                continue

        else:
            if line["titleEn"] != None and line["titleEn"] != "":
                if title in line["titleEn"] or line["titleEn"] in title:
                    return True
                else:
                    continue
            elif line["titleCn"] != None and line["titleCn"] != "":
                if title in line["titleCn"] or line["titleCn"] in title:
                    return True
                else:
                    continue
    return False

# 判断这个项目和专利题目是否在当前论文列表里
def is_exist1(list1, title):
    """

    :param list1: 论文列表
    :param title:  论文题目
    :return:
    """
    for line in list1:
        # print("4")
        # print(line["title"])
        if line["title"] != None and line["title"] != "":
            if title in line["title"] or line["title"] in title:
                # print("8")
                return True
            else:
                # print("5")
                continue
        else:
            # print("6")
            continue

    return False


# 判断两个成果列表是否有重合的
def is_pruduct_exit(list1, list2):
    """
    :param list1: 成果列表1
    :param list2: 成果列表2
    :return: 重合 True 不重合 False
    """

    for line2 in list2:
        if "titleCn" in line2.keys() and "titleEn" in line2.keys():
            # print("1")
            # print("1")
            if line2["titleCn"] != None and line2["titleCn"] != "":
                # print("2")
                if is_exist(list1, line2["titleCn"]):
                    # print("4")
                    print(line2["titleCn"])
                    return True

            if line2["titleEn"] != None and line2["titleEn"] != "":
                # print("3")
                if is_exist(list1, line2["titleEn"]):
                    # print("5")
                    print(line2["titleEn"])

                    return True

        else:
            # print("2")
            if line2["title"] != None and line2["title"] != "":
                # print("3")
                if is_exist1(list1, line2["title"]):

                    return True
                else:
                    # print("7")
                    continue
    return False


# 两个值相加
def none_add(value1, value2):
    if isinstance(value1, list) and isinstance(value2, list):
        temp = []
        temp = value1 + value2
        return temp

    if value1 == "":
        value1 = None
    if value2 == "":
        value2 = None
    if value1 == None and value2 == None:
        return None
    if value1 == None and value2 != None:
        return value2
    if value1 != None and value2 == None:
        return value1
    if value1 != None and value2 != None:
        return value1 + value2

#得到成果里的时间
def get_pruduct_date(date1, date2):
    if date1 != None and date2 != None and date1 != "" and date2 != "":
        date1 = str(date1)
        date2 = str(date2)
        if len(date1) >= 4 and len(date2) >= 4:
            date1 = "".join(list(date1)[:4])
            date2 = "".join(list(date2)[:4])
            if date1 > date2:
                return 1  # date1 为标准
            else:
                return 2  # date2 为标准
        else:
            return 3  # 相加
    else:
        return 3  # 相加


# 融合过程中的原子操作
def merge_atom_process(new_dict, cur_dict, dict_key):
    """

    :param new_dict:  蓝本字典
    :param cur_dict: 当前字典
    :param dict_key:  当前的字典key值
    :return:
    """
    # 单空
    if dict_key != "flag":
        if new_dict[dict_key] == None or new_dict[dict_key] == "":
            new_dict[dict_key] = none_add(new_dict[dict_key], cur_dict[dict_key])
        # 双非空
        elif new_dict[dict_key] != None and new_dict[dict_key] != "" and cur_dict[dict_key] != None and cur_dict[
            dict_key] != "":
            # print(cur_dict.keys())
            # print(new_dict.keys())

            if "timeStamp" in new_dict.keys() and "timeStamp" in cur_dict.keys():
                if cur_dict["timeStamp"] > new_dict["timeStamp"]:  # 以最新时间为标准
                    new_dict[dict_key] = cur_dict[dict_key]

            else:
                pass

        return new_dict[dict_key]

# 处理论文融合
def merge_paper_process(new_dict, cur_dict, dict_key):
    """
    :param new_dict:
    :param cur_dict:
    :param dict_key: 当前key值
    :return:
    """
    if isinstance(new_dict[dict_key], list) and isinstance(cur_dict[dict_key], list):
        double_paper_list = none_add(new_dict[dict_key], cur_dict[dict_key])
        # print(type(double_paper_list))

        new_paper_list = []  # 临时存储论文
        # new_paper_list.append(double_paper_list)
        if len(new_dict[dict_key]) > 0 and len(cur_dict[dict_key]) > 0:  # 若双方大于0 则进行成果的去重融合

            paper_key_list = list(new_dict[dict_key][0].keys())  # 获取论文的所有字段名
            # del paper_key_list["_id"]
            for double_paper_list_line in double_paper_list:
                is_merge = 0
                for i in range(len(new_paper_list)):
                    # print("*****************************************************************",i,len(new_paper_list))
                    # print(double_paper_list_line)
                    # print("11111111111111111111111111111111111")
                    # print(double_paper_list_line["title"])
                    # print(new_paper_list[i]["titleCn"])
                    if double_paper_list_line["titleCn"] != None and double_paper_list_line['titleCn'] != '' and \
                            new_paper_list[i]["titleCn"] != None and new_paper_list[i]['titleCn'] != '':
                        if double_paper_list_line["titleCn"] in new_paper_list[i]["titleCn"] or new_paper_list[i][
                            "titleCn"] in double_paper_list_line["titleCn"]:
                            for paper_key_list_line in paper_key_list:  # 已知两篇论文是同一篇 则遍人的的每一个字段融合
                                new_paper_list[i][paper_key_list_line] = merge_atom_process(new_paper_list[i],
                                                                                            double_paper_list_line,
                                                                                            paper_key_list_line)
                            # print("中文融合：",double_paper_list_line["titleCn"])
                            is_merge = 1
                            break
                    if double_paper_list_line["titleCn"] != None and double_paper_list_line['titleCn'] != '' and \
                            new_paper_list[i]["titleEn"] != None and new_paper_list[i]['titleEn'] != '':
                        if double_paper_list_line["titleCn"] in new_paper_list[i]["titleEn"] or new_paper_list[i][
                            "titleEn"] in double_paper_list_line["titleCn"]:
                            for paper_key_list_line in paper_key_list:  # 已知两篇论文是同一篇 则遍人的的每一个字段融合
                                new_paper_list[i][paper_key_list_line] = merge_atom_process(new_paper_list[i],
                                                                                            double_paper_list_line,
                                                                                            paper_key_list_line)
                                # print("中文融合：",double_paper_list_line["titleCn"])
                                is_merge = 1
                                break

                    if double_paper_list_line["titleEn"] != None and double_paper_list_line['titleEn'] != '' and \
                            new_paper_list[i]["titleEn"] != None and new_paper_list[i]['titleEn'] != '':
                        if double_paper_list_line["titleEn"] in new_paper_list[i]["titleEn"] or new_paper_list[i][
                            "titleEn"] in double_paper_list_line["titleEn"]:
                            for paper_key_list_line in paper_key_list:  # 已知两篇论文是同一篇 则遍人的的每一个字段融合
                                new_paper_list[i][paper_key_list_line] = merge_atom_process(new_paper_list[i],
                                                                                            double_paper_list_line,
                                                                                            paper_key_list_line)
                            # print("英文融合",double_paper_list_line["titleEn"])
                            is_merge = 1
                            break
                    if double_paper_list_line["titleEn"] != None and double_paper_list_line['titleEn'] != '' and \
                            new_paper_list[i]["titleCn"] != None and new_paper_list[i]['titleCn'] != '':
                        if double_paper_list_line["titleEn"] in new_paper_list[i]["titleCn"] or new_paper_list[i][
                            "titleCn"] in double_paper_list_line["titleEn"]:
                            for paper_key_list_line in paper_key_list:  # 已知两篇论文是同一篇 则遍人的的每一个字段融合
                                new_paper_list[i][paper_key_list_line] = merge_atom_process(new_paper_list[i],
                                                                                            double_paper_list_line,
                                                                                            paper_key_list_line)
                            # print("英文融合",double_paper_list_line["titleEn"])
                            is_merge = 1
                            break

                if is_merge == 0:
                    new_paper_list.append(double_paper_list_line)

            new_dict[dict_key] = new_paper_list



        else:  # 否则直接相加
            new_dict[dict_key] = none_add(new_dict[dict_key], cur_dict[dict_key])
        return new_dict[dict_key]
    else:
        print("paper is not list!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("type is ", type(new_dict[dict_key]), type(cur_dict[dict_key]))
        return []

# 处理专利融合
def merge_patent_project_process(new_dict, cur_dict, dict_key):
    """
    :param new_dict:
    :param cur_dict:
    :param dict_key: 当前key值
    :return:
    """
    if isinstance(new_dict[dict_key], list) and isinstance(cur_dict[dict_key], list):
        double_paper_list = none_add(new_dict[dict_key], cur_dict[dict_key])
        new_paper_list = []  # 临时存储论文
        # new_paper_list.append(double_paper_list)
        if len(new_dict[dict_key]) > 0 and len(cur_dict[dict_key]) > 0:  # 若双方大于0 则进行成果的去重融合

            paper_key_list = list(new_dict[dict_key][0].keys())  # 获取论文的所有字段名
            # del paper_key_list["_id"]
            for double_paper_list_line in double_paper_list:
                is_merge = 0
                for i in range(len(new_paper_list)):
                    if double_paper_list_line["title"] != None and double_paper_list_line['title'] != '' and \
                            new_paper_list[i]["title"] != None and new_paper_list[i]['title'] != '':
                        if double_paper_list_line["title"] in new_paper_list[i]["title"] or new_paper_list[i][
                            "title"] in double_paper_list_line["title"]:
                            for paper_key_list_line in paper_key_list:  # 已知两篇论文是同一篇 则遍人的的每一个字段融合
                                # if paper_key_list_line != "_id":
                                new_paper_list[i][paper_key_list_line] = merge_atom_process(new_paper_list[i],
                                                                                            double_paper_list_line,
                                                                                            paper_key_list_line)
                            # print("pp融合",double_paper_list_line["title"])
                            is_merge = 1
                            break

                    else:
                        continue
                if is_merge == 0:
                    new_paper_list.append(double_paper_list_line)

            new_dict[dict_key] = new_paper_list



        else:  # 否则直接相加
            new_dict[dict_key] = none_add(new_dict[dict_key], cur_dict[dict_key])
        return new_dict[dict_key]
    else:
        print("paper is not list!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("type is ", type(new_dict[dict_key]), type(cur_dict[dict_key]))
        return []

# 处理奖项 融合
def merge_award_process(new_dict, cur_dict, dict_key):
    """
    :param new_dict:
    :param cur_dict:
    :param dict_key: 当前key值
    :return:
    """
    if isinstance(new_dict[dict_key], list) and isinstance(cur_dict[dict_key], list):
        double_paper_list = none_add(new_dict[dict_key], cur_dict[dict_key])
        new_paper_list = []  # 临时存储论文
        # new_paper_list.append(double_paper_list)
        if len(new_dict[dict_key]) > 0 and len(cur_dict[dict_key]) > 0:  # 若双方大于0 则进行成果的去重融合

            paper_key_list = list(new_dict[dict_key][0].keys())  # 获取论文的所有字段名
            # del paper_key_list["_id"]
            for double_paper_list_line in double_paper_list:
                is_merge = 0
                for i in range(len(new_paper_list)):
                    if double_paper_list_line["awardName"] != None and double_paper_list_line['awardName'] != '' and \
                            new_paper_list[i]["awardName"] != None and new_paper_list[i]['awardName'] != '':
                        if double_paper_list_line["awardName"] in new_paper_list[i]["awardName"] or new_paper_list[i][
                            "awardName"] in double_paper_list_line["awardName"]:
                            for paper_key_list_line in paper_key_list:  # 已知两篇论文是同一篇 则遍人的的每一个字段融合
                                # if paper_key_list_line != "_id":
                                new_paper_list[i][paper_key_list_line] = merge_atom_process(new_paper_list[i],
                                                                                            double_paper_list_line,
                                                                                            paper_key_list_line)
                            # print("pp融合",double_paper_list_line["title"])
                            is_merge = 1
                            break
                    if double_paper_list_line["awardProductionName"] != None and double_paper_list_line[
                        'awardProductionName'] != '' and new_paper_list[i]["awardProductionName"] != None and \
                            new_paper_list[i]['awardProductionName'] != '':
                        if double_paper_list_line["awardProductionName"] in new_paper_list[i]["awardProductionName"] or \
                                new_paper_list[i]["awardProductionName"] in double_paper_list_line[
                            "awardProductionName"]:
                            for paper_key_list_line in paper_key_list:  # 已知两篇论文是同一篇 则遍人的的每一个字段融合
                                # if paper_key_list_line != "_id":
                                new_paper_list[i][paper_key_list_line] = merge_atom_process(new_paper_list[i],
                                                                                            double_paper_list_line,
                                                                                            paper_key_list_line)
                            # print("pp融合",double_paper_list_line["title"])
                            is_merge = 1
                            break

                    else:
                        continue
                if is_merge == 0:
                    new_paper_list.append(double_paper_list_line)

            new_dict[dict_key] = new_paper_list



        else:  # 否则直接相加
            new_dict[dict_key] = none_add(new_dict[dict_key], cur_dict[dict_key])
        return new_dict[dict_key]
    else:
        print("paper is not list!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("type is ", type(new_dict[dict_key]), type(cur_dict[dict_key]))
        return []

#融合过程
def merge_process2(data_key, new_dict, cur_dict):
    """
    :param data_key:  字典的字段 key李彪
    :param new_dict: 蓝本信息
    :param cur_dict: 当前信息
    :return:
    """
    for data_key_line in data_key:  # 与上面的同名同机构的融合处理逻辑一致，复用其代码
        # 遍历每条记录的所有key value
        """
            针对成果信息也要进行融合，paper patent project处理思路一样
        """
        if data_key_line == "paper":
            # print("paper-------------new", len(new_dict[data_key_line]))
            # print("paper-------------cur", len(cur_dict[data_key_line]))
            new_dict[data_key_line] = merge_paper_process(new_dict, cur_dict, data_key_line)
            # print(new_dict["name"],new_dict["work_unit"],"论文增加了",len(new_dict[data_key_line]))
            # print("paper----------------", len(new_dict[data_key_line]))
        elif data_key_line == "patent":
            # print("patent-------------new", len(new_dict[data_key_line]))
            # print("patent-------------cur", len(cur_dict[data_key_line]))
            new_dict[data_key_line] = merge_patent_project_process(new_dict, cur_dict, data_key_line)
            # print("patent----------------", len(new_dict[data_key_line]))

        elif data_key_line == "project":
            # print("project-------------new", len(new_dict[data_key_line]))
            # print("project-------------cur", len(cur_dict[data_key_line]))
            new_dict[data_key_line] = merge_patent_project_process(new_dict, cur_dict, data_key_line)
            # print("project----------------", len(new_dict[data_key_line]))

        elif data_key_line == "book":  # 直接相加
            # print
            # print("new book", len(new_dict[data_key_line]))
            # print("cur book", len(cur_dict[data_key_line]))
            # print("book-------------new", len(new_dict[data_key_line]))
            # print("book-------------cur", len(cur_dict[data_key_line]))
            new_dict[data_key_line] = merge_patent_project_process(new_dict, cur_dict, data_key_line)

            # print("book-------------cur", len(new_dict[data_key_line]))
        elif data_key_line == "award":  # 直接相加
            new_dict[data_key_line] = merge_award_process(new_dict, cur_dict, data_key_line)

        elif data_key_line == "edu":  # 直接相加
            new_dict[data_key_line] = none_add(new_dict[data_key_line], cur_dict[data_key_line])

        elif data_key_line == "work":  # 直接相加
            new_dict[data_key_line] = none_add(new_dict[data_key_line], cur_dict[data_key_line])
        elif data_key_line == "news":  # 直接相加
            new_dict[data_key_line] = none_add(new_dict[data_key_line], cur_dict[data_key_line])
        elif data_key_line == "tags":  # 直接相加
            new_dict[data_key_line] = none_add(new_dict[data_key_line], cur_dict[data_key_line])
        elif data_key_line == "evaluate":  # 直接相加
            new_dict[data_key_line] = none_add(new_dict[data_key_line], cur_dict[data_key_line])

        else:
            new_dict[data_key_line] = merge_atom_process(new_dict, cur_dict, data_key_line)
        new_dict["flag"] = 1
    # print( new_dict["flag"])
    return new_dict

#获取flag的值
def get_flag(dict_1):
    if "flag" in dict_1.keys():
        return True
    else:
        return False

# 融合判断
def merge_same_name_org(data_key, same_n_o_list, flag):
    """

    :param data_key:
    :param same_n_o_list: 长度大于1 的同名同机构列表
    :return:

    """
    print("融合判断!!!!!!!!!!!!!!!!")
    finial_list = []
    finial_list.append(same_n_o_list[0])

    for same_n_o_list_line in same_n_o_list:
        is_flag = 0
        # print("******************************************************************",len(same_n_o_list),len(finial_list))
        print()
        for i in range(len(finial_list)):
            if same_n_o_list_line["source_person_id"] == finial_list[i]["source_person_id"] and same_n_o_list_line[
                "source_db"] == finial_list[i]["source_db"]:
                print("原本就为一个人，融合：----------------")
                finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                is_flag = 1
                break  # 若已融合，则结束遍历

            if same_n_o_list_line["gender"] != None and finial_list[i]["gender"] != None and same_n_o_list_line[
                "gender"] != "" and finial_list[i]["gender"] != "" and isinstance(finial_list[i]["gender"],
                                                                                  str) and isinstance(
                    same_n_o_list_line["gender"], str) and same_n_o_list_line["gender"] != finial_list[i]["gender"]:

                if i == len(finial_list) - 1:  # 若遍历完全部的not_org_list 没有融合，则是另外一个人
                    if get_flag(same_n_o_list_line):
                        pass
                    else:
                        same_n_o_list_line["flag"] = 0
                    finial_list.append(same_n_o_list_line)
                    is_flag = 1
                    print("gender is not same and finish")
                else:  # 否则结束本层循环继续遍历
                    print("gender is not same and continue")
            else:  # 若性别同，则无法判断
                # 若ID_number相同 则融合，并结束循环
                if same_n_o_list_line["ID_number"] != None and finial_list[i]["ID_number"] != None and \
                        same_n_o_list_line["ID_number"] != "" and finial_list[i]["ID_number"] != "" and \
                        same_n_o_list_line["ID_number"] == finial_list[i]["ID_number"]:
                    print("ID_number is same and finish")
                    finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                    is_flag = 1
                    break  # 若已融合，则结束遍历

                # 若office_phone相同 则融合，并结束循环
                elif same_n_o_list_line["office_phone"] != None and finial_list[i]["office_phone"] != None and \
                        same_n_o_list_line["office_phone"] != "" and finial_list[i]["office_phone"] != "" and \
                        same_n_o_list_line["office_phone"] == finial_list[i]["office_phone"]:
                    print("office_phone is same and finish")
                    finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                    is_flag = 1
                    break  # 若已融合，则结束遍历

                # 若email相同 则融合，并结束循环
                elif same_n_o_list_line["email"] != None and finial_list[i]["email"] != None and same_n_o_list_line[
                    "email"] != "" and finial_list[i]["email"] != "" and same_n_o_list_line["email"] == finial_list[i][
                    "email"]:
                    print("email is same and finish")
                    finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                    is_flag = 1
                    break  # 若已融合，则结束遍历

                # 若mobile_phone相同 则融合，并结束循环
                elif same_n_o_list_line["mobile_phone"] != None and finial_list[i]["mobile_phone"] != None and \
                        same_n_o_list_line["mobile_phone"] != "" and finial_list[i]["mobile_phone"] != "" and \
                        same_n_o_list_line["mobile_phone"] == finial_list[i]["mobile_phone"]:
                    print("mobile_phone is same and finish")
                    finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                    is_flag = 1
                    break  # 若已融合，则结束遍历

                # 若fax相同 则融合，并结束循环
                elif same_n_o_list_line["fax"] != None and finial_list[i]["fax"] != None and same_n_o_list_line[
                    "fax"] != "" and finial_list[i]["fax"] != "" and same_n_o_list_line["fax"] == finial_list[i]["fax"]:
                    print("fax is same and finish")
                    finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                    is_flag = 1
                    break  # 若已融合，则结束遍历

                # 若start_work_date相同 则融合，并结束循环
                elif same_n_o_list_line["start_work_date"] != None and finial_list[i]["start_work_date"] != None and \
                        same_n_o_list_line["start_work_date"] != "" and finial_list[i]["start_work_date"] != "" and \
                        same_n_o_list_line["start_work_date"] == finial_list[i]["start_work_date"]:
                    print("start_work_date is same and finish")
                    finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                    is_flag = 1
                    break  # 若已融合，则结束遍历

                # 若contact_mobile_phone相同 则融合，并结束循环
                elif same_n_o_list_line["contact_mobile_phone"] != None and finial_list[i][
                    "contact_mobile_phone"] != None and same_n_o_list_line["contact_mobile_phone"] != "" and \
                        finial_list[i]["contact_mobile_phone"] != "" and same_n_o_list_line["contact_mobile_phone"] == \
                        finial_list[i]["contact_mobile_phone"]:
                    print("contact_mobile_phone is same and finish")
                    finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                    is_flag = 1
                    break  # 若已融合，则结束遍历



                else:
                    # 若birthday相同 则融合，并结束循环
                    if same_n_o_list_line["birthday"] != None and finial_list[i]["birthday"] != None and \
                            same_n_o_list_line["birthday"] != "" and finial_list[i]["birthday"] != "":
                        if same_n_o_list_line["birthday"] == finial_list[i]["birthday"]:
                            print("birthday is same and finish")
                            finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                            is_flag = 1
                            break  # 若已融合，则结束遍历


                        else:

                            if i == len(finial_list) - 1:
                                if get_flag(same_n_o_list_line):
                                    pass
                                else:
                                    same_n_o_list_line["flag"] = 0
                                finial_list.append(same_n_o_list_line)
                                is_flag = 1
                                print("birthday is not same and finish")
                            else:  # 否则继续遍历
                                print("birthday is not same and continue")
                                # continue
            # 如果以上规则均未生效，则开启成果比对
            # print("如果以上规则均未生效，则开启成果比对,未生效（0），生效（1）：", is_flag)
            if is_flag == 0:
                if len(finial_list[i]["paper"]) >= 1 and len(same_n_o_list_line["paper"]) >= 1:
                    if is_pruduct_exit(finial_list[i]["paper"], same_n_o_list_line["paper"]):
                        # 融合
                        print("paper is same and finish")
                        print(finial_list[i]["work_unit"], same_n_o_list_line["work_unit"])
                        finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                        is_flag = 1
                        break  # 若已融合，则结束遍历

                if len(finial_list[i]["patent"]) >= 1 and len(same_n_o_list_line["patent"]) >= 1:
                    if is_pruduct_exit(finial_list[i]["patent"], same_n_o_list_line["patent"]):
                        # 融合
                        print("patent is same and finish")

                        finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                        is_flag = 1
                        break  # 若已融合，则结束遍历

                if len(finial_list[i]["project"]) >= 1 and len(same_n_o_list_line["project"]) >= 1:
                    if is_pruduct_exit(finial_list[i]["project"], same_n_o_list_line["project"]):
                        # 融合
                        print("project is same and finish")
                        finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                        is_flag = 1
                        break  # 若已融合，则结束遍历

                if is_flag == 0:  # 若以上规则均未符合则判断为两人

                    if i == len(finial_list) - 1 and flag == 1:  # 若遍历全部 没有融合，则是另外一个人（同名不同机构）
                        print("all file is not same and finish, become two person")
                        if get_flag(same_n_o_list_line):
                            pass
                        else:
                            same_n_o_list_line["flag"] = 0
                        finial_list.append(same_n_o_list_line)
                        is_flag = 1
                        break
                    if i == len(finial_list) - 1 and flag == 0:  # 若遍历全部 没有融合，则融合（同名同机构）
                        print("all file is not same and finish，become one person")
                        finial_list[i] = merge_process2(data_key, finial_list[i], same_n_o_list_line)
                        is_flag = 1
                        break

    return finial_list



#  把融合完的数据清洗入库
# over_size_insert = codecs.open("over_size_insert1.json", "a+", encoding="utf-8")
def insert_clean_data(data_list):
    """
    :param data_list:  数据列表
    :return:
    """
    for line_data in data_list:
        insert_dict = line_data
        try:
            del insert_dict["_id"]
        except Exception as e:
            pass
        id = insert_dict["id"]
        source_db = insert_dict["source_db"]
        source_person_id = insert_dict["source_person_id"]
        # = insert_dict["source_person_id"]
        if len(insert_dict['paper']) >= 1:
            for i in range(len(insert_dict['paper'])):
                insert_dict['paper'][i]["talent_id"] = id
                insert_dict['paper'][i]["source_db"] = source_db
                insert_dict['paper'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['paper'][i]["_id"]
                except Exception as e:
                    # print(e)
                    pass
            for line in insert_dict["paper"]:
                # line["_id"] = line["talent_id"]
                new_paper.insert_one(line)

        if len(insert_dict['patent']) >= 1:
            for i in range(len(insert_dict['patent'])):
                insert_dict['patent'][i]["talent_id"] = id
                insert_dict['patent'][i]["source_db"] = source_db
                insert_dict['patent'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['patent'][i]["_id"]
                except Exception as e:
                    # print(e)
                    pass
            for line in insert_dict["patent"]:
                # line["_id"] = line["talent_id"]
                new_patent.insert_one(line)
        if len(insert_dict['project']) >= 1:
            for i in range(len(insert_dict['project'])):
                insert_dict['project'][i]["talent_id"] = id
                insert_dict['project'][i]["source_db"] = source_db
                insert_dict['project'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['project'][i]["_id"]
                except Exception as e:
                    # print(e)
                    pass
            for line in insert_dict["project"]:
                # line["_id"] = line["talent_id"]
                new_project.insert_one(line)
        if len(insert_dict['book']) >= 1:
            for i in range(len(insert_dict['book'])):
                insert_dict['book'][i]["talent_id"] = id
                insert_dict['book'][i]["source_db"] = source_db
                insert_dict['book'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['book'][i]["_id"]
                except Exception as e:
                    # print(e)
                    pass
            for line in insert_dict["book"]:
                # line["_id"] = line["talent_id"]
                new_book.insert_one(line)
        if len(insert_dict['award']) >= 1:
            for i in range(len(insert_dict['award'])):
                insert_dict['award'][i]["talent_id"] = id
                insert_dict['award'][i]["source_db"] = source_db
                insert_dict['award'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['award'][i]["_id"]
                except Exception as e:
                    # print(e)
                    pass
            for line in insert_dict["award"]:
                # line["_id"] = line["talent_id"]
                new_award.insert_one(line)
        if len(insert_dict['edu']) >= 1:
            for i in range(len(insert_dict['edu'])):
                insert_dict['edu'][i]["talent_id"] = id
                insert_dict['edu'][i]["source_db"] = source_db
                insert_dict['edu'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['edu'][i]["_id"]
                except Exception as e:
                    pass
            for line in insert_dict["edu"]:
                # line["_id"] = line["talent_id"]
                new_edu.insert_one(line)

        if len(insert_dict['work']) >= 1:
            for i in range(len(insert_dict['work'])):
                insert_dict['work'][i]["talent_id"] = id
                insert_dict['work'][i]["source_db"] = source_db
                insert_dict['work'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['work'][i]["_id"]
                except Exception as e:
                    pass
            for line in insert_dict["work"]:
                # line["_id"] = line["talent_id"]
                new_work.insert_one(line)
        if len(insert_dict['news']) >= 1:
            for i in range(len(insert_dict['news'])):
                insert_dict['news'][i]["talent_id"] = id
                insert_dict['news'][i]["source_db"] = source_db
                insert_dict['news'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['news'][i]["_id"]
                except Exception as e:
                    pass
            for line in insert_dict["news"]:
                # line["_id"] = line["talent_id"]
                new_news.insert_one(line)
        if len(insert_dict['tags']) >= 1:
            for i in range(len(insert_dict['tags'])):
                insert_dict['tags'][i]["talent_id"] = id
                insert_dict['tags'][i]["source_db"] = source_db
                insert_dict['tags'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['tags'][i]["_id"]
                except Exception as e:
                    pass
            for line in insert_dict["tags"]:
                # line["_id"] = line["talent_id"]
                new_tags.insert_one(line)
        if len(insert_dict['evaluate']) >= 1:
            for i in range(len(insert_dict['evaluate'])):
                insert_dict['evaluate'][i]["talent_id"] = id
                insert_dict['evaluate'][i]["source_db"] = source_db
                insert_dict['evaluate'][i]["source_person_id"] = source_person_id
                try:
                    del insert_dict['evaluate'][i]["_id"]
                except Exception as e:
                    pass
            for line in insert_dict["evaluate"]:
                # line["_id"] = line["talent_id"]
                new_evaluate.insert_one(line)

        try:
            print("insert")

            del insert_dict["paper"]
            del insert_dict["patent"]
            del insert_dict["project"]
            del insert_dict["award"]
            del insert_dict["book"]
            del insert_dict["edu"]
            del insert_dict["work"]
            del insert_dict["news"]
            del insert_dict["tags"]
            del insert_dict["evaluate"]
            # if insert_dict["flag"] == 1:
            #     over_size_insert.write(str(insert_dict) + "\n")
            big_table_v2.insert_one(insert_dict)
        except Exception as e:
            # over_size_insert.write(str(insert_dict) + "\n")
            print(e)

#生成date数据,用于提取成果中的时间
def produce_date_list():
    date_list= []
    for i in range(1945,2020):
        date_list.append(str(i))

    # save_json("date_list.json",date_list)
    return date_list
# 融合步骤一  找出该集合所有重名的人，找出所有人的信息组合成大表 添加时间戳
def step1_quchong_get_same_name():
    # 建立存贮过大文件时 报错的json数据
    over_size = codecs.open("over_size.json", "a+", encoding="utf-8")
    date_list = produce_date_list()
    name_dict = {}
    name_set = set()
    #找出所有同名的人
    for expert_10w_line in expert.find():#expert 是所有人的大表
        if expert_10w_line['name'] in name_dict.keys():
            name_dict[expert_10w_line['name']].append(expert_10w_line["id"])
        else:
            name_dict[expert_10w_line['name']] =[]
            name_dict[expert_10w_line['name']].append(expert_10w_line["id"])
    for key_line in name_dict.keys():
        if len(name_dict[key_line]) > 1:
            name_set.add(key_line)

    # name_dict[expert_10w_line['name']].append(expert_10w_line)
    save_json("same_name_set.json",name_dict)
    save_json("same_name_set.json",list(name_set))

    for key_line in name_dict.keys():
        if len( name_dict[key_line]) > 1:
            for name_dict_line in name_dict[key_line]:
                talent_id = name_dict_line
                name_dict_line = expert.find({"id":talent_id})

                name_dict_line["paper"] = []
                name_dict_line["patent"] = []
                name_dict_line["project"] = []
                name_dict_line["book"] = []
                name_dict_line["edu"] = []

                name_dict_line["work"] = []
                name_dict_line["award"] = []
                name_dict_line["tags"] = []
                name_dict_line["news"] = []
                name_dict_line["evaluate"] = []
                # talent_id = name_dict_line["id"]
                date_start = 1945

                for paper_line in paper.find({"talent_id": talent_id}):
                    name_dict_line["paper"].append(paper_line)
                    date = get_data2(paper_line, "publishDate")
                    for date_line in date_list:
                        if date_line in date:
                            date = date_line
                            if date > date_start:
                                date_start = date
                                break


                for patent_line in patent.find({"talent_id": talent_id}):
                    name_dict_line["patent"].append(patent_line)
                    date = get_data2(patent_line, "publishDate")
                    for date_line in date_list:
                        if date_line in date:
                            date = date_line
                            if date > date_start:
                                date_start = date
                                break


                for project_line in project.find({"talent_id": talent_id}):
                    name_dict_line["project"].append(project_line)
                    date = get_data2(project_line, "date")
                    for date_line in date_list:
                        if date_line in date:
                            date = date_line
                            if date > date_start:
                                date_start = date
                                break

                for award_line in award.find({"talent_id": talent_id}):
                    name_dict_line["award"].append(award_line)
                    date = get_data2(award_line, "year")
                    for date_line in date_list:
                        if date_line in date:
                            date = date_line
                            if date > date_start:
                                date_start = date
                                break

                for book_line in book.find({"talent_id": talent_id}):
                    name_dict_line["book"].append(book_line)
                    date = get_data2(book_line, "publishDate")
                    for date_line in date_list:
                        if date_line in date:
                            date = date_line
                            if date > date_start:
                                date_start = date
                                break

                for edu_line in edu.find({"talent_id": talent_id}):
                    name_dict_line["edu"].append(edu_line)
                for work_line in work.find({"talent_id": talent_id}):
                    name_dict_line["work"].append(work_line)
                for news_line in news.find({"talent_id": talent_id}):
                    name_dict_line["news"].append(news_line)
                for tags_line in tags.find({"talent_id": talent_id}):
                    name_dict_line["tags"].append(tags_line)
                for evalaute_line in evaluate.find({"talent_id": talent_id}):
                    name_dict_line["evaluate"].append(evalaute_line)
                if date_start ==1945:
                    date_start = 2020
                # date_start = 2020
                name_dict_line["timeStamp"] = date_start

                try:
                    big_table.insert_one(name_dict_line)#把重名的人的大表信息存储下来
                except Exception as e:
                    over_size.write(str(name_dict_line) + "\n")
                    print(e)
                # name_dict_new[key_line]=name_dict[key_line]






# 融合步骤一 对有重名的人 拿出来处理
def step2_quchong():
    version1 = codecs.open("version1.json", "a+", encoding="utf-8")
    """
    same_set=set()
    for big_table_line in big_table.find():
        name = big_table_line['name']
        same_set.add(name)
    print(len(same_set))

    save_json("same_name_set.json",list(same_set))
    """
    # big_table.
    same_name_org = {}
    # with open("same_name_set.json", 'r', encoding='utf-8')as f:
    #     same_name_set = json.load(f)
    same_name_set =  open_json("same_name_set.json")
    # same_name_set = ["陈炜"]
    # same_name_set=["王小凤","张亚栋","杨涛","韩峥","陈建","李海涛","陈炜","王新华","王国斌","李鹏","李刚","张恒","张涛","谭跃进","王丽","王毅"]
    # same_name_set = ["张玉忠"]
    for same_name_set_line in same_name_set:  # 去除所有有重名的 人名
        # print(same_name_set_line)
        same_name_org = {}  # 临时存储同名人的信息
        big_table_result = big_table.find({"name": same_name_set_line})
        con = 0
        for big_table_line in big_table_result:  # 从大表中取为这个名字的所有人的信息
            # print(con)
            con += 1
            version1.write(str(big_table_line) + "\n")
            name = big_table_line['name']
            org = get_data(big_table_line, "work_unit")  # 为防止work_unit字段为空
            if org == "空":
                org = get_data(big_table_line, "workunit_and_job")  # work_unit字段为空,则获取workunit_and_job
            if org == "空":  # 若前两者均为空则按为空处理，为区分不同的空值，则加上数字
                org += str(con)
            name_org = str(name + ";" + org)  # 把人和机构做一个拼接 作为key值
            if len(same_name_org) > 0:
                is_ff = 0
                # print("ppp:",len(same_name_org))
                for key_line in same_name_org.keys():
                    # print(key_line)
                    if name_org in key_line or key_line in name_org:
                        # if name_org in same_name_org.keys():
                        print("111", name_org, key_line)
                        same_name_org[key_line].append(big_table_line)
                        is_ff = 1
                        break
                    else:
                        # print(")
                        # print("continue111", name_org, key_line)
                        continue
                if is_ff == 0:
                    # print("222", name_org, key_line)
                    same_name_org[name_org] = []
                    same_name_org[name_org].append(big_table_line)  # 把同名同机构的存储在dict中{“李四北航”[{}，{}],"李四清华"：[]}

            else:
                same_name_org[name_org] = []
                same_name_org[name_org].append(big_table_line)  # 把同名同机构的存储在dict中{“李四北航”[{}，{}],"李四清华"：[]}
        print("同名列表个数：", len(same_name_org))
        print("开启同名同机构比对················")
        # 对同一人名的人 分两种形式进性处理1,同名同机构 直接融合 同名不同机构判断融合
        for same_name_org_key in same_name_org.keys():  # 遍历 for example{“李四北航”[{那么：“李四”，work_unit:“北航”}，{}],"李四清华"：[]}
            if len(same_name_org[same_name_org_key]) > 1:  # 同名同机构融合
                new_dict = same_name_org[same_name_org_key][0]  # 以列表的第一条记录的信息为蓝本，进行融合扩充
                key_list = list(new_dict.keys())  # 获取一条记录的所有key值
                # 更新同名同机构，更新后 应该是{“李四北航”：{},"李四清华"：{}}
                # print("同名同机构 融合",same_name_org[same_name_org_key][0]["work_unit"])
                same_name_org[same_name_org_key] = merge_same_name_org(key_list, same_name_org[same_name_org_key], 0)
                # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111",same_name_org[same_name_org_key][0]["flag"])
                # same_name_org[same_name_org_key] = merge_process(key_list, new_dict, same_name_org[same_name_org_key])
                print("同名同机构，融合!", same_name_org[same_name_org_key][0]["work_unit"], "同名同机构融合之后的列表长度:",
                      len(same_name_org[same_name_org_key]))
                # print("同名同机构融合")
            else:
                same_name_org[same_name_org_key] = same_name_org[same_name_org_key][0]
                # print("同名不同机构,区别！", same_name_org[same_name_org_key]["work_unit"],"同名不同机构的列表长度：",len(same_name_org[same_name_org_key]))
                # print("同名同机构无：",)
        print("len----------------1", len(same_name_org))
        # 把同名同机构的 的list 改为 dict
        same_name_org_v2 = {}
        for key_line in same_name_org.keys():
            ct = 0
            if isinstance(same_name_org[key_line], list) and len(same_name_org[key_line]) > 0:
                print("同名同机构 融合完 还剩：", len(same_name_org[key_line]))
                for line in same_name_org[key_line]:
                    ct += 1
                    new_key = key_line + str(ct)
                    same_name_org_v2[new_key] = line
            else:
                same_name_org_v2[key_line] = same_name_org[key_line]

        print("len----------------2", len(same_name_org_v2))
        # print()
        # 把字典给改为列表
        same_list = []
        for key_line in same_name_org_v2.keys():
            same_list.append(same_name_org_v2[key_line])
        print("len----------------3", len(same_name_org_v2))
        print("开启同名不同机构比对················")

        if len(same_list) > 1:  # 判断还有多少个同名不同机构的，对同名不同机构的人进行融合判断

            data_key = list(same_list[0].keys())  # 取出一个人信息的所有字段名
            not_org_list = merge_same_name_org(data_key, same_list, 1)


            insert_clean_data(not_org_list)

        else:  # 若就一个话 就直接处理后入库
            # insert_dict=same_name_org[same_name_org.keys()[0]]

            insert_clean_data(same_list)


#测试函数
def test_case():
    pass
    # test paper 融合
    # 测试paper . project . patent 的融合
    # paper = [{"timeStamp":2010,"id":1,'project':[{"title":"一种防治家畜乏情的中药复方制剂及制备方法","name":"","id":"fd"},{"title":"一种防治家畜","name":"一种防治家畜fdsadf","id":""}]}]
    # paper2 = [{"timeStamp":2008,"id":2,'project':[{"title": "fdsafdsdf方制剂及制备方法", "name": "3","id":1}, {"title": "fdafdad ","name":"","id":3,}]}]
    # key_list = ["id","project","timeStamp"]
    # print(merge_process(key_list,paper2[0], paper))
    # print(merge_process2(key_list,paper2[0], paper[0]))
if __name__ == '__main__':
    produce_date_list()
    #第一步 获得同名人的姓名
    # step1_quchong_get_same_name()
    #第二步 对同名人的去重
    # step2_quchong()


