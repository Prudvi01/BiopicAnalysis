import os, json
import pandas as pd

def convert_to_list(lines):
    output = []
    for x in lines:
        try:
            output.append(eval(x[:-1]))
        except:
            output.append(x[:-1])
    return output

def percent(x, y):
    return round((x/y)*100, 2)

def analysis_countswindows(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        # lines = list(dict.fromkeys(lines))

    # print(len(lines))
    counts = convert_to_list(lines)
    # print(len(counts))
    # print(counts[:2])
    countswindow_words60 = json.loads(counts[3]) # 1 = 60 sorted by words
    countswindow_wikilinks60 = json.loads(counts[4]) # 2 = 60 sorted by wikilinks
    countswindow_references60 = json.loads(counts[5]) # 3 = 60 sorted by references
    countswindow_words120 = json.loads(counts[6]) # 4 = 120 sorted by words
    countswindow_wikilinks120 = json.loads(counts[7]) # 5 = 120 sorted by wikilinks
    countswindow_references120 = json.loads(counts[8]) # 6 = 120 sorted by references
    for i, dic in enumerate(countswindow_words60[::-1]):
        if dic['status'] == '60 before release':
            marker60before = i
        if dic['status'] == '60 after release':
            marker60after = i
    marker_words = [marker60before, marker60after]    
    for i, dic in enumerate(countswindow_wikilinks60[::-1]):
        if dic['status'] == '60 before release':
            marker60before = i
        if dic['status'] == '60 after release':
            marker60after = i
    marker_wikilinks = [marker60before, marker60after] 
    for i, dic in enumerate(countswindow_references60[::-1]):
        if dic['status'] == '60 before release':
            marker60before = i
        if dic['status'] == '60 after release':
            marker60after = i
    marker_references = [marker60before, marker60after] 

    markers60 = (marker_words, marker_wikilinks, marker_references)
    for i, dic in enumerate(countswindow_words120[::-1]):
        if dic['status'] == '120 before release':
            marker60before = i
        if dic['status'] == '120 after release':
            marker60after = i
    marker_words = [marker60before, marker60after] 
    for i, dic in enumerate(countswindow_wikilinks120[::-1]):
        if dic['status'] == '120 before release':
            marker60before = i
        if dic['status'] == '120 after release':
            marker60after = i
    marker_wikilinks = [marker60before, marker60after] 
    for i, dic in enumerate(countswindow_references120[::-1]):
        if dic['status'] == '120 before release':
            marker60before = i
        if dic['status'] == '120 after release':
            marker60after = i
    marker_references = [marker60before, marker60after] 
    
    markers120 = (marker_words, marker_wikilinks, marker_references)
    windowcounts_lengths60 = (len(countswindow_words60), len(countswindow_wikilinks60), len(countswindow_references60))
    windowcounts_lengths120 = (len(countswindow_words120), len(countswindow_wikilinks120), len(countswindow_references120))

    # print('Word count rank for window 60 days before release = ' + str(markers60[0][0]) + '/' + str(windowcounts60[0]))
    return(markers60, windowcounts_lengths60, markers120, windowcounts_lengths120)
    
def analysis_metricswindows(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = list(dict.fromkeys(lines))
    metrics = convert_to_list(lines)

    metricswindows60 = []
    for i in range(len(metrics[3:12])):
        metricswindows60.append(json.loads(metrics[i + 3]))
    metricswindows120 = []
    for i in range(len(metrics[12:])):
        metricswindows120.append(json.loads(metrics[i + 12])) 
    
    markers60 = []
    for metricwindow in metricswindows60:
        for i, dic in enumerate(metricwindow[::-1]):
            if dic['status'] == '60 before release':
                marker60before = i
            if dic['status'] == '60 after release':
                marker60after = i
        markers60.append([marker60before, marker60after])

    markers120 = []
    for metricwindow in metricswindows120:
        for j, dic in enumerate(metricwindow[::-1]):
            if dic['status'] == '120 before release':
                marker60before = j
            if dic['status'] == '120 after release':
                marker60after = j
        markers120.append([marker60before, marker60after])

    windowmetrics_lengths60 = []
    windowmetrics_lengths120 = []
    for window in metricswindows60:
        windowmetrics_lengths60.append(len(window))

    for window in metricswindows120:
        windowmetrics_lengths120.append(len(window))

    return(markers60, windowmetrics_lengths60, markers120, windowmetrics_lengths120)
    # print(metricswindows60[0])

def run_countswindowsAnalysis():
    dire = 'results/slopeswindows/counts/'
    fileNames = os.listdir(str(dire))
    sloperankfile = open('sloperankfile_counts.txt', 'w', encoding='utf-8')
    rows_list60 = []
    rows_list120 = []
    # df.columns = ['Article Name', 'Num of 60 size windows', 'Words Rank BR', 'Words Rank BR%', 'Wikilinks Rank BR', 'Wikilinks Rank BR%', 'References Rank BR', 'References Rank BR%', 'Words Rank AR', 'Words Rank AR%', 'Wikilinks Rank AR', 'Wikilinks Rank AR%', 'References Rank AR', 'References Rank AR%', 'Num of 120 size windows', 'Words Rank BR', 'Words Rank BR%', 'Wikilinks Rank BR', 'Wikilinks Rank BR%', 'References Rank BR', 'References Rank BR%', 'Words Rank AR', 'Words Rank AR%', 'Wikilinks Rank AR', 'Wikilinks Rank AR%', 'References Rank AR', 'References Rank AR%']
    for article in fileNames:
        print(article)
        if not article == '.DS_Store' and not article == '.gitignore':
            markers60, windowcounts_lengths60, markers120, windowcounts_lengths120 = analysis_countswindows(dire + article)
            dict60 = {'Article Name': article[:-4], 'Num of 60 size windows': windowcounts_lengths60[0], 'Words Rank BR': markers60[0][0], 'Words Rank BR%': percent(markers60[0][0],windowcounts_lengths60[0]), 'Wikilinks Rank BR': markers60[1][0], 'Wikilinks Rank BR%': percent(markers60[1][0],windowcounts_lengths60[0]), 'References Rank BR': markers60[2][0], 'References Rank BR%': percent(markers60[2][0],windowcounts_lengths60[0]), 'Words Rank AR': markers60[0][1], 'Words Rank AR%': percent(markers60[0][1],windowcounts_lengths60[0]), 'Wikilinks Rank AR': markers60[1][1], 'Wikilinks Rank AR%': percent(markers60[1][1],windowcounts_lengths60[0]), 'References Rank AR': markers60[2][1], 'References Rank AR%':  percent(markers60[2][1],windowcounts_lengths60[0])}
            dict120 = {'Article Name': article[:-4], 'Num of 120 size windows': windowcounts_lengths120[0], 'Words Rank BR': markers120[0][0], 'Words Rank BR%': percent(markers120[0][0],windowcounts_lengths120[0]), 'Wikilinks Rank BR': markers120[1][0], 'Wikilinks Rank BR%': percent(markers120[1][0],windowcounts_lengths120[0]), 'References Rank BR': markers120[2][0], 'References Rank BR%': percent(markers120[2][0],windowcounts_lengths120[0]), 'Words Rank AR': markers120[0][1], 'Words Rank AR%': percent(markers120[0][1],windowcounts_lengths120[0]), 'Wikilinks Rank AR': markers120[1][1], 'Wikilinks Rank AR%': percent(markers120[1][1],windowcounts_lengths120[0]), 'References Rank AR': markers120[2][1], 'References Rank AR%':  percent(markers120[2][1],windowcounts_lengths120[0])}
            rows_list60.append(dict60)
            rows_list120.append(dict120)
            # row = pd.Series([article[:-4]], windowcounts_lengths60[0], markers60[0][0], percent(markers60[0][0],windowcounts_lengths60[0]), markers60[1][0], percent(markers60[1][0],windowcounts_lengths60[0]), markers60[2][0], percent(markers60[2][0],windowcounts_lengths60[0]), markers60[0][1], percent(markers60[0][1],windowcounts_lengths60[0]), markers60[1][1], percent(markers60[1][1],windowcounts_lengths60[0]), markers60[2][1], percent(markers60[2][1],windowcounts_lengths60[0]),       windowcounts_lengths120[0], markers120[0][0], percent(markers120[0][0],windowcounts_lengths120[0]), markers120[1][0], percent(markers120[1][0],windowcounts_lengths120[0]), markers120[2][0], percent(markers120[2][0],windowcounts_lengths120[0]), markers120[0][1], percent(markers120[0][1],windowcounts_lengths120[0]), markers120[1][1], percent(markers120[1][1],windowcounts_lengths120[0]), markers120[2][1], percent(markers120[2][1],windowcounts_lengths120[0]))
            # sloperankfile.write(article[:-4] + '\n')
            # sloperankfile.write('%s, %s, %s, %s', markers60, windowcounts_lengths60, markers120, windowcounts_lengths120 + '\n')
    df1 = pd.DataFrame(rows_list60) 
    df2 = pd.DataFrame(rows_list120)
    df1.to_csv('slopewindowrank_counts60.csv', encoding='utf-8')
    df2.to_csv('slopewindowrank_counts120.csv', encoding='utf-8')

def run_metricswindowsAnalysis():
    dire = 'results/slopeswindows/metrics/'
    fileNames = os.listdir(str(dire))
    rows_list60 = []
    rows_list120 = []
    ignorefiles = ['Michael_Rezendes_metrics.txt', '.DS_Store', '.gitignore', 'Jiro_Horikoshi_metrics.txt', 'Owen_Chase_metrics.txt', 'David_Lipsky_metrics.txt', 'Milkha_Singh_metrics.txt', 'Phiona_Mutesi_metrics.txt']
    for article in fileNames:
        print(article)
        if not article in ignorefiles:
            markers60, windowmetrics_lengths60, markers120, windowmetrics_lengths120 = analysis_metricswindows(dire + article)
            columns = ['FRE', 'SI', 'FKG', 'CLI', 'ARI', 'DCRS', 'DW', 'LWF', 'GF']
            print(markers60)
            dict60 = {'Article Name': article[:-4], 'Num of 60 size windows': windowmetrics_lengths60[0]}
            for j in range(len(markers60)): # 9
                dict60[columns[j] + ' Rank BR'] = markers60[j][0]
                dict60[columns[j] + ' Rank BR%'] = percent(markers60[j][0], windowmetrics_lengths60[0])
            for j in range(len(markers60)): # 9
                dict60[columns[j] + ' Rank AR'] = markers60[j][1]
                dict60[columns[j] + ' Rank AR%'] = percent(markers60[j][1], windowmetrics_lengths60[1])
            print(markers120)
            dict120 = {'Article Name': article[:-4], 'Num of 120 size windows': windowmetrics_lengths120[0]}
            for j in range(len(markers120)):
                dict120[columns[j] + ' Rank BR'] = markers120[j][0]
                dict120[columns[j] + ' Rank BR%'] = percent(markers120[j][0], windowmetrics_lengths120[0])
            for j in range(len(markers120)):
                dict120[columns[j] + ' Rank AR'] = markers120[j][1]
                dict120[columns[j] + ' Rank AR%'] = percent(markers120[j][1], windowmetrics_lengths120[1])
            
            rows_list60.append(dict60)
            rows_list120.append(dict120)
    df1 = pd.DataFrame(rows_list60) 
    df2 = pd.DataFrame(rows_list120)
    df1.to_csv('slopewindowrank_metrics60.csv', encoding='utf-8')
    df2.to_csv('slopewindowrank_metrics120.csv', encoding='utf-8')
# analysis_countswindows('results/slopeswindows/counts/Diana,_Princess_of_Wales_counts.txt')
# analysis_metricswindows('results/slopeswindows/metrics/Jiro_Horikoshi_metrics.txt')

run_countswindowsAnalysis()
run_metricswindowsAnalysis()