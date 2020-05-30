import pandas as pd
import numpy as np

f = open('statistics.txt', 'w', encoding = 'utf-8')
def query(a, b):
    '''
    returns number of files where columns a is greater than column b
    '''
    return len(np.where(data[a] > data[b])[0])

avgstdmetric_list = ['fre', 'si', 'fkg', 'cli', 'ari', 'dcrs', 'dw', 'lwf', 'gf']
metric_list = ['FRE', 'SI', 'FKG', 'CLI', 'ARI', 'DCRS', 'DW', 'LWF', 'GF']
avgstdcounts_list = ['words', 'wikilinks', 'references']
counts_list = ['Words', 'Wikilinks', 'References']
rankframes = ['BR', 'AR'] # Before Release, After Release
avgstdframes = ['120 frame', '60 frame']



f.write('==================== COUNTS ====================')
f.write('\n')
# printing the counts's average and std statistics
data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/AvgStd_counts.csv')
f.write('\nNUMBER OF ARTICLES (TOTAL = '+str(data.shape()[0])+') WHERE AVERAGE OF: \n')
f.write('\n')
for item in avgstdcounts_list:
    for frame in avgstdframes:
        f.write(item+' in '+frame+' is greater than all revisions = ' + str(query('Avg '+item+' of '+frame,'Avg '+item+' of all Revi'))) # should be high
        f.write('\n')

f.write('\nNUMBER OF ARTICLES (TOTAL = '+str(data.shape()[0])+') WHERE STD OF: \n')
f.write('\n')
for item in avgstdcounts_list:
    for frame in avgstdframes:
        f.write(item+' in '+frame+' is greater than all revisions = ' + str(query('STD '+item+' of '+frame,'Avg '+item+' of all Revi'))) # should be low
        f.write('\n')

# printing the counts's 60 and 120 frames's slope window ranks statistics
data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/slopewindowrank_counts60.csv')

f.write('\nFOR WINDOW SIZE OF 60 NUMBER OF FILES (TOTAL = '+str(data.shape()[0])+') WHERE :\n')
f.write('\n')
for item in counts_list:
    f.write(item + ' rank BR is greater than '+item+' rank AR = ', str(query(item+' Rank BR', item+' Rank AR'))) # should be high
    f.write('\n')

data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/slopewindowrank_counts120.csv')

f.write('\nFOR WINDOW SIZE OF 120 NUMBER OF FILES (TOTAL = '+str(data.shape()[0])+') WHERE :\n')
f.write('\n')
for item in counts_list:
    f.write(item + ' rank BR is greater than '+item+' rank AR = ', str(query(item+' Rank BR', item+' Rank AR'))) # should be high
    f.write('\n')

f.write('\n==================== METRICS ====================')
f.write('\n')
# printing the metrics's average and std statistics
data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/AvgStd_metrics.csv')
f.write('\nNUMBER OF ARTICLES (TOTAL = '+str(data.shape()[0])+') WHERE AVERAGE OF: \n')
f.write('\n')
for item in avgstdmetric_list:
    for frame in avgstdframes:
        f.write(item+' in '+frame+' is greater than all revisions = ' + str(query('Avg '+item+' of '+frame,'Avg '+item+' of all Revi'))) # should be high
        f.write('\n')

f.write('\nNUMBER OF ARTICLES (TOTAL = '+str(data.shape()[0])+') WHERE STD OF: \n')
f.write('\n')
for item in avgstdmetric_list:
    for frame in avgstdframes:
        f.write(item+' in '+frame+' is greater than all revisions = ' + str(query('STD '+item+' of '+frame,'Avg '+item+' of all Revi'))) # should be low
        f.write('\n')

# printing the metrics's 60 and 120 frames's slope window ranks statistics
data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/slopewindowrank_metrics60.csv')

f.write('\nFOR WINDOW SIZE OF 60 NUMBER OF FILES (TOTAL = '+str(data.shape()[0])+') WHERE :\n')
f.write('\n')
for item in metric_list:
    f.write(item + ' rank BR is greater than '+item+' rank AR = ', str(query(item+' Rank BR', item+' Rank AR'))) # should be high
    f.write('\n')

data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/slopewindowrank_metrics120.csv')
f.write('\nFOR WINDOW SIZE OF 120 NUMBER OF FILES (TOTAL = '+str(data.shape()[0])+') WHERE :\n')
f.write('\n')
for item in metric_list:
    f.write(item + ' rank BR is greater than '+item+' rank AR = ', str(query(item+' Rank BR', item+' Rank AR'))) # should be high
    f.write('\n')

f.close()
'''
data = pd.read_csv('/Users/prudvikamtam/Projects/BiopicAnalysis/AvgStd_ores.csv')
ores_list = ['damaging', 'goodfaith']
# for item in ores_list:
#     f.write(item + ' rank BR is greater than '+item+' rank AR = ', str(query(item+' Rank BR', item+' Rank AR')))
        f.write('\n')

f.write('Avg goodfaith of 120 frame is less than all revi = ' + str(len(np.where(data['Avg goodfaith of all Revi'] > data['Avg goodfaith of 120 frame'])[0])))
f.write('\n')
'''