import os

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import utils
import gensim
from gensim import corpora, models, similarities
import pandas as pd


word_seg_path = 'mid/word_seg'
result_path_java = 'result/Java排名.csv'
result_path_web = 'result/前端排名.csv'
result_path_mechanic = 'result/机械排名.csv'
result_path_java_test = 'result/Java排名test.csv'
result_path_web_test = 'result/前端排名test.csv'
result_path_mechanic_test = 'result/机械排名test.csv'
conditions_java = '经验丰富 熟练 MySQL 数据库 扎实 Java 面向对象 熟悉 设计模式 精通 SpringMVC Spring mybatis 框架 ' \
                  'Eclipse SVN Maven Zookeeper dubbo 互联网 电商 思路 清晰 沟通 理解 认真 踏实 责任心' \
                  '框架设计 代码优化 性能优化 数据库优化 分布式 并发 负载 高可用 系统设计 开发 调优'
conditions_web = '独立 开发 熟练 掌握 前端 技术 HTML5 CSS JavaScript Ajax jquery 开发 项目 精通 JavaScript ' \
                 'JS 语言 核心 DOM BOM Ajax JSON 深刻 理解 Web 标准 可用性 可访问性 经验 模块化 编程思想 ' \
                 ' 代码 书写 习惯 Angular Vue React 主流 前端 开发 框架 文档 逻辑性'
conditions_mechanic = '机械 行业 项目 设计 经验 熟练 掌握 CAD Proe UG 二维 三维 制图 软件 熟悉 机械 加工 装配 基础 ' \
                      '原理 钣金 塑料 模具 知识 责任心 认真 负责 沟通 能力 抗压 听说 读写'
result_path = [result_path_java, result_path_web, result_path_mechanic]
result_path_test = [result_path_java_test, result_path_web_test, result_path_mechanic_test]
conditions = [conditions_java, conditions_web, conditions_mechanic]


class MyCorpus(object):
    def __iter__(self):
        df = utils.read_csv_gbk(word_seg_path)
        words_seg = df['format_word'].tolist()
        for word_seg in words_seg:
            yield word_seg.split()


"""
通过gensim的word2vec转换词库中的词为词向量空间
"""
# if __name__ == '__main__':
def execute(cv_type):
    Corp = MyCorpus()
    dictionary = corpora.Dictionary(Corp)
    # 获取对应岗位数据以及保存路径
    condition = conditions[cv_type]
    save_path = result_path[cv_type]

    # 转换所有简历描述为词包
    corpus = [dictionary.doc2bow(text) for text in Corp]
    # 计算简历的tf_idf模型
    tf_idf = models.TfidfModel(corpus)
    print("简历模型生成完成")

    # 转换需求描述为词包
    conditions_bag = dictionary.doc2bow(condition.split())
    # 计算需求在简历模型中的向量值
    con_tf_idf = tf_idf[conditions_bag]
    print("需求模型生成完成")
    # 计算相似度矩阵
    index = similarities.MatrixSimilarity(tf_idf[corpus])
    print("匹配度计算完成")
    # 取出需求对应相似度
    sims = index[con_tf_idf]

    # 构建csv文件
    sims_series = pd.Series(sims)
    df = utils.read_csv_gbk(word_seg_path)

    # 排序保存整个文件
    df[utils.score] = sims_series
    df[utils.score].astype(float)
    # df[utils.weight] = df[utils.weight].convert_objects(convert_numeric=True)
    df[utils.weight] = df[utils.weight].astype(int)
    # print(df[utils.score])
    # print(df[utils.weight])
    df[utils.score] = df[utils.score]*df[utils.weight]
    df = df.sort_values(by=utils.score, ascending=False)
    # df.drop(['word_seg', 'format_word', utils.score, utils.leaveRate, '学历+年限', '描述'], axis=1, inplace=True)
    df.drop(utils.drops, axis=1, inplace=True)
    utils.save_csv_gbk(save_path, df)
    print("简历评估排序完成，请到", os.path.realpath(save_path), '文件查看')
