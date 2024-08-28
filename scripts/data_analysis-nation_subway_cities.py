# 用于解决中文乱码的请况


# e6b1f9e0417ceb7a4e6aa7c132a2607c


from pylab import mpl
from pyecharts.globals import SymbolType, ThemeType

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体：解决plot不能显示中文问题
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
import json
import time
import requests
from lxml import etree

# 有些是重复数据包括了重复站  原值为385
# 有些是错误数据

stations = []
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36 2345Explorer/10.11.0.20694'}
#
jinwei = {}  # 用于存放各大城市的主要经纬度
url = 'https://www.d1xz.net/xp/jingwei/'
time.sleep(1)
ans = requests.get(url=url, headers=headers)
end = ans.text
Html = etree.HTML(end)
res = Html.xpath('//div[@class="inner_con_art"]/table//tr')
for i in range(1, 5):
    res = Html.xpath('//div[@class="inner_con_art"]/table//tr[' + str(i) + ']/td')
    for j in res:
        res_end = j.xpath('./strong/a/@href')  # 紧接着之前的对象继续进行xpath操作
        # print(res_end)
        if len(res_end) != 0:
            url_end = 'https://www.d1xz.net/' + res_end[0]
            ans_1 = requests.get(url=url_end, headers=headers)
            end_1 = ans_1.text
            Html_1 = etree.HTML(end_1)
            res_1 = Html_1.xpath('//div[@class="inner_con_art"]/table//tr')
            for num_ in range(2, len(res_1)):
                end_end = Html_1.xpath('//div[@class="inner_con_art"]/table//tr[' + str(num_) + ']/td/text()')
                jinwei.update({end_end[0]: [end_end[1], end_end[2]]})
jinwei.update({'香港': ['114.12', '22.26']})

city_ID={}
def get_city():
    url = 'http://map.amap.com/subway/index.html?&1100'
    time.sleep(2)
    res = requests.get(url=url, headers=headers)
    res.raise_for_status()
    res.encoding = res.apparent_encoding
    html = res.text
    Html = etree.HTML(html)
    # 城市列表
    res1 = Html.xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/a')
    res2 = Html.xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/a')
    for i in res1:
        # 城市ID值
        ID = ''.join(i.xpath('.//@id'))  # 属性需要加上双斜杠
        # 城市拼音名
        cityname = ''.join(i.xpath('.//@cityname'))  # ./表示在当层目录下使用
        # 城市名
        name = ''.join(i.xpath('./text()'))
        get_message(ID, cityname, name)
        city_ID.update({name:ID})

    for i in res2:
        # 城市ID值
        ID = ''.join(i.xpath('.//@id'))
        # 城市拼音名
        cityname = ''.join(i.xpath('.//@cityname'))
        # 城市名
        name = ''.join(i.xpath('./text()'))
        # print(cityname)
        get_message(ID, cityname, name)


def get_message(ID, cityname, name):
    """
    地铁线路信息获取
    """
    url = 'http://map.amap.com/service/subway?_1555502190153&srhdata=' + ID + '_drw_' + cityname + '.json'
    # global end_list
    global stations
    # if end_list.get(cityname) == None:
    #     end_list[cityname] = []
    # end_list[cityname].setdefault([])
    response = requests.get(url=url, headers=headers)
    time.sleep(2)
    html = response.text
    # print(html)
    result = json.loads(html)
    for i in result['l']:
        for j in i['st']:
            # 判断是否含有地铁分线
            if len(i['la']) > 0:
                # print(name,cityname,j['sl'],j['poiid'], i['ln'] + '(' + i['la'] + ')', j['n'])
                with open('subway.csv', 'a+', encoding='utf-8') as f:
                    f.write(name + ',' + cityname + ',' + j['poiid'] + ',' + j['sl'] + ',' + i['ln'] + '(' + i[
                        'la'] + ')' + ',' + j['n'] + '\n')
                    f.close()
            else:
                # print(name,cityname,j['sl'],j['poiid'], i['ln'], j['n'])
                with open('subway.csv', 'a+', encoding='utf-8')as f:
                    f.write(
                        name + ',' + cityname + ',' + j['poiid'] + ',' + j['sl'] + ',' + i['ln'] + ',' + j['n'] + '\n')
                    f.close()
            # end_list[cityname].append(j['n'])
    print(name + '地铁站点爬取结束')
    f.close()


if __name__ == '__main__':
    # with open('subway.csv', 'w+', encoding='utf-8') as f:
    #     f.write('站点城市'+','+'城市拼音名'+','+'POI编号'+','+'经度'+','+'纬度'+','+'路线名称'+','+'地铁站点名称'+'\n')
    #     f.close()
    # get_city()
    import pandas as pd

    df_data = pd.read_csv('subway.csv', sep=',').sort_values(['城市拼音名', '路线名称'])  # 使用pd的好处可以使用行和列名进行数据访问
    city_qu = {}
    old_city = {}
    from selenium import webdriver
    from lxml import etree
    from time import sleep



    # print(df_data.路线名称)
    print(df_data.shape)
    #     # 缺失值处理：

    # 得到其读取到的行
    # 得到所有的属性非空项
    print(df_data.info())
    # 得出其中没有确实值的行

    # 重复数据处理
    # """删除完全重复的站点"""
    df_data_1 = df_data.drop_duplicates()  # 删除掉完全相同的行
    # 得到删除之后的行
    # print('删除之后的行:',df_data_1.shape)

    # '''形式上应该处理存在空的行'''
    df_data_2 = df_data_1.copy()
    # # 计算站点的换乘个数借助使用groupby排好序之后再使用count计算其中的重复数据，该重复数据就是其换乘站点数

    # groupby类比MySQL中的groupby
    df_address_cnt = df_data_2.groupby(['站点城市', '地铁站点名称']).agg({'城市拼音名': 'count'}).reset_index().rename(
        columns={'城市拼音名': '换乘站点'})  # columns属性（一行中的属性）  实际上对应的是列属性
    df_data_3 = df_data_2.merge(df_address_cnt, on=['站点城市', '地铁站点名称'], how='left')
    df_data_eda = df_data_3.copy()
    # """查看城市的地铁站点数量"""pd.Series.nunique
    df_city_cnt = df_data_eda.groupby('站点城市').agg({'地铁站点名称': pd.Series.nunique}).reset_index().rename(
        columns={'地铁站点名称': 'city_count'})
    num_station_new = {}  # 得到站点城市的地铁站点数量
    number_sum = 0  # 用于统计总的站点数量
    station_2020 = pd.read_csv('地铁站点数据.csv', sep='\t')
    num_station_check = {}  # 用于检查多余情况
    #     # 法一
    #     # for i in df_data_3.iloc[:,[0,6]].values:#不过访问时还是使用的其数据内容
    #     #     print(i)
    #     # 法二
    num_station_old = {}
    for p in zip(df_data_3['站点城市'], df_data_3['地铁站点名称']):
        (i, j) = p
        # 原始数据
        if num_station_old.get(i) == None:
            num_station_old[i] = 1
        else:
            num_station_old[i] += 1
        # 处理后的数据
        if num_station_check.get(p) == None:
            number_sum += 1
            if num_station_new.get(i) == None:
                num_station_new[i] = 1
            else:
                num_station_new[i] += 1
            num_station_check[p] = 1
    num_station_new = dict(sorted(num_station_new.items(), key=lambda x: x[1], reverse=True))
    num_station_old = dict(sorted(num_station_old.items(), key=lambda x: x[1], reverse=True))
    # 使用pyechart实现直方图数据分析
    from pyecharts.charts import Bar
    from pyecharts import options as opts
    import pandas as pd

    attr = list(num_station_new.keys())
    v1 = list(num_station_new.values())  # 新2021站点数据，主要体现数据处理
    v2 = list(num_station_old.values())  # 旧2021站点数据
    att = []  # 2020站点数据
    keys = list(station_2020.index)
    values = station_2020.values
    for i in num_station_new.keys():
        if i in keys:
            att.append(values[keys.index(i)][0])
        else:
            att.append(0)

    v1_v2 = []  # 用于得到换乘站点占比，  主要体现数据分析
    # 解释：换乘占比越大其地铁线路越是密集，其地铁相对城市的规模也比较大，因为前期地铁是以向外拓宽为核心，一般都会尽量避免出现换乘站点，导致其资源浪费
    # 当然也不是绝对的，可能有所偏差，但是大方向是对的
    for i in range(0, len(v1)):
        v1_v2.append(round((v2[i] - v1[i]) / v1[i], 3))  # round用于保留数据的位数
    # print(('%.2f' %12.234456))#使用两个%也可以达到格式化数据的目的

    bar1 = (
        Bar(init_opts=opts.InitOpts(width="1700px", height="800px", theme=ThemeType.CHALK))  # 注意添加默认参数时是在init_opts参数中设置
            .add_xaxis(attr)
            # 通过对2020和2021处理前的数据比较还是可以发现一些数据错误（最主要的就是变少的情况），这时就直接去网上单独找答案
            .add_yaxis('station_number_2020', att, itemstyle_opts=opts.ItemStyleOpts(color='red'),
                       label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}",
                                                 color='red'))  # 显示数据标签
            .add_yaxis('station_number_2021_new', v1, itemstyle_opts=opts.ItemStyleOpts(color='blue'),
                       label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}",
                                                 color='Magenta4'))  # 显示数据标签
            .add_yaxis('station_number_2021_old', v2, itemstyle_opts=opts.ItemStyleOpts(color='green'),
                       label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}",
                                                 color='blue'))  # 显示数据标签
            .add_yaxis('换乘站点占比', v1_v2, itemstyle_opts=opts.ItemStyleOpts(color='orange'),
                       label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}",
                                                 color='green'))  # 显示数据标签
            .extend_axis(  # 设置次坐标轴
            yaxis=opts.AxisOpts(  # 为什么不需要加上_opts
                name="换乘站点占比率",  # 次坐标轴名称
                type_="value",  # 次坐标手类型
                min_=0,  # 最小值
                max_=50,  # 最大值
                is_show=True,  # 是否显示
                axisline_opts=opts.AxisLineOpts(is_show=False,  # y轴线不显示
                                                linestyle_opts=opts.LineStyleOpts(color='#f6c065')),  # 设置线颜色, 字体颜色也变
                axistick_opts=opts.AxisTickOpts(is_show=False),  # 刻度线不显示
                axislabel_opts=opts.LabelOpts(formatter="{value}%"),  # 次坐标轴数据显示格式
            )
        )

            .set_global_opts(  # 对x轴标签，y轴，标题，图例的格式和类型进行修改
            # 图例默认放到 上中 位置
            datazoom_opts=opts.DataZoomOpts(is_show=True, is_realtime=True),
            visualmap_opts=opts.VisualMapOpts(is_show=True, type_='color', max_=400, min_=10),
            xaxis_opts=opts.AxisOpts(
                name='City',
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
    # "data": [
    #             "\u6570\u636e"
    #         ],
    #         "selected": {
    #             "\u6570\u636e": true
            ),
            yaxis_opts=opts.AxisOpts(
                name='station_number',
                name_location='middle',
                name_gap=30,
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
                splitline_opts=opts.SplitLineOpts(is_show=True),  # y轴网格线
                axisline_opts=opts.AxisLineOpts(is_show=False),  # y轴线
            ),
            title_opts=opts.TitleOpts(
                title="城市地铁站点数量",  # 标题
                title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 主标题字体大小
                subtitle="CV-LS",  # 副标题
                pos_left='6%'),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
    )
    #     #使用pyecharts完成经纬度图像的绘制
    #     #体现对数据描述
    from pyecharts.charts import BMap
    from pyecharts.globals import BMapType, ChartType
    from pyecharts import options as opts

    # for i in num_station_new.keys():#全部城市的数据
    station = []  # 每条路线初始化为空
    stations = []  # 城市初始化为空
    station_end = []
    check=[]
    for i in ['北京', '上海', '深圳', '广州', '徐州']:
        # print(df_data[df_data.站点城市 == '北京'])#是一个dataFrame的形式
        #     station=[]#每条路线初始化为空
        #     stations=[]#城市初始化为空
        data = df_data[df_data.站点城市 == i].values#开始先对每条线路排了序

        for num, j in enumerate(data):  # columns属性得到的迭代对象是列属性名 类似于字典中的keys,indexs得到的是行属性名一般是序号
            station.append([j[3],j[4],j[6]])
            # if j[6] not in check:
            #     station_end.append(([j[3], j[4]]))
            if num == len(data) - 1 or data[num + 1][5] != data[num][5]:
                stations.append(station)
                station = []
        # stations初始化完毕
        # 得到一个城市的station数据;
    # print(station_end)
    # with open('json.json', 'w+', encoding='utf-8') as fd:
    #     fd.write(str(station_end))
    map_b = (  # 不要异想天开认为可以将其拆开 然后每一条线赋值从而达到可以使用不同颜色添加不同的类型图的目的
        BMap(init_opts=opts.InitOpts(width="1900px", height="1000px"))
            .add_schema(
            baidu_ak='ybGicIBt9c56brfI4alusbE8SfclQcjW',  # 百度地图开发应用appkey
            center=[120.13066322374, 30.240018034923],  # 当前视角的中心点
            zoom=10,  # 当前视角的缩放比例
            is_roam=True,  # 开启鼠标缩放和平移漫游
        )
            .add(
            series_name='地铁线路',
            type_=ChartType.LINES,  # 设置Geo图类型,(pyecharts库中负责地理坐标系的模块是Geo)
            # 如果是默认的 则为点型有参数symbol_size用于设置点的大小
            # data_pair=stations,  # 数据i项
            data_pair=stations,
            is_polyline=True,  # 是否是多段线，在画lines图情况下#
            linestyle_opts=opts.LineStyleOpts(color="blue", opacity=0.5, width=1),  # 线样式配置项
            effect_opts=opts.EffectOpts(
                symbol=SymbolType.ROUND_RECT, symbol_size=3, color="blue"
            )
        )
        #     .add(
        #     series_name='地铁站点',
        #     data_pair=station_end,
        #     type_=ChartType.BAR3D,
        #     label_opts=opts.LabelOpts(formatter="{b}"),
        # )
            .set_global_opts(title_opts=opts.TitleOpts(title="BMap-基本示例"),tooltip_opts=opts.TooltipOpts(is_show=True,trigger= "item",trigger_on='click'))
            .add_control_panel(
            maptype_control_opts=opts.BMapTypeControlOpts(type_=BMapType.MAPTYPE_CONTROL_DROPDOWN),  # 切换地图类型的控件
            scale_control_opts=opts.BMapScaleControlOpts(),  # 比例尺控件
            overview_map_opts=opts.BMapOverviewMapControlOpts(is_open=True),  # 添加缩略地图
            navigation_control_opts=opts.BMapNavigationControlOpts()  # 地图的平移缩放控件
        )
            # .add_coordinate("测试点",stations)
            .set_series_opts(effect_opts=opts.EffectOpts(is_show=True, color='red'))
            # .add_coordinate("测试点", jinwei[i][0],jinwei[i][1])
            # .add('center_name',i)
            # .add_coordinate_json(json_file='json.json')
    )
    # for i in station_end.keys():
    #     map_b.add_coordinate(i,station_end[i][0],station_end[i][1])
    # map_b.add_coordinate_json(json_file='json.json')
    # path = 'subway_' + '.html'
    # map_b.render(path)
    # import webbrowser
    #
    # webbrowser.open(path)
    # print("各城市地铁流动图分析结束!")
    #
    #
    # 各城市的地铁站占比饼状图
    station_proportion = []
    for i in num_station_new.values():
        # "%.2f%%" % (c * 100)#用于将据转化为百分数形式的数据,但是实际上结果为str类型,不如直接使用round保留2位后*100再转化位字符加上'%'
        # station_proportion.append(("%.2f%%" %(i/number_sum*100)))
        station_proportion.append(("%.2f" % (i / number_sum * 100)))
    from pyecharts.charts import Pie
    import pyecharts.options as opts

    data_pie = tuple(zip(num_station_new.keys(), station_proportion))
    # print(data_pie)
    pie = (
        Pie(init_opts=opts.InitOpts(width="1900px", height="1000px", theme=ThemeType.CHALK))
            .add(series_name='城市地铁站点占比', data_pair=data_pie, center=[750, 500]
                 , tooltip_opts=opts.TooltipOpts(is_show=True), radius=None,
                 label_opts=opts.LabelOpts(
                     distance=30, is_show=True,
                     position="outside",
                     formatter="{b}:{c}%",
                 )
                 )
        # ,rosetype='radius'
        # ,rosetype='area'
    )

    #
    #     """查看每个城市的地铁线路个数"""    # df_metro = df_data_eda[df_data_eda['换乘站点'] == 1].groupby('站点城市')
    #     # df_metro_cnt = df_data_eda.groupby('站点城市').agg({'路线名称': pd.Series.nunique}).reset_index().rename(
    #     #     columns={'路线名称': 'road_cnt'})
    #     # df_data_bj = df_data_eda[df_data_eda['站点城市'] == '北京']
    #     #
    #     # print(df_metro_cnt.sample(5))
    #     # for i in df_data_eda:
    #     #     df_data_eda[i]=str(i.size())
    #     # print(df_data_eda)
    #     # df_city_cnt.sample(5)

    # 地铁在各大城市的分布情况（从中国地图来看）
    from pyecharts import options as opts
    from pyecharts.charts import Map3D
    from pyecharts.globals import ChartType
    from pyecharts.commons.utils import JsCode

    for i in num_station_new:
        jinwei[i].append(num_station_new[i])  # 添加城市的站点数量，也相当于加上高度
    example_data = [
        # (p,num_station_new[p]) for p in num_station_new.keys()]
        (p, jinwei[p]) for p in num_station_new.keys()]
    # example_data=num_station_new[i]
    from pyecharts.globals import SymbolType, ThemeType

    def f():
        print('ok')
    # class ToolBoxFeatureDataViewOpts(
    #     # 是否显示该工具。
    #     is_show= True
    # ):

    c = (
        Map3D(init_opts=opts.InitOpts(width="1900px", height="1000px", theme=ThemeType.DARK))
            .add_schema(
            itemstyle_opts=opts.ItemStyleOpts(
                color="rgb(5,101,123)",
                opacity=1,
                border_width=0.8,
                border_color="rgb(62,215,213)",
            ),
            map3d_label=opts.Map3DLabelOpts(
                is_show=False,
                formatter=JsCode("function(data){return data.name + " " + data.value[2];}"),
            ),
            emphasis_label_opts=opts.LabelOpts(
                is_show=False,
                color="#fff",
                font_size=10,
                background_color="rgba(0,23,11,0)",
            ),
            light_opts=opts.Map3DLightOpts(
                main_color="#fff",
                main_intensity=1.2,
                main_shadow_quality="high",
                is_main_shadow=False,
                main_beta=10,
                ambient_intensity=0.3,
            ),
        )
            .add(
            series_name="数据",
            data_pair=example_data,
            type_=ChartType.BAR3D,
            bar_size=1,
            shading="lambert",
            label_opts=opts.LabelOpts(
                is_show=False,
                formatter=JsCode("function(data){return data.name + ' ' + data.value[2];}"),
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="城市数据"),toolbox_opts=opts.ToolBoxFeatureDataViewOpts(
            is_show=True),tooltip_opts=opts.TooltipOpts(is_show=True,trigger_on='click',is_show_content=True))
    )
    # import webbrowser
    # c.render('china_city.html')
    # webbrowser.open('china_city.html')

    data_china=[list(i) for i in num_station_new.items()]
    from pyecharts import options as opts
    from pyecharts.charts import Geo
    from pyecharts.globals import ChartType
    from pyecharts import options as opts
    from pyecharts.charts import Map

    # G= (
    #     Map()
    #         .add("城市地铁数量",data_china, "china")
    #         .set_global_opts(
    #         title_opts=opts.TitleOpts(title="数量区分"),
    #         visualmap_opts=opts.VisualMapOpts(max_=380, is_piecewise=True),
    #     )
    # )
    # G = (
    #     Geo(init_opts=opts.InitOpts(width="1900px", height="800px"))
    #     .add_schema(maptype="china")
    #     .add(
    #         "城市地铁站点数量",
    #         data_china,
    #         type_=ChartType.EFFECT_SCATTER,
    #     )
    #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    #     .set_global_opts(title_opts=opts.TitleOpts(title="中国城市地铁分布",title_textstyle_opts=opts.TextStyleOpts(font_size=35)),visualmap_opts=opts.VisualMapOpts(max_=380),legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=20)),toolbox_opts=opts.ToolboxOpts(is_show=True))
    # )
    # G.render('subways.html')
    # import webbrowser
    # webbrowser.open('subways.html')
    # from pyecharts import options as opts
    # from pyecharts.charts import BMap
    # from pyecharts.faker import Faker
    #
    # c = (
    #     BMap()
    #         .add_schema(baidu_ak="ybGicIBt9c56brfI4alusbE8SfclQcjW", center=[120.13066322374, 30.240018034923])
    #         .add(
    #         "bmap",
    #         [list(z) for z in zip(Faker.provinces, Faker.values())],
    #         label_opts=opts.LabelOpts(formatter="{b}"),
    #     )
    #         .set_global_opts(title_opts=opts.TitleOpts(title="BMap-基本示例"))
    #         .render("bmap_base.html")
    # )
    # import webbrowser
    # webbrowser.open('bmap_base.html')
    from pyecharts.charts import Tab


    # tab=(
    #     Tab()
    #     .add(bar1,'城市地铁站点数量分析即换乘站点占比')
    #     .add(pie,'站点数量占比—饼图分析')
    #     # .add(c,'城市地铁在中国地区的分布')
    # )
    # tab.render('end_subways.html')
    # import webbrowser
    # webbrowser.open('end_subways.html')

    # from selenium import webdriver
    # # 实例化一个浏览器对象（传入浏览器的驱动成）
    # bro = webdriver.Chrome(executable_path=r'C:\Users\Dcnightmare\Desktop\chromedriver')
    # # 让浏览器发起一个指定url对应请求
    # bro.get('file:///C:/Users/Dcnightmare/PycharmProjects/pythonProject2/data_analysis_1/china_city.html')
    # # page_source获取浏览器当前页面的页面源码数据
    # import time
    # while True:
    #     page_text = bro.page_source
    #     tree = etree.HTML(page_text)
    #     li_list = tree.xpath('//body/div[1]/div[2]/text()')
    #     if len(list(li_list))!=0:
    #         print(li_list[1].split(':')[0])
    #     time.sleep(2)
