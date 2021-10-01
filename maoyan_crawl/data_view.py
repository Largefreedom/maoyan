
# coding=gbk
'''
    ����΢�Ź��ںţ�zeroing˵��    
      
'''

import datetime
import pymongo
import re
import numpy as np
import json
from pyecharts import options as opts
from pyecharts.charts import Geo,Bar,Pie,Line
from pyecharts.charts import Map
from pyecharts.globals import ChartType, SymbolType
import random
from highcharts import Highchart
'''
    ����MongoDB���ݿ���룻
'''

Client =pymongo.MongoClient('localhost',27017)
nezha =Client['maoyan']
item_info = nezha['nezha']

'''
        ����json�ļ�ȱʧ������
'''
def handle(cities):
    data =None
    with open('D:\python\Lib\site-packages\pyecharts\datasets\city_coordinates.json',mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())
    data_new =data.copy()
    for i in set(cities):
        if i =='':
            while i in cities:
                cities.remove(i)
        count = 0
        for k in data_new.keys():
            count += 1
            if k ==i:
                break
            if k.startswith(i):
                data_new[i] = data[k]
                break
            if k.startswith(i[-1:0]) and len(i) >=3:
                data_new[i] = data[k]
                break
        if count == len(data):
            while i in cities:
                cities.remove(i)
    with open('D:\python\Lib\site-packages\pyecharts\datasets\city_coordinates.json',mode='w', encoding='utf-8') as fa:
        fa.write(json.dumps(data_new, ensure_ascii=False))


city_list = []
for i in item_info.find():
    city_list.append(i['city'])
handle(city_list)
'''
        ���Ƶ�ͼ
'''
for i in set(city_list):
    a =[]
    a.append(i)
    a.append(city_list.count(i))
    z.append(a)
'''
        pyecharts�е�geoģ���ʹ�ã�����è����߸�����ֲ�
'''
geo = Geo(init_opts=opts.InitOpts(theme='vintage'))
geo.add_schema(maptype='china',)
geo.add('������Դè��ƽ̨',z,type_ =ChartType.EFFECT_SCATTER,symbol_size=10,color='gray')

geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
geo.set_global_opts(

            visualmap_opts=opts.VisualMapOpts(is_piecewise=True,max_=600),
            title_opts=opts.TitleOpts(title="����߸���������ѵ����ֲ�"),

        )
geo.render('geoheatmap.html')
'''
        Higchartsͼ��Ļ���ʹ�ã��������ѵ����ֲ���top20
'''
z0 =sorted(z,  key =lambda x:x[1],reverse=True)[:20]
print(z0)
random.shuffle(z0)
print(z0)
H =Highchart(width  = 900,highth = 800)
options = {

    'title': {
        'text': '����߸���������ѵ����ֲ�top20',

    },
    'subtitle': {
        'text': '������Դ��www.mmaoyan.com'
    },
    'xAxis': {
        'categories': [i[0] for i in z0],
        'labels': {
            'rotation': -45,
            'style': {
                'fontSize': '13px',
                'fontFamily': 'Verdana, sans-serif'
            }
        }
    },
    'yAxis': {
        'min': 0,
        'title': {
            'text': '�������������� (��)'
        }
    },

    'tooltip': {
        'pointFormat': '������˿��: <b>{point.y:.1f} ��</b>'
    },
'plotOptions': {
        'bar': {
            'dataLabels': {
                'enabled': True,

            'rotation': 0,
            'color': '#5E5E5E',
            'align': 'top',
            'format': '{point.y}',
            'style': {
                'fontSize': '8px',
                'fontFamily': 'Verdana, sans-serif'
            }
            }
        }

    },
# 'legend': {
#         'layout': 'vertical',
#         'align': 'right',
#         'verticalAlign': 'top',
#         'x': -40,
#         'y': 80,
#         'floating': True,
#         'borderWidth': 1,
#         'backgroundColor': "((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF')",
#         'shadow': True,

    # },
}
H.set_dict_options(options)
H.add_data_set(list([i[1] for i in z0]),'bar','���ѵ����ֲ�top20')
H.save_file('people_dirct')
'''
    **************************************************************************************
    ���۷�˿�Ա�ֲ����ӻ���
'''
'''
            ��MongoDB���ݿ�����ȡ���ݣ�����
'''
gender_list =[]
for i in item_info.find():
    if i['gender'] ==0:
        gender_list.append('�Ա�δ֪')
    elif i['gender'] == 1:
        gender_list.append('��')
    else:
        gender_list.append('Ů')

print(set(gender_list))
gender_lis = []
for i in set(gender_list):
    a = []
    a.append(i)
    a.append(gender_list.count(i))
    gender_lis.append(a)
print(gender_lis)

def pie_radius() -> Pie:
    c = (
        Pie()
        .add(
            "",
            gender_lis,
            radius=["50%", "75%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="����߸�����������Ա�ֲ�",subtitle='������Դ��www.maoyan,com',pos_left='40%'),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_top="15%", pos_left="2%"
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    c.render('gender_direct.html')
pie_radius()
'''
    ��߸����ʱ��ֲ���
'''

def change_to_second(str1):
    a = str(str1).split(':')
    seconds = int(a[0])
    return seconds
time_list0807 = []
for i in item_info.find():
    if re.split(' ',i['starttime'])[0] == '2019-08-07':
        hour = int(change_to_second(re.split(' ',i['starttime'])[1]))
        name = '{}-{}'.format(int(hour),int(hour)+1)
        time_list0807.append(name)
time_list0807_a =[]
for i in set(time_list0807):
    a = []
    a.append(i)
    b = time_list0807.count(i)
    a.append(b)
    time_list0807_a.append(a)
'''
    ������ϴ֮�󣺣�����������ʱ��ֲ�
'''
#
def line_areastyle_boundary_gap() -> Line:
    c = (
        Line()
        .add_xaxis(list(i[0] for i in list1))
        .add_yaxis("", list(i[1] for i in list1), is_smooth=True)

        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5,color='33AFFF'),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="����߸����������ʱ��ֲ�ͼ",pos_left='40%',
                                      subtitle='������Դ��www.maoyan.com'),
            xaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                is_scale=False,
                boundary_gap=False,
            ),
        )
    )
    c.render('date_dirct1.html')
    return c
line_areastyle_boundary_gap()

'''
        �ԡ���߸���������ֵĻ���������������ȣ����ַ�����
'''
socer_list = []
# a_list= []
# b_list =[]
# c_list =[]

a0_to1 =[]
a1_to2 =[]
a2_to3 =[]
a3_to4 =[]
a4_to5 =[]

for i in item_info.find():

    # if re.split(' ',i['starttime'])[0] == '2019-08-06':
    #     a_list.append(i['socre'])
    # elif re.split(' ',i['starttime'])[0] == '2019-08-07':
    #     b_list.append(i['socre'])
    # else:
    #     c_list.append(i['socre'])

    if int(i['socre']) < 1:
        a0_to1.append(i['socre'])
    elif int(i['socre']) < 2:
        a1_to2.append(i['socre'])
    elif int(i['socre']) < 3:
        a2_to3.append(i['socre'])
    elif int(i['socre']) < 4:
        a3_to4.append(i['socre'])
    else:
        a4_to5.append(i['socre'])
    socer_list.append(i['socre']*2)

socer_list_1 = []
socer_list_2 = []
for i in set(socer_list):
    a = []
    a.append(i)
    a.append(socer_list.count(i))
    socer_list_1.append(a)
socer_list_1 = sorted(socer_list_1,key =lambda x:x[0],reverse=False)
print(socer_list_1)

a0_to1_list = []
a0_to1_list.append('0��2��')
a0_to1_list.append(len(a0_to1))
print(set(socer_list))
print(a0_to1)
print(len(a0_to1))
a1_to2_list = []
a1_to2_list.append('2��4��')
a1_to2_list.append(len(a1_to2))
a2_to3_list = []
a2_to3_list.append('4��6��')
a2_to3_list.append(len(a2_to3))
print(a2_to3)
print(len(a2_to3))
print(a3_to4)
print(len(a3_to4))
a3_to4_list = []
a3_to4_list.append('6��8��')
a3_to4_list.append(len(a3_to4))
print(a4_to5)
print(len(a4_to5))
a4_to5_list = []
a4_to5_list.append('8��10��')
a4_to5_list.append(len(a4_to5))
socer_list_2.append(a0_to1_list)
socer_list_2.append(a1_to2_list)
socer_list_2.append(a2_to3_list)
socer_list_2.append(a3_to4_list)
socer_list_2.append(a4_to5_list)

def bar_is_selected() -> Bar:
    c = (
        Bar()
        .add_xaxis([i[0] for i in socer_list_1])
        .add_yaxis("�̼�A", [i[1] for i in socer_list_1])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-Ĭ��ȡ����ʾĳ Series"))
        .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5,color='blue')))
    c.render('socre_fenbu.html')


    return c
bar_is_selected()
def pie_radius() -> Pie:
    c = (
        Pie()
        .add(
            "",
            [i for i in socer_list_2],
            radius=["40%", "75%"],
        )
        .set_colors(["blue", "green", "orange",  "purple","red",])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="����߸���������ֲַ�",subtitle='������Դ��www.maoyan.com'),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_top="15%", pos_left="2%"
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    c.render('socre_list2.html')
    return c

pie_radius()




'''
        ��Ӱ06-08��������ͼ

'''
e_score_list =[]
a_list_06 = ['08-06',round(np.mean(a_list)*2,2)]
b_list_07 = ['08-07',round(np.mean(a_list)*2,2)]
c_list_08 = ['08-08',round(np.mean(a_list)*2,2)]
e_score_list.append(a_list_06)
e_score_list.append(b_list_07)
e_score_list.append(c_list_08)


def line_markpoint_custom() -> Line:
    x, y = [i[0] for i in e_score_list],[i[1] for i in e_score_list]
    c = (
        Line()
        .add_xaxis(x)
        .add_yaxis(
            "",
            y,
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(name="0219-08-07", coord=[x[1], y[1]], value=y[1])]
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="����߸����������ͼ��06-08��",pos_left='40%',subtitle='������Դ��www.maoyan.com'))
    )
    c.render('socre_trend.html')
    return c
line_markpoint_custom()
'''
   ��Ӱ�����浽�����ļ����У�Ϊ��������ͼ��׼����

'''
fil = open('C:/Users/FREEDOM/Desktop/aab.txt','a',encoding='gb18030')

for i in item_info.find():
    fil.write(i['contend'])
    fil.write('\n')


fil.close()

