import pandas as pd
import jieba

import utils

res_java_path = 'res/Java.csv'
res_web_path = 'res/Web.csv'
res_mechanic_path = 'res/Mechanic.csv'

stop_path = 'stop_words.txt'
desc_path = 'mid/desc'
word_seg_path = 'mid/word_seg'

res_path = [res_java_path, res_web_path, res_mechanic_path]


def get_wight(df, x):
    """
    获取简历描述权重
    """
    #     xiangmu 13/16
    #     ziwo 6/17
    #     jineng 27/58
    mul = 0
    # if df[utils.introduction].iloc[x] == 'missing':
    #     mul += 1
    # if df[utils.skill].iloc[x] == 'missing':
    #     mul += 1
    # if df[utils.jobExp].iloc[x] == 'missing':
    #     mul += 1
    if df[utils.projectExp].iloc[x] == 'missing':
        mul += 1
    return 100 - mul * 25


def combine_desc_from_origin(path1, path0, save):
    """
    合并描述(原始文件)
    """
    df = utils.read_csv_gbk(path1)
    df2 = utils.read_csv_gbk(path0)
    df[utils.label] = '通过'
    df2[utils.label] = '未通过'
    frames = [df, df2]
    df = pd.concat(frames)
    df[utils.desc] = df[utils.name]
    df = df.fillna('missing')
    for x in range(len(df[utils.name])):
        df[utils.desc].iloc[x] = df[utils.introduction].iloc[x] + ' ' + df[utils.skill].iloc[x] + ' ' \
                                 + df[utils.jobExp].iloc[x] + ' ' + df[utils.projectExp].iloc[x]

    # print(df['自我介绍'] + df['技能'])
    df2 = df[[utils.name, utils.desc, utils.label]]
    utils.save_csv_gbk(save, df2)


def combine_desc(path1, save):
    """
    合并描述(单个预处理后文件)
    """
    df = utils.read_csv_gbk(path1)
    df[utils.desc] = df[utils.name]  # 描述
    df[utils.weight] = df[utils.name]  # 权重
    df = df.fillna('missing')
    for x in range(len(df[utils.name])):
        df[utils.weight].iloc[x] = get_wight(df, x)
        df[utils.desc].iloc[x] = df[utils.introduction].iloc[x] + ' ' + df[utils.skill].iloc[x] + ' ' + \
                                 df[utils.jobExp].iloc[x] + ' ' + df[utils.projectExp].iloc[x]

    # df2 = df[[utils.name, utils.desc, utils.label]]
    utils.save_csv_gbk(save, df)


def slice_words(path, save):
    """
    切词
    """
    df = utils.read_csv_gbk(path)
    df[utils.leaveRate] = df[utils.leaveRate].astype(float)
    df[utils.degreeAndYear] = df[utils.degreeAndYear].astype(int)
    df[utils.local] = df[utils.local].astype(int)
    df = df[df[utils.leaveRate] >= 2]
    df = df[df[utils.degreeAndYear] == 1]
    df = df[df[utils.local] == 0]
    df['word_seg'] = df[utils.desc]
    df['word_seg'] = df['word_seg'].apply(lambda x: ' '.join(jieba.cut(x)))
    # for index, person in df.iterrows():
    #     content = person[utils.desc].replace('\n\r', '')  # 删除换行
    #     content = content.replace(' ', '')  # 删除换行
    #     person['word_seg'] = ' '.join(jieba.cut(content))
    utils.save_csv_gbk(save, df)


def format_words(path, save):
    """
    格式化
    """
    stop = [line.strip() for line in open(stop_path, encoding='utf-8').readlines()]
    df = utils.read_csv_gbk(path)
    df['format_word'] = df['word_seg']
    for index, person in df.iterrows():
        format_word = ''
        for word in person['word_seg'].split():
            if word not in stop:
                format_word += ' ' + word
        person['format_word'] = format_word
    utils.save_csv_gbk(save, df)


# if __name__ == '__main__':
def execute(cv_type):
    # df = utils.read_csv('res/sql_result.csv')
    # utils.save_csv_gbk('res/sql_result_gbk.csv',df)
    # 合并出description
    combine_desc(res_path[cv_type], desc_path)
    # 切词
    slice_words(desc_path, word_seg_path)
    # 去除停用词
    format_words(word_seg_path, word_seg_path)
