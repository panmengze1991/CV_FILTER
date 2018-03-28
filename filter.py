import pandas as pd

from MandatorySelect import mandatroySelect


# if __name__=="__main__":
def filter_run(cv_type, res_path):
    usecols = ['姓名', '来源', '所在地', '自我介绍', '期望地区', '工作年限（年）',
               '学历', '性别', '生日', '当前公司', '当前职位', '当前状态', '目前年薪',
               '期望行业', '期望职位', '邮箱', 'marriagestate', '技能', '手机号',
               '期望年薪', '工作经历', '教育经历', '语言能力', '项目经历']
    path = "res/"
    result_path = [path + "Java.csv", path + "Web.csv", path + "Mechanic.csv"]
    #
    # data_web_1 = pd.read_excel("01430319（前端通过简历库）.xlsx", usecols=usecols)
    # data_web_0 = pd.read_excel("01430320（前端未通过简历库）.xlsx", usecols=usecols)
    #
    # data_java_1 = pd.read_excel("01430317(java通过简历库).xlsx", usecols=usecols)
    # data_java_0 = pd.read_excel("01430318（Java未通过简历库）.xlsx", usecols=usecols)
    #
    # data_jixie_1 = pd.read_excel("01430321（机械通过简历库）.xlsx", usecols=usecols)
    # data_jixie_0 = pd.read_excel("01430322（机械未通过简历库）.xlsx", usecols=usecols)
    #
    # # 通过
    # data1 = [data_java_1,data_web_1,data_jixie_1]
    # # 未通过
    # data2 = [data_java_0,data_web_0,data_jixie_0]
    # data1 = data1[cv_type]
    # data2 = data2[cv_type]
    # # save_file = path+"jixie_test.csv"
    # save_file = result_path[cv_type]
    #
    # # data['年龄'] = data['生日'].apply\
    # #     (lambda x: 2018 - int(str(x)[:4]) if str(x)[:4] != 'NaT' else 0)
    #
    # data1['label'] = 1
    # data2['label'] = 0
    # data = pd.concat([data1, data2])

    data = pd.read_excel(res_path, usecols=usecols)
    save_file = result_path[cv_type]
    mandatroySelect(data, save_file)
