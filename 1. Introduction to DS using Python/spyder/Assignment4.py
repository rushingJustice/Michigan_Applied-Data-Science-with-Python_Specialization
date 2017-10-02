# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 07:12:26 2017

@author: Fun
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def para_remove(x):
    try: 
        return x.split('(', 1)[0]
    except ValueError as e:
            return x

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
# Import University Towns
UniTowns = pd.read_table('data/university_towns.txt', names=('A'),)
# Sanitize and create boolean matrix
UniTowns['A'] = UniTowns.A.str.replace(r"\[.*\]","").str.strip() # Remove [anything]
NBool = UniTowns.isin(states.values())
UniTowns['A']= UniTowns.A.apply(para_remove).str.strip() # Remove (anything)

# Apply bool matrix to make State and RegionName columns
state = UniTowns[NBool==True]
regionName = UniTowns[NBool==False]
UniTowns['State'] = state.fillna(method='ffill') # Fill NaN with prior name
UniTowns['RegionName'] = regionName
UniTowns = UniTowns[pd.notnull(UniTowns['RegionName'])].drop('A', axis=1) # remove NaN's and drop A
UniTowns = UniTowns.reset_index().drop('index', axis=1)

# Import GDP data
GDP = pd.read_excel('data/gdplev.xls', usecols=range(4,7), 
                    skiprows = 7, names = ('YearQ', 'GDP', 'GDP_Chained'))

Data = GDP['GDP_Chained']
begin = '2000q1'

startIndex = GDP[GDP.YearQ == begin].index[0]
for j in range(startIndex + 2,len(Data)-1):
    if Data[j] < Data[j-1] and Data[j-1] < Data[j-2]:
        recessionStart = GDP['YearQ'][j-1]
        recessionBeforeStart = GDP['YearQ'][j-2]
        break

startIndex = GDP[GDP.YearQ == recessionStart].index[0]
for j in range(startIndex + 2,len(Data)-1):
    if Data[j] > Data[j-1] and Data[j-1] > Data[j-2]:
        recessionEnd = GDP['YearQ'][j]
        break
    
recessionStartIndex = GDP[GDP.YearQ == recessionStart].index[0]
recessionEndIndex = GDP[GDP.YearQ == recessionEnd].index[0]
Recession = GDP.iloc[recessionStartIndex:recessionEndIndex+1]
recessionBottom = Recession['YearQ'][Recession['GDP_Chained'].idxmin()]

# import housing data
House = pd.read_csv('data/City_Zhvi_AllHomes.csv')
House['State'] = House['State'].map(states)
House = House.set_index(['State','RegionName']).loc[:,'2000-01':'2016-08']
House.columns = pd.to_datetime(House.columns) # Convert to datatime
House = House.resample('3M', axis=1, closed='left').mean().rename(columns=lambda x: '{:}q{:}'.format(x.year, x.quarter))# Resample to quarters

# T-test


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    return UniTowns

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    return recessionStart

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
       
    return recessionEnd

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    return recessionBottom

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    A quarter is a specific three month period, 
    Q1 is January through March,
    Q2 is April through June, 
    Q3 is July through September, 
    Q4 is October through December.
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    return House

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    UniTowns.set_index(['State', 'RegionName'], inplace=True)
    UTHdf = pd.merge(House, UniTowns, how='inner', left_index=True, right_index=True)
    NTHdf = pd.merge(House, UniTowns, how='outer', left_index=True, right_index=True, indicator=True)
    NTHdf=NTHdf[NTHdf['_merge']=='left_only']  # Take OUT the University towns
    
    UTHdf['Reccession Price Ratio'] = UTHdf[recessionStart].div(UTHdf[get_recession_bottom()])
    UTHdf = UTHdf[pd.notnull(UTHdf['Reccession Price Ratio'])]
    NTHdf['Reccession Price Ratio'] = NTHdf[recessionStart].div(NTHdf[get_recession_bottom()])
    NTHdf = NTHdf[pd.notnull(NTHdf['Reccession Price Ratio'])]
    test = ttest_ind(UTHdf['Reccession Price Ratio'],  NTHdf['Reccession Price Ratio'])
    
    p = test[1]
    different = True if p <= 0.01  else False
    
    if UTHdf['Reccession Price Ratio'].min() < NTHdf['Reccession Price Ratio'].min():
        better = 'university town'
    else:
        better = 'non-university town'
    
    ans = (different, p, better)
    return ans