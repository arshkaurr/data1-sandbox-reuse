import pandas as pd
from .models import ddo_hourly

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource, ranges, LabelSet

from datetime import timedelta

from django.db.models.functions import ExtractWeekDay
from django.db.models import Avg, Sum


def import_records():
    df = pd.read_csv('test_data.csv')
    print(df.shape == df.isna().shape and df.shape == df.isnull().shape)
    df['hDate'] = pd.to_datetime(df['hDate'])
    temp_columns = list(df.columns)
    for i in range(0,df.shape[0]):
        temp_dict = {}
        the_total = 0
        for n,j in enumerate(df.iloc[i]):
            temp_dict[temp_columns[n]] = j
            if temp_columns[n] != 'hDate' : the_total += j
        temp_dict['hTotal'] = the_total
        ddo_hourly.objects.create(**temp_dict).save()









def bokeh_render_hours(q):
    #This functions takes in a queryset and returns a Bokeh Graph
    plot = figure(title='Total Donations by DAY', x_axis_label='Date Range', y_axis_label='Individual Donations', x_axis_type='datetime')

    x = [i.hDate for i in q]
    y = [i.hTotal for i in q]
    c = ['#5A9D43' if i.hTotal < 100 else 'red' for i in q]

    # plot.circle([1,10,35,50],[1,2,3,4],size=20, color="blue")
    # plot.line(x=x,y=y, color='red')
    plot.vbar(x=x,top=y, width=timedelta(days=0.75), color=c)
    return plot







def bokeh_render_by_weekday(q):
    #This functions takes in a queryset and returns a Bokeh Graph

    WeekDayList = {1:'1. Sunday',2:'2. Monday', 3:'3. Tuesday', 4: '4. Wednesday', 5:'5. Thursday', 6: '6. Friday', 7: '7. Saturday'}
    ColorDayList = {1:'mediumseagreen',2:'green', 3:'mediumseagreen', 4: 'mediumseagreen', 5:'mediumseagreen', 6: 'mediumseagreen', 7: 'green'}

    plot = figure(title='Donations Totaled by Day of the Week',x_axis_label='Days of the Week (#) Sun, Mon ...', y_axis_label='Total Individual Donations')

    temp = q.annotate(weekday=ExtractWeekDay('hDate')).values('weekday').annotate(sum=Sum('hTotal'),avg=Avg('hTotal'))

    for i in temp:
        plot.vbar(x=i['weekday'],top=i['sum'], width=0.85, color=ColorDayList[i['weekday']] )

    return plot




def bokeh_render_by_hour(q):
    #This functions takes in a queryset and returns a Bokeh Graph

    # WeekDayList = {1:'1. Sunday',2:'2. Monday', 3:'3. Tuesday', 4: '4. Wednesday', 5:'5. Thursday', 6: '6. Friday', 7: '7. Saturday'}
    # ColorDayList = {1:'mediumseagreen',2:'green', 3:'mediumseagreen', 4: 'mediumseagreen', 5:'mediumseagreen', 6: 'mediumseagreen', 7: 'green'}
    # temp = q.annotate(weekday=ExtractWeekDay('hDate')).values('weekday').annotate(sum=Sum('hTotal'),avg=Avg('hTotal'))
    # for i in temp:
    #     plot.vbar(x=i['weekday'],top=i['sum'], width=0.85, legend=WeekDayList[i['weekday']], color=ColorDayList[i['weekday']] )

    HourList = ['h10','h11','h12','h13','h14','h15','h16','h17']
    HourListLabels = {'h10':'10a-11a', 'h11':'11a-12p', 'h12':'12p-1p', 'h13':'1p-2p', 'h14':'2p-3p', 'h15':'3p-4p', 'h16':'4p-5p', 'h17':'5p-6p'}

    plot = figure(title='Donations Totaled by HOUR of the Day',x_axis_label='Hour of the Day', y_axis_label='Total Individual Donations')

    bokeh_dict = {}
    for i in HourList:
        bokeh_dict[i] = list(q.aggregate(Sum(i)).values())[0]

    #print(bokeh_dict)
    x = [i for i in bokeh_dict.keys()]
    top = [i for i in bokeh_dict.values()]
    #print('\n\n\n',x,'\n\n\n',top,'\n\n\n')

    plot.vbar(x=[10,11,12,13,14,15,16,17], top=top, width=0.85)


    return plot
