import pandas as pd
pd.set_option('display.width', 1000)#加了这一行那表格的一行就不会分段出现了
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)

from pyecharts.globals import SymbolType, ThemeType
'''
CAND_NAME – 接受捐赠的候选人姓名
NAME – 捐赠人姓名
STATE – 捐赠人所在州
EMPLOYER – 捐赠人所在公司
OCCUPATION – 捐赠人职业
TRANSACTION_AMT – 捐赠数额（美元）
TRANSACTION_DT – 收到捐款的日期
CAND_PTY_AFFILIATION – 候选人党派
# '''
df_data = pd.read_csv("weball20.txt", sep = '|',names=['CAND_ID','CAND_NAME','CAND_ICI','PTY_CD','CAND_PTY_AFFILIATION','TTL_RECEIPTS',
                                                          'TRANS_FROM_AUTH','TTL_DISB','TRANS_TO_AUTH','COH_BOP','COH_COP','CAND_CONTRIB',
                                                          'CAND_LOANS','OTHER_LOANS','CAND_LOAN_REPAY','OTHER_LOAN_REPAY','DEBTS_OWED_BY',
                                                          'TTL_INDIV_CONTRIB','CAND_OFFICE_ST','CAND_OFFICE_DISTRICT','SPEC_ELECTION','PRIM_ELECTION','RUN_ELECTION'
                                                          ,'GEN_ELECTION','GEN_ELECTION_PRECENT','OTHER_POL_CMTE_CONTRIB','POL_PTY_CONTRIB',
                                                          'CVG_END_DT','INDIV_REFUNDS','CMTE_REFUNDS'])
# 读取候选人和委员会的联系信息
df_data1 = pd.read_csv("ccl.txt", sep = '|',names=['CAND_ID','CAND_ELECTION_YR','FEC_ELECTION_YR','CMTE_ID','CMTE_TP','CMTE_DSGN','LINKAGE_ID'])
df_data1=pd.merge(df_data1,df_data)
df_data1=pd.DataFrame(df_data1,columns=[ 'CMTE_ID','CAND_ID', 'CAND_NAME','CAND_PTY_AFFILIATION'])
#随意输出10行看其格式是否符合我们需要的
# print(df_data1.sample(10))
df_data2= pd.read_csv('itcont_2020_20200722_20200820.txt', sep='|',names=['CMTE_ID','AMNDT_IND','RPT_TP','TRANSACTION_PGI',
                                                                                  'IMAGE_NUM','TRANSACTION_TP','ENTITY_TP','NAME','CITY',
                                                                                  'STATE','ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT',
                                                                                  'TRANSACTION_AMT','OTHER_ID','TRAN_ID','FILE_NUM','MEMO_CD',
                                                                                  'MEMO_TEXT','SUB_ID'])
df_data2=pd.merge(df_data2,df_data1)
df_data2=pd.DataFrame(df_data2,columns=['CAND_NAME','NAME', 'STATE','EMPLOYER','OCCUPATION',
                                           'TRANSACTION_AMT', 'TRANSACTION_DT','CAND_PTY_AFFILIATION'])
#输出前10行看数据是否符合我们的目标数据
# print(df_data2.head(10))
#
# print(df_data2.shape)
# print(df_data2.info())
#先给空值行数据赋值
df_data2['STATE'].fillna('NOT PROVIDED',inplace=True)
df_data2['EMPLOYER'].fillna('NOT PROVIDED',inplace=True)
df_data2['OCCUPATION'].fillna('NOT PROVIDED',inplace=True)
# 查看每一行的具体数据是怎么样的方便进行下一步操作
# for i in df_data2.columns:
#     print(df_data2.groupby(i).size())
#一般数据量比较小的方便观察但是因为这里数据量太大所以其数据分类显示不完，不过还是能看出有些数据
#是错误的比如TRANSACTION_AMT 捐赠数额（美元）其中的数据还存在负值，明显就是错误数据这时我们就需要将其
#处理->简要处理凡是为负值的变为0
df_data2['TRANSACTION_AMT']=df_data2['TRANSACTION_AMT'].apply(lambda x:x if x>0 else 0)#对列进行替换，apply看前面的数据是series还是dataframe，lambda得到的是内部的元素
#使用apply最后得到时会都是series数据  再如 df['x1'] = df.apply(lambda x: x.amount if x.name != "" else 0, axis=1)
print(df_data2.groupby('TRANSACTION_AMT').size())#再次计算这一列的数据
# # 对日期TRANSACTION_DT列进行处理
df_data2['TRANSACTION_DT'] = df_data2['TRANSACTION_DT'] .astype(str)#改为str类型是因为str方便修改时间之后也可以修改回去
# # 将日期格式改为年月日  7242020
df_data2['TRANSACTION_DT'] = [i[3:7]+i[0]+i[1:3] for i in df_data2['TRANSACTION_DT'] ]
# #重新检查类型
df_data2.info()
# #随意输出10行判断数据是否修改
print(df_data2['TRANSACTION_DT'].sample(10))
# # # 计算每个党派的所获得的捐款总额，然后排序，取前十位
# # print(df_data2.groupby("CAND_PTY_AFFILIATION").sum().sort_values("TRANSACTION_AMT",ascending=False).head(10))
# # # 计算每个总统候选人所获得的捐款总额，然后排序，取前十位
# # print(df_data2.groupby("CAND_NAME").sum().sort_values("TRANSACTION_AMT",ascending=False).head(10))
# # # 查看不同职业的人捐款的总额，然后排序，取前十位
# # print(df_data2.groupby('OCCUPATION').sum().sort_values("TRANSACTION_AMT",ascending=False).head(10))
# # # 查看每个职业捐款人的数量
# # print(df_data2['OCCUPATION'].value_counts().head(10))
# # # 每个州获捐款的总额，然后排序，取前十位
# # print(df_data2.groupby('STATE').sum().sort_values("TRANSACTION_AMT",ascending=False).head(10))
# # # 查看每个州捐款人的数量，取前十位
# # print(df_data2['STATE'].value_counts().head(10))
#
#
from pyecharts import options as opts
#词云图
from pyecharts.charts import WordCloud, Boxplot
#是基于人数排名的
y_NAME=df_data2.groupby('CAND_NAME').size().sort_values(ascending=False).head(25).values.tolist()
x_NAME=df_data2.groupby('CAND_NAME').size().sort_values(ascending=False).head(25).index.tolist()
data_111=list(zip(x_NAME,y_NAME))
# print(data_111)
word=(
    WordCloud(init_opts=opts.InitOpts(width="1900px", height="1000px",theme=ThemeType.DARK))
    .add(series_name="票选人物TOP25", data_pair=data_111, word_size_range=[20, 100],shape=SymbolType.DIAMOND)
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="ballots_top-25", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
)
#
Y_container=[]
for i in x_NAME:#前25个人的箱型数据
    Y_container.append(df_data2[df_data2.CAND_NAME==i]["TRANSACTION_AMT"].values.tolist())

#单独分析其中比较突出的两个候选人，我们只关注给他们捐款的钱数，公司，还有对应捐款人的职业
print(x_NAME[1]+':')
print(df_data2[df_data2.CAND_NAME==x_NAME[1]].loc[:,['TRANSACTION_AMT','EMPLOYER','OCCUPATION']].sort_values('TRANSACTION_AMT',ascending=False).head(20))
print(df_data2[df_data2.CAND_NAME==x_NAME[1]].groupby('EMPLOYER').sum().sort_values('TRANSACTION_AMT',ascending=False).head(20))
# df_data1=df_data2.copy()
# df_data1.drop(index=df_data2[df_data2.CAND_NAME==x_NAME[1]].loc[:,['TRANSACTION_AMT','EMPLOYER','OCCUPATION']].sort_values('TRANSACTION_AMT',ascending=False).head(10).index,inplace=True)
# print(df_data1[df_data1.CAND_NAME==x_NAME[1]].loc[:,['TRANSACTION_AMT','EMPLOYER','OCCUPATION']].sort_values('TRANSACTION_AMT',ascending=False).head(20))
print(x_NAME[2]+':')
print(df_data2[df_data2.CAND_NAME==x_NAME[2]].loc[:,['TRANSACTION_AMT','EMPLOYER','OCCUPATION']].sort_values('TRANSACTION_AMT',ascending=False).head(20))
print(df_data2[df_data2.CAND_NAME==x_NAME[2]].groupby('EMPLOYER').sum().sort_values('TRANSACTION_AMT',ascending=False).head(20))

# .groupby('TRANSACTION_AMT','').sort_values(ascending=False).head(10)
# df_data_y=df_data2.groupby('CAND_NAME')
# print(df_data_y[1][df_data_y[1].TRANSACTION_AMT>100000]['TRANSACTION_AMT'])
# error.append(df_data2[(df_data2.CAND_NAME == i) and (df_data2.TRANSACTION_AMT>100000)]['TRANSACTION_AMT'].values.tolist())
# ['NAME','EMPLOYER','OCCUPATION','TRANSACTION_AMT']

box_plot = Boxplot(init_opts=opts.InitOpts(width="2400px", height="1500px",theme=ThemeType.CHALK))

box_plot = (
    box_plot.add_xaxis(xaxis_data=x_NAME)
    .add_yaxis(series_name="", y_axis=box_plot.prepare_data(Y_container),itemstyle_opts=opts.ItemStyleOpts(color='blue'))
    .set_global_opts(
        datazoom_opts=opts.DataZoomOpts(is_show=True),
        title_opts=opts.TitleOpts(
            pos_left="center", title="GAND_NAME_TOP25获取捐款"
        ),
        tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="shadow"),
        xaxis_opts=opts.AxisOpts(
            # type_="category",
            boundary_gap=True,
            splitarea_opts=opts.SplitAreaOpts(is_show=False),
            # axislabel_opts=opts.LabelOpts(formatter="expr {value}"),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
        yaxis_opts=opts.AxisOpts(
            # type_="value",#值轴，一般默认的是类别轴
            type_='value',
            name="所获捐赠",

            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
    )
    .set_series_opts(tooltip_opts=opts.TooltipOpts(formatter="{b}: {c}"))
)
# 前面的结果似乎耐人寻味，因为排名第一的拜登似乎最大值，平均值都没别人的大
sum_data=df_data2.groupby('CAND_NAME').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).sort_values('TRANSACTION_AMT',ascending=True)['TRANSACTION_AMT']
sum_data_y=sum_data.values.tolist()
sum_data_x=sum_data.index.tolist()
from pyecharts.charts import Bar
bar_1=(
    Bar(init_opts=opts.InitOpts(width="1700px", height="1000px",theme=ThemeType.CHALK))
    .add_xaxis(sum_data_x)
    .add_yaxis('获得的捐赠总金额',sum_data_y,bar_width='40%')
    .reversal_axis()
    .set_global_opts(title_opts=opts.TitleOpts(title='获得捐赠总金额排名前10的候选人',pos_left='left'),legend_opts=opts.LegendOpts(pos_left='left',is_show=False))
)
# 分析完之后让我们重新意识到虽然拜登的平均，最大值都不如别人但是其获得投票的人数是最多的，也从侧面看出了支持拜登的更多是平民，而非资本家
# 分析拜登参与投票中的职业捐款组成
OCCUPATION_data=df_data2[df_data2.CAND_NAME==x_NAME[0]].groupby('OCCUPATION').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).sort_values('TRANSACTION_AMT',ascending=True)
OCCUPATION_data_y=OCCUPATION_data['TRANSACTION_AMT'].values.tolist()
OCCUPATION_data_x=OCCUPATION_data.index.tolist()
bar_2=(
    Bar(init_opts=opts.InitOpts(width="1700px", height="1000px",theme=ThemeType.CHALK))
    .add_xaxis(OCCUPATION_data_x)
    .add_yaxis('捐赠总金额',OCCUPATION_data_y,bar_width='40%')
    .reversal_axis()
    .set_global_opts(title_opts=opts.TitleOpts(title='对拜登捐赠总金额排名前10的职业',pos_right='center'),legend_opts=opts.LegendOpts(pos_right='right',is_show=False))
)
from pyecharts.charts import Grid
grid_1=(
    Grid(init_opts=opts.InitOpts(width='1900px',height='1000px',theme=ThemeType.CHALK))
    .add(bar_1,grid_opts=opts.GridOpts(pos_right='55%'))
    .add(bar_2,grid_opts=opts.GridOpts(pos_left='55%'))
)

data=df_data2[df_data2['CAND_NAME']=='BIDEN, JOSEPH R JR']
data_y=data.groupby('STATE').sum().sort_values("TRANSACTION_AMT",ascending=False).head(10)['TRANSACTION_AMT'].tolist()
data_x=data.groupby('STATE').sum().sort_values("TRANSACTION_AMT",ascending=False).head(10).index.tolist()
sum1=sum(data_y)
data_y=[round(i/sum1*100,1) for i in data_y]
from pyecharts.charts import Pie
pie = (
    # Pie()
    # .add("", [list(z) for z in zip(data_x, data_y)])
    # # .set_colors(["blue", "green", "black", "red", "pink", "orange", "purple"])
    # .set_global_opts(title_opts=opts.TitleOpts(title="TRANSACTION_AMT"))
    # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
    Pie(init_opts=opts.InitOpts(width="1900px", height="1100px",theme=ThemeType.PURPLE_PASSION))
    .add(
        "各州捐款数占比",
        [list(z) for z in zip(data_x, data_y)],
        radius=["40%", "50%"],
        center=[600,450],
        label_opts=opts.LabelOpts(

            position="outside",
            formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            background_color="#eee",
            border_color="#aaa",
            border_width=1,
            border_radius=4,
            rich={
                "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                "abg": {
                    "backgroundColor": "#e3e3e3",
                    "width": "100%",
                    "align": "right",
                    "height": 22,
                    "borderRadius": [4, 4, 0, 0],
                },
                "hr": {
                    "borderColor": "#aaa",
                    "width": "100%",
                    "borderWidth": 0.5,
                    "height": 0,
                },
                "b": {"fontSize": 16, "lineHeight": 33},
                "per": {
                    "color": "#eee",
                    "backgroundColor": "#334455",
                    "padding": [2, 4],
                    "borderRadius": 2,
                },
            },
        ),
    )
    # .set_global_opts(title_opts=opts.TitleOpts(title="TRANSACTION_AMT"))
)

Y_CAND_PTY_AFFILIATION=df_data2.groupby('CAND_PTY_AFFILIATION').size().sort_values(ascending=False).head(5).values.tolist()
X_CAND_PTY_AFFILIATION=df_data2.groupby('CAND_PTY_AFFILIATION').size().sort_values(ascending=False).head(5).index.tolist()
from pyecharts.charts import Bar
Bar_YX=(
    Bar(init_opts=opts.InitOpts(width='1900px',height='1000px',theme=ThemeType.CHALK))
    .add_xaxis(X_CAND_PTY_AFFILIATION)
    .add_yaxis('候选人党派获取支持票数',Y_CAND_PTY_AFFILIATION)
    # .reversal_axis()
    .set_global_opts(title_opts=opts.TitleOpts(title='候选人党派')
                     ,toolbox_opts=opts.ToolboxOpts(is_show=True))
)
#
from pyecharts.charts import Bar
from pyecharts import options as opts
y=df_data2.groupby('STATE').sum().sort_values("TRANSACTION_AMT",ascending=False).head(10)['TRANSACTION_AMT'].tolist()
y=[round(i/1e7,3) for i in y]
# print(y)
x=df_data2.groupby('STATE').sum().sort_values("TRANSACTION_AMT",ascending=False).head(10).index.tolist()
# print(x)
# print(x)
c1=(
    Bar(init_opts=opts.InitOpts(width="800px", height="600px"))
    .add_xaxis(x)
    .add_yaxis('TRANSACTION_AMT',y,itemstyle_opts=opts.ItemStyleOpts(color='Teal'),
                       label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}",
                                                 color='cyan'))
    # .reversal_axis()
    .set_global_opts(
        legend_opts=opts.LegendOpts(pos_left='left',pos_top='top'),
        xaxis_opts=opts.AxisOpts(
                name='STATE',
                name_location='middle',
                name_gap=30,  # 与x轴线的距离
                # name_Rorate设置旋转角度

                #                 x轴名称的格式配置
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Microsoft Yahei',
                    font_size=20,
                ),
                #                 坐标轴刻度配置项
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    #                     is_show=False,  # 是否显示
                    is_inside=True,  # 刻度线是否在内侧
                ),
                #                 坐标轴线的配置
                axisline_opts=opts.AxisLineOpts(
                    symbol='none',
                    linestyle_opts=opts.LineStyleOpts(
                        width=1,
                        color='black',
                    )
                ),
                axislabel_opts=opts.LabelOpts(
                    rotate=40,
                    font_size=12,
                    font_family='Arial',
                    font_weight='bold'
                ),

            ),
            yaxis_opts=opts.AxisOpts(
                name='TRANSACTION_AMT_SUM(/1e7)',
                name_location='middle',
                name_gap=60,
                min_=0,
                max_=3,
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Times New Roman',
                    font_size=20,
                    color='black',
                    #                     font_weight='bolder',
                ),
                axistick_opts=opts.AxisTickOpts(

                    is_show=False,  # 是否显示

                    is_inside=True,  # 刻度线是否在内侧
                ),
                axislabel_opts=opts.LabelOpts(
                    font_size=12,
                    font_family='Times New Roman',
                    formatter="{value}"  # y轴显示方式以数据形式

                ),
                splitline_opts=opts.SplitLineOpts(is_show=True,linestyle_opts=opts.LineStyleOpts(color='black')),  # y轴网格线
                axisline_opts=opts.AxisLineOpts(is_show=False),  # y轴线
            ),
            # title_opts=opts.TitleOpts(
            #     title="",  # 标题
            #     title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 主标题字体大小
            #     subtitle="17195190_刘帅",  # 副标题
            # pos_left='6%'),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
    .set_series_opts(markline_opts=opts.MarkLineOpts(
        data=[
            opts.MarkLineItem(type_="average", name="平均值"),
            opts.MarkLineItem(type_='min',name='最小值'),
            opts.MarkLineItem(symbol="none", x="90%", y="max"),
            opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
        ]
            ))
)

# print(df_data2.groupby('STATE'))#grouby使用sum后会自动寻找其中的可以求和的
# 数据项进行求和（一般是int、float类型才行）
x1=df_data2.groupby('STATE').size().sort_values(ascending=False).head(10).index.tolist()
y1=df_data2.groupby('STATE').size().sort_values(ascending=False).head(10).tolist()
c2=(
    Bar(init_opts=opts.InitOpts(width="800px", height="600px"))
    .add_xaxis(x1)
    .add_yaxis('TRANSACTION',y1,itemstyle_opts=opts.ItemStyleOpts(color='Navy'),label_opts=opts.LabelOpts(color='cyan'))
    # .reversal_axis()
    .set_global_opts(
                datazoom_opts=opts.DataZoomOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(
                name='STATE',
                name_location='middle',
                name_gap=30,  # 与x轴线的距离
                # name_Rorate设置旋转角度
                #                 x轴名称的格式配置
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Microsoft Yahei',
                    font_size=20,
                ),
                #                 坐标轴刻度配置项
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    #                     is_show=False,  # 是否显示
                    is_inside=True,  # 刻度线是否在内侧
                ),
                #                 坐标轴线的配置
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        width=1,
                        color='black',
                    )
                ),
                axislabel_opts=opts.LabelOpts(
                    rotate=40,
                    font_size=12,
                    font_family='Arial',
                    font_weight='bold'
                ),

            ),
            yaxis_opts=opts.AxisOpts(
                name='TRANSACTION_PERSON_NUMBER',
                name_location='middle',
                name_gap=50,
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Times New Roman',
                    font_size=20,
                    color='black',
                    #                     font_weight='bolder',
                ),
                axistick_opts=opts.AxisTickOpts(

                    is_show=False,  # 是否显示

                    is_inside=True,  # 刻度线是否在内侧
                ),
                axislabel_opts=opts.LabelOpts(
                    font_size=12,
                    font_family='Times New Roman',
                    formatter="{value}"  # y轴显示方式以数据形式
                ),
                splitline_opts=opts.SplitLineOpts(is_show=True,linestyle_opts=opts.LineStyleOpts(color='black')),  # y轴网格线
                axisline_opts=opts.AxisLineOpts(is_show=False),  # y轴线
            ),
            # title_opts=opts.TitleOpts(
            #     title="TRANSACTION_AMT_person",  # 标题
            #     title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 主标题字体大小
            #     subtitle="17195190_刘帅",  # 副标题
            # pos_left='6%'),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
        .set_series_opts(markline_opts=opts.MarkLineOpts(
        data=[
            opts.MarkLineItem(type_="average", name="平均值"),
            opts.MarkLineItem(type_='min',name='最小值'),
            opts.MarkLineItem(symbol="none", x="90%", y="max"),
            opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
        ]
    ))
)
from pyecharts.charts import Line
data_1=df_data2.groupby('STATE').size().sort_values(ascending=False).head(10).index.tolist()
data_2=df_data2.groupby('STATE').sum()['TRANSACTION_AMT']
data_2=[data_2[i] for i in data_1]
p=sum(data_2)
data_2=[round(i/p*100,2) for i in data_2]

line_1=(
    Line(init_opts=opts.InitOpts(width="800px", height="500px",theme=ThemeType.PURPLE_PASSION))
    .add_xaxis(data_1)
    .add_yaxis('TRANSACTION_ATtop10_AVERAGE', y_axis=data_2,
               )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="捐赠人数排行前10的人均捐赠数目",pos_left='left',pos_top='center',
                                  title_textstyle_opts=opts.TextStyleOpts( font_family='Times New Roman',
                                font_size=20,
                                color='black',)
                                  ),#一定程度上反应了州的经济水平
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts( name='STATE',
                name_location='middle',
                name_gap=50,
              type_="category",
              boundary_gap=False,
              name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Times New Roman',
                    font_size=20,
                    color='black',
                ),
        axislabel_opts=opts.LabelOpts(
            rotate=40)),
        legend_opts=opts.LegendOpts(is_show=False),
yaxis_opts=opts.AxisOpts(
                name='TRANSACTION_PERSON_NUMBER',
                name_location='middle',
                name_gap=50,
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Times New Roman',
                    font_size=20,
                    color='black',
                    # font_weight='bolder',
                ),
                axistick_opts=opts.AxisTickOpts(

                    is_show=False,  # 是否显示

                    is_inside=True,  # 刻度线是否在内侧
                ),
                axislabel_opts=opts.LabelOpts(
                    font_size=12,
                    font_family='Times New Roman',
                    formatter="{value}"  # y轴显示方式以数据形式
                ),
                axisline_opts=opts.AxisLineOpts(is_show=False),  # y轴线
            )
    )
    .set_series_opts(markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="average", name="平均值"),
                opts.MarkLineItem(type_='min', name='最小值'),
                opts.MarkLineItem(symbol="none", x="90%", y="max"),
                opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
            ]
        )
    )
)

from pyecharts.charts import Grid
p1=(
    Grid(init_opts=opts.InitOpts(width="1900px", height="1400px",theme=ThemeType.CHALK))
    # Page(layout=Page.SimplePageLayout)
    .add(c1,grid_opts=opts.GridOpts(pos_bottom='60%',pos_right='55%'))
    .add(c2,grid_opts=opts.GridOpts(pos_bottom='60%',pos_left='55%'))
    .add(line_1,grid_opts=opts.GridOpts(pos_top='60%',pos_right='50%'))
)



'''# 杨航锋的方法
    df['x1'] = df.apply(lambda x: x.amount if x.name != "" else 0, axis=1)

    # 张翼轸的方法
    df['x2'] = np.where(df['name'] == '', 0, df['amount'])

    df['x3'] = df['amount'].where(df['name'] != '', 0)

    df['x4'] = df['amount']
    df.loc[df['name'] == '', 'x4'] = 0
'''
'''
CAND_NAME – 接受捐赠的候选人姓名
NAME – 捐赠人姓名
STATE – 捐赠人所在州
EMPLOYER – 捐赠人所在公司
OCCUPATION – 捐赠人职业
TRANSACTION_AMT – 捐赠数额（美元）
TRANSACTION_DT – 收到捐款的日期
CAND_PTY_AFFILIATION – 候选人党派
# '''
#研究各职业的每天的捐款流入，但是因为职业存在很多所以这里只研究了总捐赠前10的职业,可以认为是主职业捐赠流入，若都下降说明小职业捐赠流入增多
OCCUPATION_top10=df_data2.groupby('OCCUPATION').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).index.tolist()
STATE_top10=df_data2.groupby('STATE').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).index.tolist()
# print(OCCUPATION_top10)
def find(x,l):
    if x not in l:
        return 0
    else:
        return l[x]
dete_occupation_y=[]
dete_state_y=[]
for i in df_data2.groupby('TRANSACTION_DT').size().index.tolist():
    ans_date=[]
    date=i[0:4]+'/'+'{:02}'.format(int(i[4:5]))+'/'+i[5:]
    find_y=df_data2[df_data2.TRANSACTION_DT==i].groupby('OCCUPATION').sum().sort_values('TRANSACTION_AMT',ascending=False)['TRANSACTION_AMT']
    find_y_1 =df_data2[df_data2.TRANSACTION_DT == i].groupby('STATE').sum().sort_values('TRANSACTION_AMT', ascending=False)['TRANSACTION_AMT']
    # sum_find_y=0
    # for j in OCCUPATION_top10:
    #     sum_find_y+=find(j,find_y)
    sum_find_y=sum(find_y.values)#不能只是取这top10的数据来计算百分比,因为这样只能分析到这10个数据之间的变化,不能得到
    sum_find_y_1=sum(find_y_1.values)
    for j in OCCUPATION_top10:
         dete_occupation_y.append([date,round(find(j,find_y)/sum_find_y*100,1),j])#使用百分比实际上也是将数据缩放到一个范围内
    for j in STATE_top10:
        dete_state_y.append([date,round(find(j,find_y_1)/sum_find_y_1*100,1),j])
# print(dete_sum_y)
from pyecharts.charts import Calendar
import datetime
from pyecharts import options as opts

data_dete=df_data2.groupby('TRANSACTION_DT').sum()['TRANSACTION_AMT'].values.tolist()
begin = datetime.date(2020, 7, 22)
end = datetime.date(2020, 8, 20)
data = [
    [str(begin + datetime.timedelta(days=i)),data_dete[i] ]
    for i in range((end - begin).days + 1)
]
import numpy as np
split=np.linspace(min(data_dete),max(data_dete),8)
end_split=[]
for i in range(0,7):
    end_split.append({'min':split[i],'max':split[i+1]})
calendar=(
    Calendar(init_opts=opts.InitOpts(width="1900px", height="800px",theme=ThemeType.PURPLE_PASSION))
    .add(
        series_name="",
        yaxis_data=data,
        calendar_opts=opts.CalendarOpts(
            pos_top="120",
            pos_left="30",
            pos_right="30",
            range_="2020",
            yearlabel_opts=opts.CalendarYearLabelOpts(is_show=False),

        ),
        # label_opts=opts.LabelOpts(color='purple')
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(pos_top="30", pos_left="center", title="过去一个月每天获得的捐款数"),
        visualmap_opts=opts.VisualMapOpts(
            max_=max(data_dete),
            min_=min(data_dete),
            orient="horizontal",
            is_piecewise=True,
            pos_top="center",
            pos_left="center",
            # is_inverse=True,
            pieces=end_split,
            textstyle_opts=opts.TextStyleOpts(color='write',font_size=20,font_family='Microsoft YaHei')
            ,item_height=20,item_width=30
        ),
    )
)

from pyecharts.charts import ThemeRiver
river=(
    ThemeRiver(init_opts=opts.InitOpts(width='1900px',height='1000px',theme=ThemeType.CHALK))
    .add(
        series_name=OCCUPATION_top10,
        data=dete_occupation_y,
        singleaxis_opts=opts.SingleAxisOpts(
        pos_top="50", pos_bottom="50", type_="time"
    ),
)
    .set_global_opts(

        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line")
        ,title_opts=opts.TitleOpts(title='总捐赠top10职业每天的捐赠流入'),
        datazoom_opts=opts.DataZoomOpts(is_show=True),
    )
)
river1=(
    ThemeRiver(init_opts=opts.InitOpts(width='1900px',height='1000px',theme=ThemeType.CHALK))
    .add(
        series_name=STATE_top10,
        data=dete_state_y,
        singleaxis_opts=opts.SingleAxisOpts(
        pos_top="50", pos_bottom="50", type_="time"
    ),
)
    .set_global_opts(

        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line")
        ,title_opts=opts.TitleOpts(title='总捐赠top10的州每天的捐赠流入'),
        datazoom_opts=opts.DataZoomOpts(is_show=True),
    )
)

# #先取出数据量前10的，然后再对日期排序
data_sum_y=df_data2.groupby('TRANSACTION_DT').sum().sort_values('TRANSACTION_AMT',ascending=True)['TRANSACTION_AMT'].head(10).values.tolist()
data_personsum_y=df_data2.groupby('TRANSACTION_DT').size().sort_values(ascending=True).head(10).values.tolist()
data_sum_x=df_data2.groupby('TRANSACTION_DT').sum().sort_values('TRANSACTION_AMT',ascending=True).head(10).index.tolist()
data_personsum_x=df_data2.groupby('TRANSACTION_DT').size().sort_values(ascending=True).head(10).index.tolist()
ans=list(zip(data_sum_x,data_sum_y))
ans1=list(zip(data_personsum_x,data_personsum_y))
ans=sorted(ans,key=(lambda x:x[0]))
ans1=sorted(ans1,key=(lambda x:x[0]))
data_sum_x=[i[0] for i in ans]
data_personsum_x=[i[0] for i in ans1]
data_sum_y=[i[1] for i in ans]
data_personsum_y=[i[1] for i in ans1]
#
from pyecharts.charts import Line
line=(
    Line(init_opts=opts.InitOpts(width="1500px", height="380px",theme=ThemeType.CHALK))
    .add_xaxis(data_sum_x)
    .add_yaxis('data_personsum', y_axis=data_personsum_y,
               markline_opts=opts.MarkLineOpts(
                   data=[
                       opts.MarkLineItem(type_="average", name="平均值"),
                       opts.MarkLineItem(symbol="none", x="90%", y="max"),
                       opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                   ]
               ),
               )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(min_=13000),
        title_opts=opts.TitleOpts(title="过去某10天总捐款人数/总捐款数"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
)
line1=(
    Line(init_opts=opts.InitOpts(width="1500px", height="380px"))
    .add_xaxis(data_sum_x)
    .add_yaxis('data_sum',y_axis=data_sum_y,
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="average", name="平均值"),
                opts.MarkLineItem(symbol="none", x="90%", y="max"),
                opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
            ]
        ),
    )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(min_=1300000),
        # title_opts=opts.TitleOpts(title="过去某10天总捐款情况"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
)
from pyecharts.charts import Grid
page=(#page是最上层的图表不能嵌入到其他图表之中
    # Page()
    Grid(init_opts=opts.InitOpts(width="1900px", height="1000px",theme=ThemeType.CHALK))
    .add(line,grid_opts=opts.GridOpts(pos_bottom='55%'))
    .add(line1,grid_opts=opts.GridOpts(pos_top='55%'))
)
from pyecharts.charts import Tab
tab=(#似乎不能添加page表
    Tab()
    .add(word,'热点候选人物TOP25')
    .add(box_plot,'候选人获得的捐款情况')
    .add(grid_1,'总获得捐赠额和获得捐赠人数分析')
    .add(pie,'top人物拜登在各个州获得的捐赠占比')
    .add(Bar_YX,'候选党派票数')
    .add(p1,'各州的总捐赠数和总捐赠人数以及各州人均捐赠数额')
     .add(calendar,'一个月的捐赠分布情况')
    .add(river1,'一个月内总捐赠额top10的州捐赠流入情况')
    .add(river,'一个月内总捐赠额top10的职业捐赠流入情况')
    .add(page,'过去10天总捐款人数和捐款数')
)
tab.render('inok.html')
import webbrowser
webbrowser.open('inok.html')

#一般认为捐款的人数越多其捐款总数就会越大但是发现有两天人数与捐款数差距，所以我们具体分析这两天，并加入
#一般的一天作为对照组 2020803 2020808 +2020725  由分析各个属性最有可能就是捐赠人职业的影响
y11=df_data2[df_data2.TRANSACTION_DT=='2020803'].groupby('OCCUPATION').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).sort_values('OCCUPATION')['TRANSACTION_AMT'].values.tolist()
x11=df_data2[df_data2.TRANSACTION_DT=='2020803'].groupby('OCCUPATION').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).sort_values('OCCUPATION')['TRANSACTION_AMT'].index.tolist()
y11_person=df_data2[df_data2.TRANSACTION_DT=='2020803'].groupby('OCCUPATION').size()
sum_y11=sum(y11)

y11_bi=[round(i/sum_y11*100/y11_person[x11[j]],4) for j,i in enumerate(y11)]#每个职业在总金额的占比

y12=df_data2[df_data2.TRANSACTION_DT=='2020808'].groupby('OCCUPATION').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).sort_values('OCCUPATION')['TRANSACTION_AMT'].values.tolist()
x12=df_data2[df_data2.TRANSACTION_DT=='2020808'].groupby('OCCUPATION').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).sort_values('OCCUPATION')['TRANSACTION_AMT'].index.tolist()
y12_person=df_data2[df_data2.TRANSACTION_DT=='2020808'].groupby('OCCUPATION').size()
sum_y12=sum(y12)
y12_bi=[round(i/sum_y12*100/y12_person[x12[j]],4) for j,i in enumerate(y12)]

y13=df_data2[df_data2.TRANSACTION_DT=='2020725'].groupby('OCCUPATION').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).sort_values('OCCUPATION')['TRANSACTION_AMT'].values.tolist()
x13=df_data2[df_data2.TRANSACTION_DT=='2020725'].groupby('OCCUPATION').sum().sort_values('TRANSACTION_AMT',ascending=False).head(10).sort_values('OCCUPATION')['TRANSACTION_AMT'].index.tolist()
y13_person=df_data2[df_data2.TRANSACTION_DT=='2020725'].groupby('OCCUPATION').size()
sum_y13=sum(y13)
y13_bi=[round(i/sum_y13*100/y13_person[x13[j]],4) for j,i in enumerate(y13)]

# 做柱形图
l11=(
    Bar(init_opts=opts.InitOpts(width="1900px", height="400px",theme=ThemeType.DARK))
    .add_xaxis(x11)
    .add_yaxis('data_personsum', y_axis=y11,bar_width='50%',
itemstyle_opts=opts.ItemStyleOpts(color='blue'),
               markline_opts=opts.MarkLineOpts(
                   data=[
                       opts.MarkLineItem(type_="average", name="平均值"),
                       opts.MarkLineItem(symbol="none", x="90%", y="max"),
                       opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                   ]
               ),
               )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2020-08-03职业总捐款TOP10"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(
            rotate=40)),
    )
)
l21=(
    Bar(init_opts=opts.InitOpts(width="1900px", height="400px",theme=ThemeType.DARK))
    .add_xaxis(x12)
    .add_yaxis('data_personsum', y_axis=y12,bar_width='50%',
itemstyle_opts=opts.ItemStyleOpts(color='red'),
               markline_opts=opts.MarkLineOpts(
                   data=[
                       opts.MarkLineItem(type_="average", name="平均值"),
                       opts.MarkLineItem(symbol="none", x="90%", y="max"),
                       opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                   ]
               ),
               )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2020-08-08职业总捐款TOP10"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(
            rotate=40)),
    )
)
l31=(
    Bar(init_opts=opts.InitOpts(width="1900px", height="400px",theme=ThemeType.DARK))
    .add_xaxis(x13)
    .add_yaxis('data_personsum', y_axis=y13,bar_width='50%',
itemstyle_opts=opts.ItemStyleOpts(color='green'),
               # yaxis=opts.AxisOpts(min_=1300000),
               markline_opts=opts.MarkLineOpts(
                   data=[
                       opts.MarkLineItem(type_="average", name="平均值"),
                       opts.MarkLineItem(symbol="none", x="90%", y="max"),
                       opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                   ]
               ),
               )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2020-07-25职业总捐款TOP10"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(
            rotate=40)),
    )
)
#做折线图
l1=(
    Line(init_opts=opts.InitOpts(width="1900px", height="400px",theme=ThemeType.DARK))
    .add_xaxis(x11)
    .add_yaxis('data_personsum', y_axis=y11_bi,
               itemstyle_opts=opts.ItemStyleOpts(color='blue'),
               markline_opts=opts.MarkLineOpts(
                   data=[
                       opts.MarkLineItem(type_="average", name="平均值"),
                       opts.MarkLineItem(symbol="none", x="90%", y="max"),
                       opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                   ]
               ),
               )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2020-08-03总捐款TOP10职业个人占比"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(
            rotate=40)),
    )
)
l2=(
    Line(init_opts=opts.InitOpts(width="1900px", height="400px",theme=ThemeType.DARK))
    .add_xaxis(x12)
    .add_yaxis('data_personsum', y_axis=y12_bi,
    itemstyle_opts=opts.ItemStyleOpts(color='red'),
               markline_opts=opts.MarkLineOpts(
                   data=[
                       opts.MarkLineItem(type_="average", name="平均值"),
                       opts.MarkLineItem(symbol="none", x="90%", y="max"),
                       opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                   ]
               ),
               )
    .set_global_opts(
# yaxis_opts=opts.AxisOpts(max_=1.5),
        title_opts=opts.TitleOpts(title="2020-08-08总捐款TOP10职业个人占比"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(
            rotate=40)),
    )
)
l3=(
    Line(init_opts=opts.InitOpts(width="1900px", height="400px",theme=ThemeType.DARK))
    .add_xaxis(x13)
    .add_yaxis('data_personsum', y_axis=y13_bi,
                itemstyle_opts=opts.ItemStyleOpts(color='green'),
               # yaxis=opts.AxisOpts(min_=1300000),
               markline_opts=opts.MarkLineOpts(
                   data=[
                       opts.MarkLineItem(type_="average", name="平均值"),
                       opts.MarkLineItem(symbol="none", x="90%", y="max"),
                       opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                   ]
               ),
               )
    .set_global_opts(
# yaxis_opts=opts.AxisOpts(max_=1.5),
        title_opts=opts.TitleOpts(title="2020-07-25总捐款TOP10职业个人占比"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(
            rotate=40)),
    )
)

from pyecharts.charts import Page
page1=(
    Page()
    .add(l1,l2,l3)
)
page2=(
    Page()
    .add(l11,l21,l31)
)
page2.render('page1.html')
page1.render('page.html')

# from pyecharts.charts import Tab
# end1=(
#     Tab()
#     .add(word,'热点人物分析')
#     .add(pie,'top人物拜登在各个州获得的捐赠占比')
#     .add(p1,'各州的总捐赠数和总捐赠人数')
#     .add(page,'过去10天总捐款人数和捐款数')
#     # .add(page2,'实验探索')
#     # .add(page1,'每个职业个体捐款额占当天的比率')
# )
import webbrowser
webbrowser.open('page1.html')
webbrowser.open('page.html')




# page1.render('h.html')
# import webbrowser
# webbrowser.open('h.html')
# print(y11)
# print(y12)
# print(y13)
#如果从总金额判断，这三天实际职业差距不是特别大,所以想到了用个人占比来做判断


