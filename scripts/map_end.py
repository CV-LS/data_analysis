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

city_provice={}#城市的provice
provice_city={}#provice中的城市
stations = []
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36 2345Explorer/10.11.0.20694'}
#
jinwei = {}  # 用于存放各大城市的主要经纬度

def get_jinwei(station_city):
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
                name = j.xpath('./strong/a/text()')[0]
                url_end = 'https://www.d1xz.net/' + res_end[0]
                ans_1 = requests.get(url=url_end, headers=headers)
                end_1 = ans_1.text
                Html_1 = etree.HTML(end_1)
                res_1 = Html_1.xpath('//div[@class="inner_con_art"]/table//tr')
                for num_ in range(2, len(res_1)):
                    end_end = Html_1.xpath('//div[@class="inner_con_art"]/table//tr[' + str(num_) + ']/td/text()')
                    if end_end[0] in station_city:
                        provice_city.setdefault(name,[]).append(end_end[0])
                        city_provice.update({end_end[0]:name})
                    jinwei.update({end_end[0]: [end_end[1], end_end[2]]})
    city_provice.update({'香港':'香港'})
    provice_city.update({'香港':['香港']})
    jinwei.update({'香港': ['114.12', '22.26']})

city_ID = {}


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
        city_ID.update({name: ID})

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
def get_district(df_data):
    url1 = 'https://www.youbianku.com/SearchResults?address='
    # response=requests.get(url=url1,headers=headers)
    # response.enconding='utf-8'
    # print(response.text)
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    chrome_options = webdriver.ChromeOptions()
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=r'C:\Users\Dcnightmare\Desktop\chromedriver')
    list_city=[]
    last_text=''
    # driver.get(url='https://www.youbianku.com')
    for i in list(zip(df_data['站点城市'].values, df_data['地铁站点名称'])):
        driver.get(url=url1 + ''.join(list(i)))
        # driver.find_element_by_id('mySearchInput').send_keys(''.join(list(i)))
        # driver.find_element_by_id('mySearchButton').click()
        html_from_page = driver.page_source
        html = etree.HTML(html_from_page)
        try:
            text = html.xpath('//div[@class="mw-parser-output"]/div[1]//table//tr[2]/td/text()')[0]
            text = text.split('市')[1].split('区')[0] + '区'
        except Exception:
            driver.execute_script("window.stop()")
            list_city.append(last_text)
            continue
        if text=='区':
            list_city.append(last_text)
            continue
        last_text=text
        list_city.append(last_text)
    df_data['行政区']=list_city

if __name__ == '__main__':
    # with open('subway.csv', 'w+', encoding='utf-8') as f:
    #     f.write('站点城市'+','+'城市拼音名'+','+'POI编号'+','+'经度'+','+'纬度'+','+'路线名称'+','+'地铁站点名称'+'行政区'+'\n')
    #     f.close()
    # get_city()
    import pandas as pd
    df_data = pd.read_csv('subway_end.csv', sep=',')  # 使用pd的好处可以使用行和列名进行数据访问
    # get_district(df_data)#花费时间巨长不适合展示
    # print(df_data)
    city_qu = {}
    old_city = {}
    from selenium import webdriver
    from lxml import etree
    # print(df_data.路线名称)
    # print(df_data.shape)
    #     # 缺失值处理：

    # 得到其读取到的行
    # 得到所有的属性非空项
    # print(df_data.info())
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
    # # """查看城市的地铁站点数量"""pd.Series.nunique
    df_city_cnt = df_data_eda.groupby('站点城市').agg({'地铁站点名称': pd.Series.nunique}).reset_index().rename(
        columns={'地铁站点名称': 'city_count'})
    num_station_new = {}  # 得到站点城市的地铁站点数量
    number_sum = 0  # 用于统计总的站点数量
    # station_2020 = pd.read_csv('地铁站点数据.csv', sep='\t')
    num_station_check = {}  # 用于检查多余情况
    #     # 法一
    #     # for i in df_data_3.iloc[:,[0,6]].values:#不过访问时还是使用的其数据内容
    #     #     print(i)
    #     # 法二
    num_station_old = {}
    num_city_new={}
    cnt=0
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
            num_city_new.setdefault(i, []).append(df_data_3['行政区'][cnt])
            if num_station_new.get(i) == None:
                num_station_new[i] = 1
            else:
                num_station_new[i] += 1
            num_station_check[p] = 1
        cnt+=1
    num_station_new = dict(sorted(num_station_new.items(), key=lambda x: x[1], reverse=True))
    num_station_old = dict(sorted(num_station_old.items(), key=lambda x: x[1], reverse=True))

    #总体中国地铁分布地图
    from pyecharts import options as opts
    from pyecharts.globals import ChartType
    data_yy=list(num_station_new.values())
    data_xx=list(num_station_new.keys())
    print(data_xx)
    get_jinwei(data_xx)
    data=num_station_new
    provice={}
    for i in data_xx:
        provice.setdefault(city_provice[i],0)
        provice[city_provice[i]]+=data[i]
    from pyecharts import options as opts
    from pyecharts.charts import Map
    china_map = (
        Map(init_opts=opts.InitOpts(width="1530px", height="684px",theme=ThemeType.CHALK))
            .add("中国地铁", [list(z) for z in provice.items()], "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国地铁数据"),
            visualmap_opts=opts.VisualMapOpts(max_=max(provice.values()), is_piecewise=True,textstyle_opts=opts.TextStyleOpts(color='write',font_size=20,font_family='Microsoft YaHei')),
        )
    )
    # import webbrowser
    # webbrowser.open('geo_base.html')



    # 使用pyechart实现直方图数据分析
    from pyecharts.charts import Bar
    from pyecharts import options as opts
    import pandas as pd

    attr = list(num_station_new.keys())

    v1 = list(num_station_new.values())  # 新2021站点数据，主要体现数据处理
    v2 = list(num_station_old.values())  # 旧2021站点数据

    # att = []  # 2020站点数据
    # keys = list(station_2020.index)
    # values = station_2020.values
    # for i in num_station_new.keys():
    #     if i in keys:
    #         att.append(values[keys.index(i)][0])
    #     else:
    #         att.append(0)

    v1_v2 = []  # 用于得到换乘站点占比，  主要体现数据分析
    # 解释：换乘占比越大其地铁线路越是密集，其地铁相对城市的规模也比较大，因为前期地铁是以向外拓宽为核心，一般都会尽量避免出现换乘站点，导致其资源浪费
    # 当然也不是绝对的，可能有所偏差，但是大方向是对的
    for i in range(0, len(v1)):
        v1_v2.append(round((v2[i] - v1[i]) / v1[i], 3))  # round用于保留数据的位数
    # print(('%.2f' %12.234456))#使用两个%也可以达到格式化数据的目的
#在数量规模不大的时候其换乘站点占比就很高,当地的发展不平衡
    #换乘站点侧面反映了城市的地铁的规模和经济发展水平
    #一般只有规模比较大了之后才会考虑将线路连通,因为修建地铁的费用很高
    #查看地图和地铁线路,确实青岛有存在地区发展不平衡的问题,不过每个城市都有但是青岛,南昌更突出一些,当然也可能是因为当地主要经济在哪
#把居民区（郊区）和商业区（市中心）以及火车站、机场等连接起来，（比如一个城市1、2号线的交汇处都是商业中心，繁华地段）而且尽量规划一条主方向
    # ，不绕路，再把市区线适当地延长到郊县，再有就是客流走向了,客流预测。
    #要考虑到地质结构，太容易塌陷的地方或者地震断裂带肯定不行
    bar1 = (
        Bar(init_opts=opts.InitOpts(width="1530px", height="684px", theme=ThemeType.CHALK))  # 注意添加默认参数时是在init_opts参数中设置
            .add_xaxis(attr)
            # 通过对2020和2021处理前的数据比较还是可以发现一些数据错误（最主要的就是变少的情况），这时就直接去网上单独找答案
            # .add_yaxis('station_number_2020', att, itemstyle_opts=opts.ItemStyleOpts(color='red'),
            #            label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}",
            #                                      color='red'))  # 显示数据标签
            .add_yaxis('station_number_2021_new', v1, itemstyle_opts=opts.ItemStyleOpts(color='blue'),
                       label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}",
                                                 color='Magenta4'))  # 显示数据标签
            .add_yaxis('station_number_2021_old', v2, itemstyle_opts=opts.ItemStyleOpts(color='green'),
                       label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}",
                                                 color='yellow'))  # 显示数据标签
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
            visualmap_opts=opts.VisualMapOpts(is_show=True, max_=540, min_=0,is_piecewise=True,textstyle_opts=opts.TextStyleOpts(color='write',font_size=15,font_family='Microsoft YaHei')),
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
                subtitle="数量/占比",  # 副标题
                pos_left='6%'),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
    )
    #     #使用pyecharts完成经纬度图像的绘制
    #     #体现对数据描述


    from pyecharts.charts import BMap
    from pyecharts.globals import BMapType, ChartType
    js = "window.open('{}','_blank');"
    def show_city(bro,city):#city使用字典型
        from pyecharts.globals import SymbolType, ThemeType
        from pyecharts import options as opts
        global num_station_new,jinwei,num_city_new,df_data_3
        station = []  # 每条路线初始化为空
        stations = []  # 城市初始化为空
        center_x=0
        center_y=0
        station_point=[]
        for i in city[1]:
            data_ = df_data_3[df_data_3.站点城市 == i].values  # 开始先对每条线路排了序
            center_x+=float(jinwei[i][0])
            center_y+=float(jinwei[i][1])
            for num, j in enumerate(data_):  # columns属性得到的迭代对象是列属性名 类似于字典中的keys,indexs得到的是行属性名一般是序号
                station.append([j[4], j[5], j[6]])
                station_point.append([j[4], j[5], j[6]])
                if num == len(data_) - 1 or data_[num + 1][6] != data_[num][6]:
                    stations.append(station)
                    station = []
        center_x/=len(city[1])
        center_y/=len(city[1])
        if len(city[1])!=1:
            Zoom=8
        else:
            Zoom=10
        map_b = (  # 不要异想天开认为可以将其拆开 然后每一条线赋值从而达到可以使用不同颜色添加不同的类型图的目的
            BMap(init_opts=opts.InitOpts(width="1500px", height="800px",theme=ThemeType.MACARONS))
                .add_schema(
                baidu_ak='ybGicIBt9c56brfI4alusbE8SfclQcjW',  # 百度地图开发应用appkey
                center=[center_x,center_y],  # 当前视角的中心点
                zoom=Zoom,  # 当前视角的缩放比例
                is_roam=True,  # 开启鼠标缩放和平移漫游
            )
                .add(
                series_name=city[0]+'地铁',
                type_=ChartType.LINES,  # 设置Geo图类型,(pyecharts库中负责地理坐标系的模块是Geo)
                # 如果是默认的 则为点型有参数symbol_size用于设置点的大小
                # data_pair=stations,  # 数据i项
                data_pair=stations,
                is_polyline=True,  # 是否是多段线，在画lines图情况下#
                linestyle_opts=opts.LineStyleOpts(color="blue", opacity=0.5, width=1.5),  # 线样式配置项
                effect_opts=opts.EffectOpts(
                    symbol=SymbolType.ROUND_RECT, symbol_size=3, color="red"
                )
            )
                .set_global_opts(title_opts=opts.TitleOpts(title=city[0]+"的地铁线路"),
                                 tooltip_opts=opts.TooltipOpts(is_show=True))
                .add_control_panel(
                maptype_control_opts=opts.BMapTypeControlOpts(type_=BMapType.MAPTYPE_CONTROL_HORIZONTAL),  # 切换地图类型的控件
                scale_control_opts=opts.BMapScaleControlOpts(),  # 比例尺控件
                overview_map_opts=opts.BMapOverviewMapControlOpts(is_open=True),  # 添加缩略地图
                navigation_control_opts=opts.BMapNavigationControlOpts()  # 地图的平移缩放控件
            )
                # .add_coordinate_json(json_file='json.json')
                .set_series_opts(effect_opts=opts.EffectOpts(is_show=True, color='red'))
                .render(city[0]+'地铁线路图.html')
        )
        # print('ok1')
        # # map_b.render(city[0]+'.html')
        # # bro.execute_script(js.format(city[0]+'.html'))

        data_yy = list(num_station_new.values())
        data = num_station_new
        station_sum = 0
        df_x=[]
        df_y=[]
        from collections import Counter
        for i in city[1]:
            station_sum += data[i]
            count = dict(Counter(num_city_new[i]))
            df_x+=list(count.keys())
            df_y+=list(count.values())
        data_xy=tuple(zip(df_x,df_y))
        data_xy=sorted(data_xy,key=lambda x:x[1],reverse=True)
        data_xy=dict(data_xy)

        from pyecharts import options as opts
        from pyecharts.charts import Map
        #每个城市单独的分布地图
        if len(city[1])!=1:
            df_city_x=[i+'市' for i in city[1]]
            df_city_y = [num_station_new[i] for i in city[1]]
            show_city = (
                    Map(init_opts=opts.InitOpts(width="1700px", height="760px",theme=ThemeType.CHALK))
                    .add(city[0], [list(z) for z in zip(df_city_x,df_city_y)],maptype=city[0])
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title=city[0]+"地铁数据",title_textstyle_opts=opts.TextStyleOpts(font_size=20)),
                visualmap_opts=opts.VisualMapOpts(max_=max(df_city_y),is_piecewise=True,range_color=["lightskyblue", "yellow", "orangered"], range_text=["High", "Low"],textstyle_opts=opts.TextStyleOpts(color='write', font_size=20,
                                                                                        font_family='Microsoft YaHei'))
                    ,legend_opts=opts.LegendOpts(is_show=False)
                )
            )
            show_pie=(
                Pie(init_opts=opts.InitOpts(width="200px", height="200px",theme=ThemeType.DARK))
                    .add(
                    city[0]+"各城市地铁占比",
                    data_pair=[list(i) for i in zip(df_city_x,df_city_y)],
                    radius=["20%", "30%"],
                    center=[1200, 450],
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
                                "borderColor": "blue",
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
                 .set_global_opts(legend_opts=opts.LegendOpts(is_show=True))
              )
        else:
            show_city = (
                Map(init_opts=opts.InitOpts(width="1700px", height="760px", theme=ThemeType.DARK))
                    .add(city[0], [list(z) for z in zip(df_x, df_y)], maptype=city[0])
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title=city[0]+"地铁数据"),
                    visualmap_opts=opts.VisualMapOpts(max_=max(df_y), is_piecewise=True,range_color=["lightskyblue", "yellow", "orangered"], range_text=["High", "Low"],
                                                      textstyle_opts=opts.TextStyleOpts(color='write', font_size=20,
                                                                                        font_family='Microsoft YaHei'))
                    , legend_opts=opts.LegendOpts(is_show=False)
                )
            )
            data_pie_y=[round(i / sum(df_y)*100, 2) for i in df_y]
            show_pie = (
                Pie(init_opts=opts.InitOpts(width="1530px", height="684px",theme=ThemeType.CHALK))
                    .add(
                    city[0] + "各区地铁占比",
                    data_pair=[list(i) for i in zip(df_x, df_y)],
                    radius=["40%", "60%"],
                    center=[1200, 450],
                    label_opts=opts.LabelOpts(
                       is_show=True, position="inside",color='black'
                    ),
                )
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),title_opts=opts.TitleOpts(title=city[0]+"各区地铁站点占比",pos_top='top',pos_right='10%',title_textstyle_opts=opts.TextStyleOpts(color='purple')))
            .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            # label_opts=opts.LabelOpts(formatter="{b}: {c}")
        )
        )
        from pyecharts import options as opts
        from pyecharts.charts import Liquid
        from pyecharts.commons.utils import JsCode
        liquid = (
                Liquid(init_opts=opts.InitOpts(width="200px", height="200px",theme=ThemeType.CHALK))
                .add(city[0]+'占比',[round(station_sum/sum(data_yy),4),1-round(station_sum/sum(data_yy),4)],center=[1200,450],shape=SymbolType.ARROW,label_opts=opts.LabelOpts(
                font_size=40,
                formatter=JsCode(
                    """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
                ),
                position="inside",
            ),
        )
                .set_global_opts(title_opts=opts.TitleOpts(title=city[0]+"地铁站点在全国占比",pos_top='top',pos_right='10%',title_textstyle_opts=opts.TextStyleOpts(color='purple')))
        )
        from pyecharts import options as opts
        from pyecharts.charts import Funnel
        if len(df_y) > 15:
            copy_y = list(data_xy.values())[:15]
            copy_x = list(data_xy.keys())[:15]
        else:
            copy_y = list(data_xy.values())
            copy_x = list(data_xy.keys())
        loudou = (
            Funnel(init_opts=opts.InitOpts(width="1530px", height="684px", theme=ThemeType.CHALK))
                .add(
                city[0] + "地铁",
                [list(z) for z in zip(copy_x, copy_y)],
                label_opts=opts.LabelOpts(position="inside"),
            )
                .set_global_opts(legend_opts=opts.LegendOpts(is_show=True),
                                 visualmap_opts=opts.VisualMapOpts(is_show=True, type_='color', max_=max(df_y),is_piecewise=True,textstyle_opts=opts.TextStyleOpts(color='write',font_size=15,font_family='Microsoft YaHei')),
                                 title_opts=opts.TitleOpts(title=city[0]+'地铁分析',title_textstyle_opts=opts.TextStyleOpts(font_size=20)))
        )
        from pyecharts.charts import Bar
        show_bar=(
            Bar(init_opts=opts.InitOpts(width="1700px", height="760px", theme=ThemeType.CHALK))  # 注意添加默认参数时是在init_opts参数中设置
                .add_xaxis(copy_x)
                .add_yaxis('2021'+city[0]+'地铁分布', copy_y, itemstyle_opts=opts.ItemStyleOpts(color='blue'),
                           label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}",
                                                     color='Magenta4'))  # 显示数据标签
                .set_global_opts(  # 对x轴标签，y轴，标题，图例的格式和类型进行修改
                # datazoom_opts=opts.DataZoomOpts(is_show=True),
                visualmap_opts=opts.VisualMapOpts(is_show=True, type_='color', max_=max(df_y),is_piecewise=True,textstyle_opts=opts.TextStyleOpts(color='write',font_size=15,font_family='Microsoft YaHei')),
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
                    title=city[0]+"地铁站点数量",  # 标题
                    title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 主标题字体大小
                    ),
            )
        )
        from pyecharts.charts import Grid
        from pyecharts.globals import SymbolType, ThemeType
        grid1 = (
            Grid(init_opts=opts.InitOpts(width="1530px", height="684px", theme=ThemeType.CHALK))
                .add(show_city, grid_opts=opts.GridOpts(pos_bottom='50%', pos_right='left'))
                .add(show_pie, grid_opts=opts.GridOpts(pos_bottom='50%', pos_left='55%'))
            # .add(liquid, grid_opts=opts.GridOpts(pos_top='60%', pos_right='50%',width='100px',height='100px'))
        )
        grid2=(
            Grid(init_opts=opts.InitOpts(width="1530px", height="684px", theme=ThemeType.CHALK))
                .add(show_bar, grid_opts=opts.GridOpts(pos_right='55%'))
                # .add(loudou,grid_opts=opts.GridOpts(pos_left='80%'))
                .add(liquid,grid_opts=opts.GridOpts())
        )
        # print('ok5')
        from pyecharts.charts import Tab
        show_tab=(
            Tab()
            .add(grid2, city[0]+'地铁数量情况')
            .add(loudou,city[0]+'地铁(<=15)')
            .add(grid1, city[0]+'地铁分布情况')
        )
        show_tab.render(city[0] + '.html')
        bro.execute_script(js.format(city[0] + '.html'))
        bro.execute_script(js.format(city[0]+'地铁线路图' + '.html'))
        bro.switch_to.window(bro.window_handles[0])

    #     # 各城市的地铁站占比饼状图
    station_proportion = []
    for i in num_station_new.values():
        # "%.2f%%" % (c * 100)#用于将据转化为百分数形式的数据,但是实际上结果为str类型,不如直接使用round保留2位后*100再转化位字符加上'%'
        # station_proportion.append(("%.2f%%" %(i/number_sum*100)))
        station_proportion.append(("%.2f" % (i / number_sum * 100)))
    from pyecharts.charts import Pie
    import pyecharts.options as opts

    data_pie = tuple(zip(num_station_new.keys(), station_proportion))
    color=['DarkSlateBlue','CadetBlue4','SpringGreen4','CornflowerBlue']
    # colors=[color[i%len(color)] for i in range(len(num_station_new))]
    pie = (
        Pie(init_opts=opts.InitOpts(width="1530px", height="684px", theme=ThemeType.CHALK))
            .set_colors(color)
            .add(series_name='城市地铁站点占比', data_pair=data_pie, center=[750, 320]
                 , tooltip_opts=opts.TooltipOpts(is_show=True), radius=None,
                 label_opts=opts.LabelOpts(
                     distance=30, is_show=True,
                     position="outside",
                     formatter="{b}:{c}%",
                 )
                 )
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),title_opts=opts.TitleOpts(title='城市地铁站点占比',title_textstyle_opts=opts.TextStyleOpts(font_size=20,color='blue')))

        # ,rosetype='radius'
        # ,rosetype='area'
    )
    #
    # #
    # #     """查看每个城市的地铁线路个数"""    # df_metro = df_data_eda[df_data_eda['换乘站点'] == 1].groupby('站点城市')
    # #     # df_metro_cnt = df_data_eda.groupby('站点城市').agg({'路线名称': pd.Series.nunique}).reset_index().rename(
    # #     #     columns={'路线名称': 'road_cnt'})
    # #     # df_data_bj = df_data_eda[df_data_eda['站点城市'] == '北京']
    # #     #
    # #     # print(df_metro_cnt.sample(5))
    # #     # for i in df_data_eda:
    # #     #     df_data_eda[i]=str(i.size())
    # #     # print(df_data_eda)
    # #     # df_city_cnt.sample(5)
    #
    # # 地铁在各大城市的分布情况（从中国地图来看）
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
    #发现大多数地铁城市都是沿海,查询资料发现地铁修建需要一些条件,包括人口和经济水平(主要是GDP).而众所周知沿海城市的经济发展水平都不错
    c = (
        Map3D(init_opts=opts.InitOpts(width="1600px", height="700px", theme=ThemeType.CHALK))
            .add_schema(
                # center=['34.3227','108.5525'],
                itemstyle_opts=opts.ItemStyleOpts(
                color="rgb(5,101,123)",
                opacity=1,
                border_width=0.8,
                border_color="rgb(62,215,213)",
                # ground_color=''
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
            series_name="城市数据",
            bevel_smoothness=2,
            data_pair=example_data,
            type_=ChartType.BAR3D,
            bar_size=1,
            shading="lambert",
            label_opts=opts.LabelOpts(
                is_show=False,
                formatter=JsCode("function(data){return data.name + ' ' + data.value[2];}"),
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="中国地铁数据"), toolbox_opts=opts.ToolBoxFeatureDataViewOpts(
            is_show=True), tooltip_opts=opts.TooltipOpts(is_show=True, trigger_on='click', is_show_content=True),visualmap_opts=opts.VisualMapOpts(is_show=True,max_=max(num_station_new.values()),
                                                 is_piecewise=True , textstyle_opts=opts.TextStyleOpts(color='write',font_size=20,font_family='Microsoft YaHei')))
    )
    from pyecharts.charts import Tab
    tab1=(
        Tab()
        .add(bar1,'各城市地铁分布')
        .add(pie,'各城市地铁数量占比')
        .add(china_map,'各城市地铁在中国分布')
        .add(c,'3D展示')
    )
    tab1.render('china_city.html')

    #
    # data_china = [list(i) for i in num_station_new.items()]
    # from pyecharts import options as opts
    # from pyecharts.charts import Geo
    # from pyecharts.globals import ChartType
    # from pyecharts import options as opts
    # from pyecharts.charts import Map
    #
    # # G= (
    # #     Map()
    # #         .add("城市地铁数量",data_china, "china")
    # #         .set_global_opts(
    # #         title_opts=opts.TitleOpts(title="数量区分"),
    # #         visualmap_opts=opts.VisualMapOpts(max_=380, is_piecewise=True),
    # #     )
    # # )
    # # G = (
    # #     Geo(init_opts=opts.InitOpts(width="1900px", height="800px"))
    # #     .add_schema(maptype="china")
    # #     .add(
    # #         "城市地铁站点数量",
    # #         data_china,
    # #         type_=ChartType.EFFECT_SCATTER,
    # #     )
    # #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # #     .set_global_opts(title_opts=opts.TitleOpts(title="中国城市地铁分布",title_textstyle_opts=opts.TextStyleOpts(font_size=35)),visualmap_opts=opts.VisualMapOpts(max_=380),legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=20)),toolbox_opts=opts.ToolboxOpts(is_show=True))
    # # )
    # # G.render('subways.html')
    # # import webbrowser
    # # webbrowser.open('subways.html')
    # # from pyecharts import options as opts
    # # from pyecharts.charts import BMap
    # # from pyecharts.faker import Faker
    # #
    # # c = (
    # #     BMap()
    # #         .add_schema(baidu_ak="ybGicIBt9c56brfI4alusbE8SfclQcjW", center=[120.13066322374, 30.240018034923])
    # #         .add(
    # #         "bmap",
    # #         [list(z) for z in zip(Faker.provinces, Faker.values())],
    # #         label_opts=opts.LabelOpts(formatter="{b}"),
    # #     )
    # #         .set_global_opts(title_opts=opts.TitleOpts(title="BMap-基本示例"))
    # #         .render("bmap_base.html")
    # # )
    # # import webbrowser
    # # webbrowser.open('bmap_base.html')
    # from pyecharts.charts import Tab
    #
    # # tab=(
    # #     Tab()
    # #     .add(bar1,'城市地铁站点数量分析即换乘站点占比')
    # #     .add(pie,'站点数量占比—饼图分析')
    # #     # .add(c,'城市地铁在中国地区的分布')
    # # )
    # # tab.render('end_subways.html')
    # # import webbrowser
    # # webbrowser.open('end_subways.html')

    flag = 2
    start_time=0
    import tkinter as tk
    from tkinter import *
    def set(a):
        global flag
        flag = a
    def select():
        global flag,start_time
        win=tk.Tk()
        win.geometry('100x100')
        but1 = Button(win,activeforeground='blue', relief=tk.SOLID, highlightthickness=0, borderwidth=0, padx=0, pady=0,
                      # 修改这里查看按钮边缘大小
                      compound='center', font='Simhei 15 bold',  # 修改字体和大小
                      text='省视图', command=lambda :set(1))
        but2 = Button(win,activeforeground='blue', relief=tk.SOLID, highlightthickness=0, borderwidth=0, padx=0, pady=0,
                      # 修改这里查看按钮边缘大小
                      compound='center', font='Simhei 15 bold',  # 修改字体和大小
                      text='市视图', command=lambda :set(2))
        but1.place(x=0,y=25)
        but2.place(x=50,y=25)
        while int(time.time()-start_time)<5:
            win.mainloop()
        # time.sleep(5)
    from selenium import webdriver
    # 实例化一个浏览器对象（传入浏览器的驱动成）
    bro = webdriver.Chrome(executable_path=r'C:\Users\Dcnightmare\Desktop\chromedriver')
    # 让浏览器发起一个指定url对应请求
    bro.get('file:///C:/Users/Dcnightmare/PycharmProjects/pythonProject2/data_analysis_1/china_city.html')
    # page_source获取浏览器当前页面的页面源码数据
    import time
    last_city=''#防止一直更新

    last_flag=1
    while True:
        page_text = bro.page_source
        tree = etree.HTML(page_text)
        # li_list = tree.xpath('//body/div[1]/div[2]/text()')
        li_list = tree.xpath('//body/div[2]/div[4]/div[2]/text()')
        if len(list(li_list))!=0:
            city=li_list[1].split(':')[0]
            if last_city==city:
                continue
            last_city = city
            if len(provice_city[city_provice[city]])!=1:
                start_time = time.time()
                select()
            if flag==1:#对应省视图
                show_city(bro, [city_provice[city], provice_city[city_provice[city]]])
                flag=2#恢复到市的状态
            else:#对应市视图
                show_city(bro, [city, [city]])
        time.sleep(1)
