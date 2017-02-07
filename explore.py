import csv
import httplib2
from apiclient.discovery import build
import urllib
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.plotly as py 
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF

plotly.tools.set_credentials_file(username = 'ediering', api_key='k23nwbsle7')

# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyAmiZjaV_lNunEyrglKUuqK57TvVPM84aY'

# This is the table id for the fusion table
TABLE_ID = '15CnIT8u1snCOSRYjV3lPrEnUR_5qoGZ1ZhwGytAt'

try:
    fp = open("data.json")
    response = json.load(fp)
except IOError:
    service = build('fusiontables', 'v1', developerKey=API_KEY)
    query = "SELECT * FROM " + TABLE_ID #+ " WHERE 'Total Energy Cost ($)' > 0 AND 'Total Energy Cost ($)' < 1000000 "
    response = service.query().sql(sql=query).execute()
    fp = open("data.json", "w+")
    json.dump(response, fp)
    
# print len(response['rows'])
    
data_df = pd.DataFrame(response[u'rows'], columns = response[u'columns'])

working = data_df[['Site', 'Site ID', 'Year', 'Total Energy (kBtu)', 'Total Energy Cost ($)']]

pivot_cost = working.pivot(index='Site ID', columns='Year', values='Total Energy Cost ($)')
pivot_energy = working.pivot(index='Site ID', columns='Year', values='Total Energy (kBtu)')

def totalcostplot_energy():
  pivot_cost = working.pivot(index='Site ID', columns='Year', values='Total Energy Cost ($)')
  pivot_energy = working.pivot(index='Site ID', columns='Year', values='Total Energy (kBtu)')
  rows = pivot_cost.index

  plot = []

  for i in xrange(len(rows)):
    index = rows[i]
    trace = go.Scatter(
        x = pivot_cost.columns.values,
        y = pivot_cost.loc[index],
        #mode = 'markers'
    )
    plot.append(trace)

  layout = go.Layout(
            xaxis=dict(
              autotick=False),
            showlegend=False)

  fig= go.Figure(data=plot, layout=layout)
  
  return fig

def boxplot():
  ten = pd.to_numeric(pivot_cost['2010']).dropna()
  eleven = pd.to_numeric(pivot_cost['2011']).dropna()
  twelve = pd.to_numeric(pivot_cost['2012']).dropna()
  thirteen = pd.to_numeric(pivot_cost['2013']).dropna()
  fourteen = pd.to_numeric(pivot_cost['2014']).dropna()
  
  trace0 = go.Box(
    y= ten,
    name = '2010'
  )
  trace1 = go.Box(
      y= eleven,
      name = '2011'
  )
  trace2 = go.Box(
      y= twelve,
      name = '2012'
  )
  trace3 = go.Box(
      y= thirteen,
      name = '2013'
  )
  trace4 = go.Box(
      y= fourteen,
      name = '2014'
  )
  data = [trace0, trace1, trace2, trace3, trace4]
  layout = go.Layout(
    yaxis=dict(
        range=[0, 40000]
    )
  )
  return [data, layout]

def histogram():
  ten = pd.to_numeric(pivot_cost['2010']).dropna()
  eleven = pd.to_numeric(pivot_cost['2011']).dropna()
  twelve = pd.to_numeric(pivot_cost['2012']).dropna()
  thirteen = pd.to_numeric(pivot_cost['2013']).dropna()
  fourteen = pd.to_numeric(pivot_cost['2014']).dropna()
  
  plt = sns.distplot(fourteen)
  plt1 = sns.distplot(thirteen)
  plt2 = sns.distplot(twelve)
  plt3 = sns.distplot(eleven)
  plt4 = sns.distplot(ten)
  fig = plt.get_figure()
  fig.savefig("overlay.png")
 
def sum_data():
  cost = working['Total Energy Cost ($)']
  print(cost[1])

def average_data():
  data_df = pd.DataFrame(response[u'rows'], columns = response[u'columns'])
  working = data_df[['Site', 'Site ID', 'Year', 'Total Energy (kBtu)', 'Total Energy Cost ($)']]
  pivot_cost = working.pivot(index='Site ID', columns='Year', values='Total Energy Cost ($)')
  
  ten = pd.to_numeric(pivot_cost['2010']).dropna()
  eleven = pd.to_numeric(pivot_cost['2011']).dropna()
  twelve = pd.to_numeric(pivot_cost['2012']).dropna()
  thirteen = pd.to_numeric(pivot_cost['2013']).dropna()
  fourteen = pd.to_numeric(pivot_cost['2014']).dropna()
  
  averages = [np.mean(ten), np.mean(eleven), np.mean(twelve), np.mean(thirteen), np.mean(fourteen)]
  data = [go.Bar(
            x=['2010', '2011', '2012', '2013', '2014'],
            y=[averages[0], averages[1], averages[2], averages[3], averages[4] ],
    )]
  return data

def median_data():
  data_df = pd.DataFrame(response[u'rows'], columns = response[u'columns'])
  working = data_df[['Site', 'Site ID', 'Year', 'Total Energy (kBtu)', 'Total Energy Cost ($)']]
  pivot_cost = working.pivot(index='Site ID', columns='Year', values='Total Energy Cost ($)')
  
  ten = pd.to_numeric(pivot_cost['2010']).dropna()
  eleven = pd.to_numeric(pivot_cost['2011']).dropna()
  twelve = pd.to_numeric(pivot_cost['2012']).dropna()
  thirteen = pd.to_numeric(pivot_cost['2013']).dropna()
  fourteen = pd.to_numeric(pivot_cost['2014']).dropna()
  
  averages = [np.median(ten), np.median(eleven), np.median(twelve), np.median(thirteen), np.median(fourteen)]
  data = [go.Bar(
            x=['2010', '2011', '2012', '2013', '2014'],
            y=[averages[0], averages[1], averages[2], averages[3], averages[4] ],
    )]
  return data
  
def total_data():
  data_df = pd.DataFrame(response[u'rows'], columns = response[u'columns'])
  working = data_df[['Site', 'Site ID', 'Year', 'Total Energy (kBtu)', 'Total Energy Cost ($)']]
  pivot_cost = working.pivot(index='Site ID', columns='Year', values='Total Energy Cost ($)')
  
  ten = pd.to_numeric(pivot_cost['2010']).dropna()
  eleven = pd.to_numeric(pivot_cost['2011']).dropna()
  twelve = pd.to_numeric(pivot_cost['2012']).dropna()
  thirteen = pd.to_numeric(pivot_cost['2013']).dropna()
  fourteen = pd.to_numeric(pivot_cost['2014']).dropna()
  
  averages = [np.sum(ten), np.sum(eleven), np.sum(twelve), np.sum(thirteen), np.sum(fourteen)]
  data = [go.Bar(
            x=['2010', '2011', '2012', '2013', '2014'],
            y=[averages[0], averages[1], averages[2], averages[3], averages[4] ],
    )]
  return data
  
  
  


#data = totalcostplot_energy()
#fig = go.Figure(data=data[0], layout=data[1])
# fig = histogram()
# fig['layout'].update( yaxis=dict(
#         range=[0,0.1]
#     ))
# data = median_data()
#py.iplot(data)

# data2 = boxplot()
# py.iplot(data2)
# boxplot()
# sanitized_boxplot()
#average_data()
#total_data()
