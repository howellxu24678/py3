# -*- coding: utf-8 -*-
__author__ = 'xujh'

import xlwings as xw
import pandas as pd
import datetime


#短期明细2018.01.15
wb = xw.Book(r'./账目/李家账.xlsx')
#短期明细2018.01.15
ws = wb.sheets['短期明细']
df = ws.range((2, 2), (ws.api.UsedRange.Rows.count, ws.api.UsedRange.Columns.count)).options(pd.DataFrame, expand='table').value
df = df.reset_index()
df = df.drop(0)

df['应还日期'] = df['应还日期'].map(lambda x: x.strftime("%Y/%m/%d") if not isinstance(x, str) and isinstance(x, datetime.datetime) else x )
df['实还日期'] = df['实还日期'].map(lambda x: x.strftime("%Y/%m/%d") if not isinstance(x, str) and isinstance(x, datetime.datetime) else x )

dc = df[df['实还日期'] > df['应还日期']]['姓名'].groupby(df['姓名']).count()
dc[dc > 1]

df[(df['实还日期'] > df['应还日期']) & (df['姓名'] == '陈鲁健')]
df[df['姓名'] == '陈鲁健'][['姓名','应还日期','实还日期']]

df['收益'] = df['已还金额'] - df['到账金额']

# df[df['应还日期'].map(lambda x: not isinstance(x, str))]
# df['应还日期'][29].strftime("%Y/%m/%d")

#df[df['实还日期'].isnull()] isnan()
#df[df['实还日期'].notnull()]
#删除第一行 df = df.drop(0)

app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = False
wb = app.books.open(r'./账目/李家账.xlsx')

