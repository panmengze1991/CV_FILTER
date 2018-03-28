import pandas as pd

# 岗位标识
JAVA_CV = 0
WEB_CV = 1
MECHANIC_CV = 2
CV_TYPE = 0

# 是否调试
test = False

# 列表头
# label = '是否通过'
desc = '描述'
name = '姓名'
introduction = '自我介绍'
skill = '技能'
jobExp = '工作经历'
projectExp = '项目经历'
score = '简历评分'
# sim = '相似度'
leaveRate = '离职率'
label = 'label'
degreeAndYear = '学历+年限'
weight = '简历权重'
local = '民办'

drops = ['word_seg', 'format_word', score, leaveRate, degreeAndYear, desc,weight,local]


# 读取文件
def readfile(path):
    with open(path, "rb") as fp:
        content = fp.read()
    return content


# 读取CSV
def read_csv(path):
    return pd.read_csv(path, low_memory=False)


# 读取CSV-gbk
def read_csv_gbk(path):
    return pd.read_csv(path, low_memory=False, encoding='gbk', dtype=str)


# 保存至CSV
def save_csv(path, df):
    df.to_csv(path, index=None)


# 保存至CSV-gbk
def save_csv_gbk(path, df):
    df.to_csv(path, encoding='gbk', index=None)
