'''
Compute the total, +60,-60 and +120, -120 averages for all metrics
'''
import os
import pandas as pd
from numpy import mean, std

def convert_to_list(lines):
    output = []
    for x in lines:
        try:
            x = x.replace('NaN', '0')
            output.append(eval(x[:-1]))
        except:
            output.append(x[:-1])
    return output

def findmarkers(item):
    markers = [0,0,0,0,0] # [120 days start, 60 days start, movie release, 60 end, 120 end]
    for i, item in enumerate(item):
        if item == '120 days start':
            markers[0] = i
        if item == '60 days start':
            markers[1] = i
        if item == 'reviafterrelease':
            markers[2] = i
        if item == '60 days end':
            markers[3] = i
        if item == '120 days end':
            markers[4] = i
    if markers[3] == 0:
        markers[3] = i
    if markers[4] == 0:
        markers[4] = i
    

    return markers

def findcountavgstd(counts):
    wikilinks = []
    references = []
    words = []
    for entry in counts:
        if type(entry) != str:
            wikilinks.append(entry['wikilinks'])
            references.append(entry['references'])
            words.append(entry['words'])
    avgs = {}
    stds = {}
    try:
        avgs['words'] = mean(words)
        avgs['wikilinks'] = mean(wikilinks)
        avgs['references'] = mean(references)
        stds['words'] = std(words)
        stds['wikilinks'] = std(wikilinks)
        stds['references'] = std(references)
    except:
        avgs = {'words' : 0, 'wikilinks' : 0, 'references' : 0}
        stds = {'words' : 0, 'wikilinks' : 0, 'references' : 0}
    return (avgs, stds)

def analyse_counts(filepath):
    with open(filepath, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        lines = list(dict.fromkeys(lines))
    counts = convert_to_list(lines)
    markers = findmarkers(counts)
    
    avgstdfull = findcountavgstd(counts[:-1]) # All revisions
    avgstdset120 = findcountavgstd(counts[markers[0]+1:markers[4]]) # -120 to 120
    avgstdset60 = findcountavgstd(counts[markers[1]+1:markers[3]]) # -60 to 60
    return (avgstdfull, avgstdset120, avgstdset60)

def run_countAnalysis():
    path = 'results/counts/'
    files = os.listdir(path)
    rows_list = []
    for article in files:
        print(article)
        if not article == '.DS_Store' and not article == '.gitignore':
            avgstdfull, avgstdset120, avgstdset60 = analyse_counts(path + article)
            entrydict = {}
            entrydict['Article name'] = article[:-4]
            countslist = ['words', 'references', 'wikilinks']
            for item in countslist:
                entrydict['Avg '+item+ ' of all Revi'] = avgstdfull[0][item]
                entrydict['STD '+item+ ' of all Revi'] = avgstdfull[1][item]
                entrydict['Avg '+item+ ' of 120 frame'] = avgstdset120[0][item]
                entrydict['STD '+item+ ' of 120 frame'] = avgstdset120[1][item]
                entrydict['Avg '+item+ ' of 60 frame'] = avgstdset60[0][item]
                entrydict['STD '+item+ ' of 60 frame'] = avgstdset60[1][item]
            rows_list.append(entrydict)
    
    df = pd.DataFrame(rows_list)
    df.to_csv('AvgStd_counts.csv', encoding='utf-8')

def findmetricavgstd(metrics):
    fre = []
    si = []
    fkg = []
    cli = []
    ari = []
    dcrs = []
    dw = []
    lwf = []
    gf = []
    ts = []
    for entry in metrics:
        if type(entry) != str:
            fre.append(entry['flesch_reading_ease'])
            si.append(entry["smog_index"])
            fkg.append(entry["flesch_kincaid_grade"])
            cli.append(entry["coleman_liau_index"])
            ari.append(entry["automated_readability_index"])
            dcrs.append(entry["dale_chall_readability_score"])
            dw.append(entry["difficult_words"])
            lwf.append(entry["linsear_write_formula"])
            gf.append(entry["gunning_fog"])
            ts.append(entry["text_standard"])

    avgs = {}
    stds = {}
    lists = [fre, si, fkg, cli, ari, dcrs, dw, lwf, gf]
    stringlist = ['fre', 'si', 'fkg', 'cli', 'ari', 'dcrs', 'dw', 'lwf', 'gf']
    try:
        for i, item in enumerate(lists):
            avgs[stringlist[i]] = mean(item)
            stds[stringlist[i]] = std(item)
    except:
        avgs = {'fre': 0, 'si': 0, 'fkg': 0, 'cli': 0, 'ari': 0, 'dcrs': 0, 'dw': 0, 'lwf': 0, 'gf': 0}
        stds = {'fre': 0, 'si': 0, 'fkg': 0, 'cli': 0, 'ari': 0, 'dcrs': 0, 'dw': 0, 'lwf': 0, 'gf': 0}
    return (avgs, stds)

def analyse_metrics(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = list(dict.fromkeys(lines))

    metrics = convert_to_list(lines)
    markers = findmarkers(metrics)

    avgstdfull = findmetricavgstd(metrics[:-1]) # All revisions
    avgstdset120 = findmetricavgstd(metrics[markers[0]+1:markers[4]]) # -120 to 120
    avgstdset60 = findmetricavgstd(metrics[markers[1]+1:markers[3]]) # -60 to 60
    return (avgstdfull, avgstdset120, avgstdset60)

def run_metricsAnalysis():
    path = 'results/metrics/'
    files = os.listdir(path)
    rows_list = []
    for article in files:
        print(article)
        if not article == '.DS_Store' and not article == '.gitignore':
            avgstdfull, avgstdset120, avgstdset60 = analyse_metrics(path + article)
            metricslist = ['fre', 'si', 'fkg', 'cli', 'ari', 'dcrs', 'dw', 'lwf', 'gf']
            entrydict = {}
            entrydict['Article name'] = article[:-4]
            for item in metricslist:
                entrydict['Avg '+item+ ' of all Revi'] = avgstdfull[0][item]
                entrydict['STD '+item+ ' of all Revi'] = avgstdfull[1][item]
                entrydict['Avg '+item+ ' of 120 frame'] = avgstdset120[0][item]
                entrydict['STD '+item+ ' of 120 frame'] = avgstdset120[1][item]
                entrydict['Avg '+item+ ' of 60 frame'] = avgstdset60[0][item]
                entrydict['STD '+item+ ' of 60 frame'] = avgstdset60[1][item]
            rows_list.append(entrydict)
    
    df = pd.DataFrame(rows_list)
    df.to_csv('AvgStd_metrics.csv', encoding='utf-8')

# run_countAnalysis() 
run_metricsAnalysis()