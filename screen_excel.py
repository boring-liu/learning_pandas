import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False

def clear_data(df):
    """数据清理，将不需要的数据清理掉"""
    row_indexs = []
    for row_index, row in df.iterrows():
        if '0天0时' in row['持续时间'] or 'MV' not in row['资源名称'] or '紧急' not in row['告警级别']:  # 将持续时间里面小于1小时的筛选出来
            row_indexs.append(row_index)
    df.drop(row_indexs, inplace=True)  # 删除不需要的数据
    df.index = range(0, len(df))  # 重新建立索引


def clear_ignore_data(df1, df2):
    """清理未开通的数据"""
    i = 0
    row_indexs = []
    while i < len(df2):
        for row_index, row in df1.iterrows():
            if df2['联合电服名称'].at[i] in row['资源名称']:  # 将持续时间里面小于1小时的筛选出来
                row_indexs.append(row_index)
        i += 1
    df1.drop(row_indexs, inplace=True)  # 删除不需要的数据
    df1.index = range(0, len(df1))  # 重新建立索引


def calculat_time(df):
    """计算最后告警时间和开始告警时间之间的差值"""
    if '时间差' in df.axes:
    df.insert(8, column='时间差', value=pd.Timedelta('1 hours'))  # 插入一个列，作为后面两个时间计算值的承载
    i = 0
    while i < len(df):  # 输出Timedelta的值给到持续时
        df.loc[:, '首次告警时间'].at[i] = pd.to_datetime(df.loc[:, '首次告警时间'].at[i])  # 转换为时间类型
        df.loc[:, '最后告警时间'].at[i] = pd.to_datetime(df.loc[:, '最后告警时间'].at[i])
        df.loc[:, '时间差'].at[i] = df.loc[:, '最后告警时间'].at[i] - df.loc[:, '首次告警时间'].at[i]  # 计算出来持续时间
        i += 1

def hour_timedelta(a):
    dt_1 = pd.Timedelta('6 hours')
    return a>dt_1


def del_colunms(df):
    del df['']


while True:
    msg=input('请问是否清理数据：（y/n）')
    if msg =='y':
        filename = 'data/Q2.xlsx'
        df1 = pd.read_excel(filename)  # 导入Excel文件，转成DataFrame数据格式
        ignore_filename = 'data/7次异常固定清单匹配(2)(1).xlsx'
        ignore_name = pd.read_excel(ignore_filename)
        rightfile = 'data/专线监控20210622142355.xlsx'
        rightdf = pd.read_excel(rightfile)  # 导入需要合并的表格
        clear_data(df1)  # 清理不需要的数据
        clear_ignore_data(df1, ignore_name)  # 清理未开通数据
        df1 = df1.merge(rightdf, how='left', left_on='资源名称', right_on='名称')  # 以资源名称为主键 合并表格
        df1.dropna(axis=1, how='all', inplace=True)  # 删除空列
        df1.to_excel('output.xlsx')
        print('数据清理完成')
        break
    else:
        break

output=pd.read_excel('output.xlsx')
print(f'中断时间大于1小时的中断记录有{len(output)}条。｝')
calculat_time(output)  # 计算时间差
print(output['时间差'].dtypes)
#dt_1 = output.loc[output['时间差'].apply(hour_timedelta)]
#print(f'中断时间大于6小时的中断记录有{len(dt_1)}条。')
# count_citys = output['所属地市'].value_counts()
# print(count_citys)
# fig,ax=plt.subplots(figsize=(10,6))
# fig.autofmt_xdate()
# ax.bar(count_citys.index,count_citys.values,width=0.5)
# ax.set_xlabel('所属地市',fontsize=14)
# ax.set_ylabel('中断次数',fontsize=14)
# plt.title('各地市中断次数',fontsize=24)
# plt.show()

print('Done!')
