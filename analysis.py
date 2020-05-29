"""
Finds the slopes of the counts, metrics and ores.
"""

import pandas as pd
from scipy.stats import linregress
import os, sys, json

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#', printEnd = "\r"):

    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s/%s %s%% %s' % (prefix, bar, iteration, total, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()     

def convert_to_list(lines):
    output = []
    for x in lines:
        try:
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

def findcountslopes(counts):
    wikilinks = []
    references = []
    words = []
    for entry in counts:
        if type(entry) != str:
            wikilinks.append(entry['wikilinks'])
            references.append(entry['references'])
            words.append(entry['words'])
    slopes = {}
    try:
        b = [x for x in range(len(words))]
        slopes['words'] = linregress(words, b)[0]
        b = [x for x in range(len(wikilinks))]
        slopes['wikilinks'] = linregress(wikilinks, b)[0]
        b = [x for x in range(len(references))]
        slopes['references'] = linregress(references, b)[0]
    except:
        slopes = {'words' : 0, 'wikilinks' : 0, 'references' : 0}

    return slopes

def analyse_counts(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = list(dict.fromkeys(lines))
    counts = convert_to_list(lines)
    markers = findmarkers(counts)
    
    slopesfull = findcountslopes(counts[:-1]) # All revisions
    slopesset120 = findcountslopes(counts[markers[0]+1:markers[4]]) # -120 to 120
    slopesset60 = findcountslopes(counts[markers[1]+1:markers[3]]) # -60 to 60
    return (slopesfull, slopesset120, slopesset60)

def findmetricsslopes(metrics):
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

    slopes = {}
    lists = [fre, si, fkg, cli, ari, dcrs, dw, lwf, gf]
    stringlist = ['fre', 'si', 'fkg', 'cli', 'ari', 'dcrs', 'dw', 'lwf', 'gf']
    try:
        for i, item in enumerate(lists):
            b = [x for x in range(len(item))]
            slopes[stringlist[i]] = linregress(item, b)[0]
    except:
        slopes = {'fre': 0, 'si': 0, 'fkg': 0, 'cli': 0, 'ari': 0, 'dcrs': 0, 'dw': 0, 'lwf': 0, 'gf': 0}
    return slopes

def analyse_metrics(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = list(dict.fromkeys(lines))

    metrics = convert_to_list(lines)
    markers = findmarkers(metrics)

    slopesfull = findmetricsslopes(metrics) # All revisions
    slopesset120 = findmetricsslopes(metrics[markers[0]+1:markers[4]]) # -120 to 120
    slopesset60 = findmetricsslopes(metrics[markers[1]+1:markers[3]]) # -60 to 60
    return (slopesfull, slopesset120, slopesset60)

def findoresslopes(ores):
    damaging = []
    goodfaith = []
    for entry in ores:
        if type(entry) != str:
            try:
                damaging.append(entry["damaging"]["score"]["probability"]["true"])
                goodfaith.append(entry["goodfaith"]["score"]["probability"]["true"])
            except:
                continue

    slopes = {}
    lists = [damaging, goodfaith]
    stringlist = ['damaging', 'goodfaith']
    try:
        for i, item in enumerate(lists):
            b = [x for x in range(len(item))]
            slopes[stringlist[i]] = linregress(item, b)[0]
    except:
        slopes = {'damaging': 0, 'goodfaith': 0}
    return slopes

def analyse_ores(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = list(dict.fromkeys(lines))

    ores = convert_to_list(lines)
    markers = findmarkers(ores)

    slopesfull = findoresslopes(ores) # All revisions
    slopesset120 = findoresslopes(ores[markers[0]+1:markers[4]]) # -120 to 120
    slopesset60 = findoresslopes(ores[markers[1]+1:markers[3]]) # -60 to 60
    return (slopesfull, slopesset120, slopesset60)

def run_metricsAnalysis():
    dire = 'results/metrics/'
    fileNames = os.listdir(str(dire))
    revilimit = len(fileNames)
    #printProgressBar(0, revilimit, prefix = 'Progress:', suffix = 'Complete', length = 50)
    revi = 0
    for article in fileNames:
        revi += 1
        print(article)
        #printProgressBar(revi, revilimit, prefix = article[:-4], suffix = 'Complete', length = 50)
        if not article == '.DS_Store' and not article == '.gitignore' and not article == 'Mother_Teresa_metrics.txt':
            #counts_slopesets = analyse_counts()
            metrics_slopesets = analyse_metrics(dire + article)
            openfile = open('results/slopes/metrics/'+ article[:-4] + '.txt', 'w', encoding='utf-8')
            for dic in metrics_slopesets:
                    json.dump(dic, openfile) 
                    openfile.write("\n")
        openfile.close()

def run_countsAnalysis():
    dire = 'results/counts/'
    fileNames = os.listdir(str(dire))
    for article in fileNames:
        print(article)
        if not article == '.DS_Store' and not article == '.gitignore' and not article == 'Mother_Teresa_counts.txt':
            metrics_slopesets = analyse_counts(dire + article)
            openfile = open('results/slopes/counts/'+ article[:-4] + '.txt', 'w', encoding='utf-8')
            for dic in metrics_slopesets:
                    json.dump(dic, openfile) 
                    openfile.write("\n")
        openfile.close()

def run_oresAnalysis():
    dire = 'results/ores/'
    fileNames = os.listdir(str(dire))
    for article in fileNames:
        print(article)
        if not article == '.DS_Store' and not article == '.gitignore':
            ores_slopesets = analyse_ores(dire + article)
            openfile = open('results/slopes/ores/'+ article[:-4] + '.txt', 'w', encoding='utf-8')
            for dic in ores_slopesets:
                    json.dump(dic, openfile) 
                    openfile.write("\n")
        openfile.close()

run_metricsAnalysis()
run_countsAnalysis()
# run_oresAnalysis()
