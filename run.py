# 所有代码已上传私有github，请尊重版权，感谢！
# author ：Panmengze & Lijunfeng
# time : 2018年3月27日00:53:20
import cut_words as cut
import vectorized as vec
import filter as ft

if __name__ == '__main__':
    print('0表示Java')
    print('1表示前端')
    print('2表示机械')
    cv_type = int(input('请输入类型：'))
    path = input('请输入文件全名（包括.xlsx后缀名）：')
    # utils.CV_TYPE = sys.argv[1]
    # cv_type = 0
    # if len(sys.argv) > 1:
    #     cv_type = int(sys.argv[1])
    print('正在进行数据预处理...')
    print('正在进行强规则处理...')
    ft.filter_run(cv_type, path)

    print('正在整理数据...')
    cut.execute(cv_type)

    print('正在匹配模型...')
    vec.execute(cv_type)
