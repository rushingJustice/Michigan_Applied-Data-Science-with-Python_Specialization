# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np

# Create split - join func for data (remove inner whitespace..)
def make_int(text):
    try:
        x = "".join(text.split())
        return int(x)
    except AttributeError:
        return text
    
# Load energy df

energy = pd.read_excel('data/Energy Indicators.xls', 
                     usecols=['Unnamed: 1','Petajoules','Gigajoules','%'],
                     encoding = "ISO-8859-1", na_values = '...',
                     skiprows = 17, skip_footer = (38))
energy = energy.rename(columns={'Unnamed: 1': 'Country', 'Petajoules': 'Energy Supply',
                     'Gigajoules': 'Energy Supply per Capita', 
                     '%': '% Renewable'})

#energy = pd.read_csv('data/EnergyIndicators.csv', index_col = 0, 
                     #encoding = "ISO-8859-1", na_values = '...')
# Set Energy Supply to GigaJoules and call make_int
energy['Energy Supply'] = energy['Energy Supply'] * 1000000
# Remove countries with (..) AND/OR numbers in Name
energy['Country'] = energy['Country'].str.replace(r"\(.*\)","") # replace (...) with nothing
energy['Country'] = energy['Country'].str.replace('\d+', '') # replace digits with nothing
energy['Country'] = energy['Country'].str.strip() # remove proceeding/trailing whitespace
# Rename specific countries per assignment
energy['Country'].replace(['Republic of Korea','United States of America',
      'United Kingdom of Great Britain and Northern Ireland',
      'China, Hong Kong Special Administrative Region'],
    ['South Korea','United States', 'United Kingdom','Hong Kong'],
    inplace=True)

# Load GDP df
GDP = pd.read_csv('data/world_bank.csv', encoding = "ISO-8859-1", skiprows=4)
GDP = GDP.rename(columns={'Country Name': 'Country'})
GDP['Country'].replace(['Korea, Rep.', 'Iran, Islamic Rep.',
   'Hong Kong SAR, China'], ['South Korea', 'Iran', 'Hong Kong'], inplace=True)

# Load ScimEn
ScimEn = pd.read_excel('data/scimagojr-3.xlsx', encoding = "ISO-8859-1")

# Join Energy, GDP and ScimEn
GDP = GDP[['Country','2006','2007','2008','2009',
           '2010','2011','2012','2013','2014','2015']] # take only GDP data from 2006-2015
EnergyGDP = pd.merge(energy, GDP, how='outer', on='Country') # Join Energy and GDP
df = pd.merge(EnergyGDP, ScimEn, how='outer', on='Country') # Join with with ScimEn
df.set_index('Country', inplace=True) # set to Country

df = df.loc[:,['Rank', 'Documents', 'Citable documents', 'Citations', 
               'Self-citations', 'Citations per document', 'H index', 
               'Energy Supply', 'Energy Supply per Capita', '% Renewable', 
               '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', 
               '2014', '2015']]

df_sorted = df.sort_values('Rank')
df = df_sorted.iloc[0:15,:] # take only first ranks 1-15

def answer_one():
    return df

def answer_two():
    df = pd.merge(energy, GDP, how='outer', on='Country') # Join Energy and GDP
    dfAll = pd.merge(df, ScimEn, how='outer', on='Country') # Join with with ScimEn
    outside = len(dfAll)
    
    df = pd.merge(energy, GDP, how='inner', on='Country') # Join Energy and GDP
    dfAll = pd.merge(df, ScimEn, how='inner', on='Country') # Join with with ScimEn
    inside = len(dfAll)
    
    return outside - inside

def answer_three():
    avgGDP = np.mean(df.loc[:,'2006':'2015'],axis=1).sort_values(ascending=False)
    return avgGDP

def answer_four():
    avgGDP = np.mean(df.loc[:,'2006':'2015'],axis=1).sort_values(ascending=False)
    ans = df.loc[avgGDP.index[5]]['2015'] - df.loc[avgGDP.index[5]]['2006']
    return ans

def answer_five():
    ans = np.mean(df['Energy Supply per Capita'])
    return ans

def answer_six():
    ans = (df['% Renewable'].argmax(), max(df['% Renewable']))
    return ans

def answer_seven():
    ratio = df['Self-citations'] / df['Citations']
    ans = (ratio.argmax(), max(ratio))
    return ans

def answer_eight():
    popEstimate = df['Energy Supply'] / df['Energy Supply per Capita']
    popEstimate.sort_values(ascending=False, inplace=True)
    thirdMostPop = popEstimate.index[2]
    return thirdMostPop

def answer_nine():
    popEstimate = df['Energy Supply'] / df['Energy Supply per Capita']
    citeCapita = df['Citable documents'] / popEstimate
    joinCapita = citeCapita.to_frame().join(df['Energy Supply per Capita'].to_frame())
    ans = joinCapita.corr().iloc[0,1]
    return ans

def plot9():
    import matplotlib as plt
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])
    
def answer_ten():
    renewMedian = np.median(df['% Renewable'])
    HighRenew = (df['% Renewable'] >= renewMedian).replace([True,False],[1,0])
    return HighRenew

def answer_eleven():
    dict = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    cont = df.reset_index()
    cont['Country'] = cont['Country'].map(dict)
    cont = cont.rename(columns={"Country": "Continent"})
    # Add in the estimated pop
    cont['Estimated Population'] = cont['Energy Supply'] /cont['Energy Supply per Capita']
    # 
    Continent = cont.set_index('Continent').groupby(level=0)['Estimated Population'].agg({'size': len, 'sum': np.sum, 'mean': np.average, 'std': np.std})
    
    return Continent

def answer_twelve():
    Top15 = answer_one()
    dict = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    cont = Top15.reset_index()
    cont['Continent'] = cont['Country'].map(dict)
    cont['Renew'] = pd.cut(cont['% Renewable'],5)
    return cont.groupby(['Continent', 'Renew']).size()

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    def thousands(x):
        try:
            return '{0:,}'.format(x)
        except ValueError as e:
            return x
    return Top15['PopEst'].apply(thousands)
# as a lamba...
    #return Top15.apply(lambda x: "{:,}".format(x['PopEst']), axis=1)

