# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'d8ec60a9509245ea9dd4073c9fc5ce2d22d38ae8cfe148550e6c959e')

# Read in and sort
df = pd.read_csv('data/d8ec60a9509245ea9dd4073c9fc5ce2d22d38ae8cfe148550e6c959e.csv')
df['Date'] = pd.to_datetime(df['Date'])
df_2005_2014 = df[(df['Date'] >= '2005') & (df['Date'] <= '2014')]
df_2005_2014['Date'] = pd.to_datetime(df_2005_2014['Date'])
df_2005_2014['Tmin_Value'] = df_2005_2014['Data_Value'][(df_2005_2014['Element'] == 'TMIN')]
df_2005_2014['Tmax_Value'] = df_2005_2014['Data_Value'][(df_2005_2014['Element'] == 'TMAX')]
df_2005_2014.set_index('Date', inplace=True)

record10Year = df_2005_2014.groupby([(df_2005_2014.index.month),(df_2005_2014.index.day)]).agg({'Tmax_Value': np.max, 'Tmin_Value': np.min})
record10Year = record10Year.reset_index(drop=True).drop([59]).reset_index()

# Get 2015 data
df_2015 = df[(df['Date'] >= '2015')]
df_2015['Tmin_Value'] = df_2015['Data_Value'][(df_2015['Element'] == 'TMIN')]
df_2015['Tmax_Value'] = df_2015['Data_Value'][(df_2015['Element'] == 'TMAX')]
df_2015['Date'] = pd.to_datetime(df_2015['Date'])
df_2015.set_index('Date', inplace=True)
data2015 = df_2015.groupby(df_2015.index).agg({'Tmax_Value': np.max, 'Tmin_Value': np.min})

# Take only data that beats the 10 Year Record
data2015.reset_index(drop=True, inplace=True)
broke10YearMax = data2015['Tmax_Value'][(data2015['Tmax_Value'] > record10Year['Tmax_Value'])]
broke10YearMin = data2015['Tmin_Value'][(data2015['Tmin_Value'] < record10Year['Tmin_Value'])]

# Plot it
plt.figure()

plt.plot(record10Year['Tmax_Value']/10, '-r', alpha=0.3)
plt.plot(record10Year['Tmin_Value']/10, '-b', alpha=0.3)
plt.scatter(np.array(broke10YearMax.index), broke10YearMax.values/10, s=10, color='r')
plt.scatter(np.array(broke10YearMin.index), broke10YearMin.values/10, s=10, color='b')
plt.gca().fill_between(range(len(record10Year['Tmax_Value'])), 
                       record10Year['Tmax_Value']/10, record10Year['Tmin_Value']/10, 
                       facecolor='grey', 
                       alpha=0.15)

xticks = np.array([1,32,60,91,121,152,182,213,244,274,305,335])
xticks_labels = pd.to_datetime(xticks,format='%j').strftime('%b')
plt.xticks(xticks, xticks_labels, alpha=1, ha='left', rotation=None)

ax = plt.gca()
ax.axis([1,365,-15,50])

plt.ylabel('Degrees C')
plt.title('Record High/Low Temperature in Gilbert, AZ [2005-2014]')
plt.legend(['High', 'Low', '2015 Highs', '2015 Lows'])

# add a legend with legend entries (because we didn't have labels when we plotted the data series)



#observation_dates = list(map(pd.to_datetime, observation_dates)) # convert the map to a list to get rid of the error

#observation_dates = np.arange('2017-01-01', '2017-01-09', dtype='datetime64[D]')
#dates = list(dates) # convert the map to a list to get rid of the error
#plt.plot(dates, tmin, '-o',  dates, tmax, '-o')
