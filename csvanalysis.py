import pandas as pd
import numpy as np

#data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/AvgStd_metrics.csv')
def query(a, b):
    '''
    returns number of files where columns a is greater than column b
    '''
    return len(np.where(data[a] > data[b])[0])

metric_list = ['FRE', 'SI', 'FKG', 'CLI', 'ARI', 'DCRS', 'DW', 'LWF', 'GF']
counts_list = ['Words', 'Wikilinks', 'References']
frames = ['BR', 'AR'] # Before Release, After Release

'''
for item in metric_list:
    for frame in frames:
        print('Number of articles where average of '+item+' in '+frame+' is greater than all revisions = ' + str(query('Avg '+item+' of '+frame,'Avg '+item+' of all Revi')))

for item in metric_list:
    for frame in frames:
        print('Number of articles where STD of '+item+' in '+frame+' is greater than all revisions = ' + str(query('STD '+item+' of '+frame,'Avg '+item+' of all Revi')))
'''
print('=============== COUNTS ===============')
data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/slopewindowrank_counts60.csv')

print('\nFOR WINDOW SIZE OF 60 NUMBER OF FILES WHERE :\n')
for item in counts_list:
    print(item + ' rank BR is greater than '+item+' rank AR = ', str(query(item+' Rank BR', item+' Rank AR')))

data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/slopewindowrank_counts120.csv')

print('\nFOR WINDOW SIZE OF 120 NUMBER OF FILES WHERE :\n')
for item in counts_list:
    print(item + ' rank BR is greater than '+item+' rank AR = ', str(query(item+' Rank BR', item+' Rank AR')))

print('\n=============== METRICS ===============')
data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/slopewindowrank_metrics60.csv')

print('\nFOR WINDOW SIZE OF 60 NUMBER OF FILES WHERE :\n')
for item in metric_list:
    print(item + ' rank BR is greater than '+item+' rank AR = ', str(query(item+' Rank BR', item+' Rank AR')))


data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/slopewindowrank_metrics120.csv')
print('\nFOR WINDOW SIZE OF 120 NUMBER OF FILES WHERE :\n')
for item in metric_list:
    print(item + ' rank BR is greater than '+item+' rank AR = ', str(query(item+' Rank BR', item+' Rank AR')))
