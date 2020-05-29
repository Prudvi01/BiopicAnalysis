"""
Finds the difference between the slopes of windows
of size 60 and 120.
"""
import pandas as pd
from scipy.stats import linregress
import os, sys, json

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
            try:    
                wikilinks.append(entry['wikilinks'])
                references.append(entry['references'])
                words.append(entry['words'])
            except:
                continue
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
    slopeswindows60 = []
    # print(counts[0:60])
    for i, count in enumerate(counts[:-1]):
        slopeswindows60.append(findcountslopes(counts[i:i + 60]))

    slopeswindows120 = []
    for i, count in enumerate(counts[:-1]):
        slopeswindows120.append(findcountslopes(counts[i:i + 120]))

    markerwindows60 = [0, 0, 0] # Finding the index of windows containing the markers
    markerwindows120 = [0, 0, 0] # Finding the index of windows containing the markers
    
    # Finding the windows where the markers are present for slopeswindows60
    markerwindows60[0] = markers[1]//60 +  1 # -60 
    markerwindows60[1] = markers[2]//60 +  1 # movie release
    markerwindows60[2] = markers[3]//60 +  1 # 60

    # Finding the windows where the markers are present for slopeswindows120
    markerwindows120[0] = markers[0]//120 +  1 # -120 
    markerwindows120[1] = markers[2]//120 +  1 # movie release
    markerwindows120[2] = markers[4]//120 +  1 # 120


    # print(markerwindows60)
    # Marking the list of dictionaries of windows with markers for windows of 60 
    for i, item in enumerate(slopeswindows60):   
        if i == markerwindows60[1] - 1: # movie release
            item['status'] = '60 before release'
            continue    
        if i == markerwindows60[1] + 1: # movie release
            item['status'] = '60 after release'
            continue     
        # for every other window
        item['status'] = 'None'

    # Marking the list of dictionaries of windows with markers for windows of 120
    for i, item in enumerate(slopeswindows120):
        if i == markerwindows120[1] - 1: # movie release
            item['status'] = '120 before release'
            continue    
        if i == markerwindows120[1] + 1: # movie release
            item['status'] = '120 after release'
            continue   
        # for every other window
        item['status'] = 'None'

    return (slopesfull, slopesset120, slopesset60, slopeswindows60, slopeswindows120)

def run_countsAnalysis():
    dire = 'results/counts/'
    fileNames = os.listdir(str(dire))
    for article in fileNames:
        print(article)
        if not article == '.DS_Store' and not article == '.gitignore' and not article == 'Mother_Teresa_counts.txt':
            metrics_slopesets = analyse_counts(dire + article)
            openfile = open('results/slopeswindows/counts/'+ article[:-4] + '.txt', 'w', encoding='utf-8')
            for dic in metrics_slopesets[:-2]:
                json.dump(dic, openfile) 
                openfile.write("\n")
            item = metrics_slopesets[3]
            json.dump(sorted(item, key = lambda i: i['words']), openfile) 
            openfile.write("\n")
            json.dump(sorted(item, key = lambda i: i['wikilinks']), openfile) 
            openfile.write("\n")
            json.dump(sorted(item, key = lambda i: i['references']), openfile) 
            openfile.write("\n")

            item = metrics_slopesets[4]
            json.dump(sorted(item, key = lambda i: i['words']), openfile) 
            openfile.write("\n")
            json.dump(sorted(item, key = lambda i: i['wikilinks']), openfile) 
            openfile.write("\n")
            json.dump(sorted(item, key = lambda i: i['references']), openfile) 
            openfile.write("\n")
        openfile.close()

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
            try:
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
            except:
                continue
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
    slopeswindows60 = []
    # print(counts[0:60])
    for i, count in enumerate(metrics[:-1]):
        slopeswindows60.append(findmetricsslopes(metrics[i:i + 60]))

    slopeswindows120 = []
    for i, count in enumerate(metrics[:-1]):
        slopeswindows120.append(findmetricsslopes(metrics[i:i + 120]))

    markerwindows60 = [0, 0, 0] # Finding the index of windows containing the markers
    markerwindows120 = [0, 0, 0] # Finding the index of windows containing the markers
    
    # Finding the windows where the markers are present for slopeswindows60
    markerwindows60[0] = markers[1]//60 +  1 # -60 
    markerwindows60[1] = markers[2]//60 +  1 # movie release
    markerwindows60[2] = markers[3]//60 +  1 # 60

    # Finding the windows where the markers are present for slopeswindows120
    markerwindows120[0] = markers[0]//120 +  1 # -120 
    markerwindows120[1] = markers[2]//120 +  1 # movie release
    markerwindows120[2] = markers[4]//120 +  1 # 120


    # print(markerwindows60)
    # Marking the list of dictionaries of windows with markers for windows of 60 
    for i, item in enumerate(slopeswindows60):   
        if i == markerwindows60[1] - 1: # movie release
            item['status'] = '60 before release'
            continue    
        if i == markerwindows60[1] + 1: # movie release
            item['status'] = '60 after release'
            continue     
        # for every other window
        item['status'] = 'None'

    # Marking the list of dictionaries of windows with markers for windows of 120
    for i, item in enumerate(slopeswindows120):
        if i == markerwindows120[1] - 1: # movie release
            item['status'] = '120 before release'
            continue    
        if i == markerwindows120[1] + 1: # movie release
            item['status'] = '120 after release'
            continue   
        # for every other window
        item['status'] = 'None'

    return (slopesfull, slopesset120, slopesset60, slopeswindows60, slopeswindows120)

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
            openfile = open('results/slopeswindows/metrics/'+ article[:-4] + '.txt', 'w', encoding='utf-8')
            for dic in metrics_slopesets[:-2]:
                json.dump(dic, openfile) 
                openfile.write("\n")
            item = metrics_slopesets[3]
            metriclist = ["fre", "si", "fkg", "cli", "ari", "dcrs", "dw", "lwf", "gf"]
            for x in metriclist:
                json.dump(sorted(item, key = lambda i: i[x]), openfile) 
                openfile.write("\n")

            item = metrics_slopesets[4]
            for x in metriclist:
                json.dump(sorted(item, key = lambda i: i[x]), openfile) 
                openfile.write("\n")
        openfile.close()

run_countsAnalysis()
run_metricsAnalysis()