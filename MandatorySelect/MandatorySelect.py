# -*- coding: utf-8 -*-

import re



from Colleage import CollegeUtils


def get_year(content):
    return int(content[:4])


# 筛选民办学学校
def minban(data):
    data['民办'] = 0
    pattern1 = "[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{4}-[0-9]{2}-[0-9]{2}\s[^\d]+?\s"  # 2005-09-01 2009-07-01 青岛理工大学
    pattern2 = "[0-9]{4}-[0-9]{2}-[0-9]{2}\s1\s[^\d]+?\s"  # 2008-08-01 1 青岛理工大学 机械设计制造及其自动化  1：表示至今
    pattern3 = "[0-9]{4}-[0-9]{2}-[0-9]{2}\s至今\s[^\d]+?\s"  # 2008-08-01 至今 青岛理工大学 机械设计制造及其自动化
    re1 = re.compile(pattern1)
    re2 = re.compile(pattern2)
    re3 = re.compile(pattern3)
    cu = CollegeUtils()
    for x in range(len(data['姓名'])):
        line = data['教育经历'].iloc[x]
        # print(line, x)
        college = re2.search(line)
        if college is not None:  # 2008-08-01 1 青岛理工大学 机械设计制造及其自动化  1：表示至今
            college = college.group().strip()[13:]
            college_nature = cu.getCollege_nature(college)
        else:
            # 2008-08-01 至今 青岛理工大学 机械设计制造及其自动化
            college = re3.search(line)
            if college is not None:
                college = college.group().strip()[14:]
                college_nature = cu.getCollege_nature(college)
            else:
                # 2005-09-01 2009-07-01 青岛理工大学
                college = re1.search(line)
                if college is not None:
                    college = college.group().strip()[22:]
                    college_nature = cu.getCollege_nature(college)
                else:
                    college_nature = "error"
        # print(college)

        if college_nature.find("民办") >= 0 or college_nature == "error":
            data['民办'].iloc[x] = 1
            # print("民办", data['姓名'].iloc[x], college)
            continue
    cu.close()


# 筛选学历与年限
def work_year(data):
    data['学历+年限'] = 0
    p1 = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    pattern_date = re.compile(p1)
    for x in range(len(data['姓名'])):
        if data['学历'].iloc[x] == '本科' or data['学历'].iloc[x] == '硕士':
            if data['工作年限（年）'].iloc[x] >= 2:
                data['学历+年限'].iloc[x] = 1
                # if data['学历'].iloc[x] == '专科':
                #     if data['工作年限（年）'].iloc[x] >= 5:
                #         data['学历+年限'].iloc[x] = 1


# 筛选离职频率
def change_job_fre(data, min):
    """

    :param data:
    :param min: 能容忍能小跳槽间隔，比如低于平均2年跳一次就剔除
    :return:
    """
    data['离职率'] = min
    for x in range(len(data['姓名'])):
        exp = str(data['工作经历'].iloc[x])

        p1 = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
        pattern_date = re.compile(p1)
        date = pattern_date.findall(exp)

        p2 = r'[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{4}-[0-9]{2}-[0-9]{2}\s[^\d]+?(实习)|(兼职)'
        pattern_shixi = re.compile(p2)
        shixi = pattern_shixi.findall(exp)

        work_year = data['工作年限（年）'].iloc[x]
        change_time = (len(date) + 1) // 2 - len(shixi)
        if change_time > 0:
            data['离职率'].iloc[x] = work_year / change_time
        # if len(shixi) != 0 and data['离职率'].iloc[x] < min:
        #     print(x, data['姓名'].iloc[x], "实习或兼职 =", len(shixi), "fre =", data['离职率'].iloc[x],
        #           "work_year =", work_year, "change_time =", change_time, data['工作经历'].iloc[x])


def mandatroySelect(data,save_file):


    # 筛选民办学学校
    minban(data)

    # 筛选学历与年限
    work_year(data)

    # 筛选离职频率
    min = 2
    change_job_fre(data, min)

    data.to_csv(save_file, index=False)
