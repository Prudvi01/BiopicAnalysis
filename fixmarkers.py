import json
import xmltodict
import datetime
import requests
import time
import textstat
import mwparserfromhell
import pandas as pd
import matplotlib.pyplot as plt
from oresapi import Session
import sys
import wikipedia as wp

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

def cleanmarkers(ores):
    for item in ores:
        if type(item) == str:
            ores.remove(item)
    return ores

def dateDifference(APIDate, RevisionDate) :
    ''' 
    The format of data we get from KnolML is different from the one
    we get using IMDB API, this function converts thm to a common
    format and calculates the difference.
    -30 means 30 days before release, +30 means 30 days after
    '''
    converter = {"Jan":'1', "Feb":'2', "Mar":'3', "Apr":'4', 
            "May":'5', "Jun":'6', "Jul":'7', "Aug":'8',
            "Sep":'9', "Oct":'10', "Nov":'11', "Dec":'12'}
    date = APIDate.split()
    date[1] = date[1].replace(date[1], converter[date[1]])
    date = list(map(int, date[::-1]))
    APIdate = datetime.datetime(date[0], date[1], date[2])
    date = RevisionDate
    date = list(map(int, date.split('-')))
    RevisionDate = datetime.datetime(date[0], date[1], date[2])
    return (RevisionDate-APIdate).days, APIdate, RevisionDate    

def getores(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = list(dict.fromkeys(lines))
    ores = convert_to_list(lines)
    ores = cleanmarkers(ores)
    return ores

def fixmarkers(name, date, di, ores):
    revisions = [x for x in di['page']['revision']] #list of all articles for a movie
    revs = [] # Batch of revisions for ORES Analysis
    #metrics = [] # List of metrics dictionaries
    #counts = [] # List of counts dictionaries
    #sha1 = {} # Tracks the sha1 values to count reverts
    revi = 0 
    revilimit = len(revisions)
    printProgressBar(0, revilimit, prefix = 'Progress:', suffix = 'Complete', length = 50)
    breaker = [0, 0, 0, 0, 0] # Used to maintain flags 

    for i in range(0, revilimit) :
        revi += 1
        printProgressBar(revi, revilimit, prefix = name, suffix = 'Complete', length = 50)
        sha1Value = revisions[i]['sha1'] 
        
        diff, APIdate, RevisionDate = dateDifference(date, revisions[i]['timestamp'].split('T')[0])
        if RevisionDate > APIdate:
            if breaker[0] == 0:
                breaker[0] = 1
                ores.insert(i, 'reviafterrelease')
                reviafterrelease = i # First revision after release
                firstrevidateafterelease = RevisionDate # Revision date afte the movie release

        '''
        if diff < -200 :
            continue
        '''
        if diff > -120 and diff < -60:
            if breaker[1] == 0:
                breaker[1] = 1
                ores.insert(i, '120 days start')

        if diff >= -60:
            if breaker[2] == 0:
                breaker[2] = 1
                ores.insert(i, '60 days start')

        if diff > 60:
            if breaker[3] == 0:
                breaker[3] = 1
                ores.insert(i, '60 days end')
        
        if diff > 120:
            if breaker[4] == 0:
                breaker[4] = 1
                ores.insert(i, '120 days end')

    return ores

def getEachArticle():
    '''
    	This is the driver function, it gets the name of all biopics from MovieDetails.json
    	and their release dates from ReleaseDates from releaseDates.json. Both these files
    	are available in the repository.
    	For each biopic, it performs proper analysis
    '''
    with open("MovieDetails.json",'r') as f :
        movieDetails = json.loads(f.read())
    
    movieNames = [x for x in movieDetails.keys()]

    with open("releaseDates.json",'r') as f :
        dates = json.loads(f.read())

    #name = "Walt Before Mickey||/wiki/Walt_Before_Mickey"
    for MovieName in movieNames:
        completedfile = open("completedfixingmarkers.txt", "r")
        completed = completedfile.readlines()
        completedfile.close()
        if not (MovieName + '\n') in completed:  
            for i in range(len(movieDetails[MovieName])):
                namefordate = MovieName.split('||')[0] # "Walt Before Mickey"
                name, url = list(movieDetails[MovieName][i].keys())[0].split('||')
                name = wp.search(name)[0]
                date = dates[namefordate] if namefordate in dates else "--" 
                print(name, date)
                if date != "--": # because we couldn't get all release dates using IMDB API
                    article = "dataset/" + name.replace(' ','_') + ".xml"
                    try:
                        with open(article, 'r', encoding="utf-8") as f :
                            di = xmltodict.parse(f.read())                    
                    except:
                        print('File not found!', article)
                        with open('filesnotfound.txt', 'a', encoding='utf-8') as f:
                            f.write(name + '\n')
                        continue
                    try:
                        ores = getores('results/ores/'+ name.replace(' ', '_') + '_ores.txt')
                        ores = fixmarkers(name, date, di, ores)
                        ores_file = open('results/ores/'+ name.replace(' ', '_') + '_ores.txt', 'w', encoding='utf-8')
                        for dic in ores:
                            if type(dic) != str:
                                json.dump(dic, ores_file) 
                                ores_file.write("\n")
                            else:
                                ores_file.write(dic + '\n')
                        ores_file.close()
                    except:
                        continue

                    # allORES, metrics, counts = AnalyzeValidEdits(name, date, di) #vaild means before and after 60 days
                    #savethese(allORES, metrics, counts, name)
                else:
                    print('Skipping ' + MovieName + '. No date found')
                print('')
                f = open("completedfixingmarkers.txt", "a")
                f.write(MovieName + '\n')
                f.close()
                print("Article "+ MovieName +" is done:")
            
        else:
            print('Skipping ' + MovieName)

getEachArticle()