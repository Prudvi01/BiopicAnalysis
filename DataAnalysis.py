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


#reload(sys)
#sys.setdefaultencoding('utf8')

# allORES = [] # will store ORES scores for all revisions

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

def updateORES(revids): 
    '''
    Uses API to get the scores of a "batch of revisions", optimal batch size is 50
    '''
    '''
    url = "https://ores.wikimedia.org/v3/scores/enwiki/?revids=" + str(revid)
    page = requests.get(url)
    di = json.loads(page.text)
    '''
    my_session = Session("https://ores.wikimedia.org", user_agent="Demonstrating how to use Session - my_address@email.com")
    results = my_session.score("enwiki", ["damaging", "goodfaith"], revids)
    
    for rev_id, result in zip(revids, results):
        allORES.append(result)

def getReadabilityMetrics(test_data) : 
    '''
    for a given article IN TEXT FORMAT, returns its readability metrics
    Uses textstat library, please install it
    '''
    metric = {"flesch_reading_ease" : textstat.flesch_reading_ease(test_data),
                "smog_index" : textstat.smog_index(test_data),
                "flesch_kincaid_grade" : textstat.flesch_kincaid_grade(test_data),
                "coleman_liau_index" : textstat.coleman_liau_index(test_data),
                "automated_readability_index" : textstat.automated_readability_index(test_data),
                "dale_chall_readability_score" : textstat.dale_chall_readability_score(test_data),
                "difficult_words" : textstat.difficult_words(test_data),
                "linsear_write_formula" : textstat.linsear_write_formula(test_data),
                "gunning_fog" : textstat.gunning_fog(test_data),
                "text_standard" : textstat.text_standard(test_data)}
    return metric

def getCounts(text) :
    '''
    for a given article in TEXT format, returns its wikilinks, references and 
    word count in a dictionary
    '''
    code = mwparserfromhell.parse(text)
    di = { "wikilinks" : len(code.filter_wikilinks()),
          "references" : text.count("<ref>"),
          "words" : text.count(" ")}
    return di

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

def plotmetrics(metrics):
    # Plotting Metrics
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
    article_name = 'Walt_Disney_Metrics'
    startrevi = metrics.index('startrevi')
    endrevi = metrics.index('endrevi')
    reviafterrelease = metrics.index('reviafterrelease')
    metrics.remove('reviafterrelease')
    metrics.remove('startrevi')
    metrics.remove('endrevi')
    for entry in metrics:
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

    plt.style.use('fivethirtyeight')
    plt.plot(fre, label='flesch_reading_ease', linewidth= 1.5)
    plt.plot(si, label="smog_index", linewidth= 1.5)
    plt.plot(fkg, label="flesch_kincaid_grade", linewidth= 1.5)
    plt.plot(cli, label="coleman_liau_index", linewidth= 1.5)
    plt.plot(ari, label="automated_readability_index", linewidth= 1.5)
    plt.plot(dcrs, label="dale_chall_readability_score", linewidth= 1.5)
    plt.plot(lwf, label="linsear_write_formula", linewidth= 1.5)
    plt.plot(gf, label="gunning_fog", linewidth= 1.5)
    
    plt.axvline(x=startrevi,color='red', linewidth= 1.5)
    plt.axvline(x=endrevi,color='red', linewidth= 1.5)
    plt.axvline(x=reviafterrelease, color='gray',linestyle='--', linewidth= 1.5)
    #plt.plot(ts, label="text_standard", linewidth= 1.5)
    #plt.plot(dw, label="difficult_words", linewidth= 1.5)
    
    plt.suptitle(article_name, fontsize = 16)
    plt.xlabel("Revisions")
    plt.ylabel('Score')
    plt.legend(fontsize=8)
    plt.savefig('results/metrics/'+article_name+'.png',bbox_inches = "tight",dpi=800)
    
    plt.show()

def plotcounts(counts):
    words = []
    references = []
    wikilinks = []
    startrevi = counts.index('startrevi')
    endrevi = counts.index('endrevi')
    reviafterrelease = counts.index('reviafterrelease')
    counts.remove('reviafterrelease')
    counts.remove('startrevi')
    counts.remove('endrevi')
    for entry in counts:
        words.append(entry["words"])
        references.append(entry['references'])
        wikilinks.append(entry['wikilinks'])
    article_name = 'Walt_Disney_Counts'
    plt.style.use('fivethirtyeight')
    #plt.plot(words, label='words', linewidth= 1.5)
    plt.plot(references, label='references', linewidth= 1.5)
    plt.plot(wikilinks, label='wikilinks', linewidth= 1.5)
    plt.suptitle(article_name, fontsize = 16)
    plt.xlabel("Revisions")
    plt.ylabel('Counts')
    plt.axvline(x=startrevi,color='red', linewidth= 1.5)
    plt.axvline(x=endrevi,color='red', linewidth= 1.5)
    plt.axvline(x=reviafterrelease, color='gray',linestyle='--', linewidth= 1.5)
    plt.legend(fontsize=8)
    plt.savefig('results/counts/'+article_name+'.png',bbox_inches = "tight",dpi=800)
    
    plt.show()

def plotores(allORES):
    damaging = []
    goodfaith = []
    startrevi = allORES.index('startrevi')
    endrevi = allORES.index('endrevi')
    reviafterrelease = allORES.index('reviafterrelease')
    allORES.remove('reviafterrelease')
    allORES.remove('startrevi')
    allORES.remove('endrevi')
    article_name = 'Walt_Disney_ORES'
    for entry in allORES:
        damaging.append(entry['damaging']['score']['probability']['true'])
        goodfaith.append(entry['goodfaith']['score']['probability']['true'])
    
    plt.style.use('fivethirtyeight')
    plt.plot(damaging, label='references', linewidth= 1.5)
    plt.plot(goodfaith, label='wikilinks', linewidth= 1.5)
    plt.suptitle(article_name, fontsize = 16)
    plt.xlabel("Revisions")
    plt.ylabel('allORES')
    plt.axvline(x=startrevi,color='red', linewidth= 1.5)
    plt.axvline(x=endrevi,color='red', linewidth= 1.5)
    plt.axvline(x=reviafterrelease, color='gray',linestyle='--', linewidth= 1.5)
    plt.legend(fontsize=8)
    plt.savefig('results/ores/'+article_name+'.png',bbox_inches = "tight",dpi=800)
    plt.show()

def plottheseforchristsake(allORES, metrics, counts):
    plotmetrics(metrics)
    plotcounts(counts)
    plotores(allORES)

def savethese(metrics, counts, name):
    name = name.replace(' ', '_')
    print(name)
    # ores_file = open('results/ores/'+ name + '_ores.txt', 'w', encoding='utf-8')
    counts_file = open('results/counts/'+ name + '_counts.txt', 'w', encoding='utf-8')
    metrics_file = open('results/metrics/'+ name + '_metrics.txt', 'w', encoding='utf-8')
    '''
    for dic in allORES:
        if type(dic) != str:
            json.dump(dic, ores_file) 
            ores_file.write("\n")
        else:
            ores_file.write(dic + '\n')
    '''

    for dic in metrics:
        if type(dic) != str:
            json.dump(dic, metrics_file) 
            metrics_file.write("\n")
        else:
            metrics_file.write(dic + '\n')
    
    for dic in counts:
        if type(dic) != str:
            json.dump(dic, counts_file) 
            counts_file.write("\n")
        else:
            counts_file.write(dic + '\n')

    # ores_file.close()
    metrics_file.close()
    counts_file.close()

def AnalyzeValidEdits(name, date, di):
    '''
    Valid edits means the ones within a period of 2 months
    For each valid edit, it does the following 3 tasks
    1) Get its ORES score
    2) Get its readability metrics
    3) Count wikilinks, references and number of words
    '''
    
    revisions = [x for x in di['page']['revision']] #list of all articles for a movie
    revs = [] # Batch of revisions for ORES Analysis
    metrics = [] # List of metrics dictionaries
    counts = [] # List of counts dictionaries
    sha1 = {} # Tracks the sha1 values to count reverts
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
                metrics.append('reviafterrelease')
                counts.append('reviafterrelease')
                # allORES.append('reviafterrelease')
                reviafterrelease = i # First revision after release
                firstrevidateafterelease = RevisionDate # Revision date afte the movie release

        '''
        if diff < -200 :
            continue
        '''
        if diff > -120 and diff < -60:
            if breaker[1] == 0:
                breaker[1] = 1
                metrics.append('120 days start')
                counts.append('120 days start')
                # allORES.append('120 days start')

        if diff >= -60:
            if breaker[2] == 0:
                breaker[2] = 1
                metrics.append('60 days start')
                counts.append('60 days start')
                # allORES.append('60 days start')

        if diff > 60:
            if breaker[3] == 0:
                breaker[3] = 1
                metrics.append('60 days end')
                counts.append('60 days end')
                # allORES.append('60 days end')
        
        if diff > 120:
            if breaker[4] == 0:
                breaker[4] = 1
                metrics.append('120 days end')
                counts.append('120 days end')
                # allORES.append('120 days end')
                
        '''
        if diff > 200:
            updateORES(revids)
            break
        '''
        try:
            metrics.append(getReadabilityMetrics(revisions[i]['text']['#text']))
            counts.append(getCounts(revisions[i]['text']['#text']))
            revs.append(revisions[i]['id'])
        except:
            pass
        
        '''
        if len(revs) >= 50 : # since ORES scores are to be calculated in batches of 50s
            revids = [int(x) for x in revs] #str(revs).replace(', ','|')[1:-1].replace("'","")
            revs = []
            updateORES(revids)
        '''
        try:
            if sha1[sha1Value]:
                sha1[sha1Value] += 1
        except:
            sha1[sha1Value] = 1
    counts.append(sha1)
    
    
    #plottheseforchristsake(allORES, metrics, counts)
    return metrics, counts
    
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
        completedfile = open("completed.txt", "r")
        completed = completedfile.readlines()
        completedfile.close()
        # if not (MovieName + '\n') in completed:  
        for i in range(len(movieDetails[MovieName])):
            namefordate = MovieName.split('||')[0] # "Walt Before Mickey"
            name, url = list(movieDetails[MovieName][i].keys())[0].split('||')
            name = wp.search(name)[0]
            date = dates[namefordate] if namefordate in dates else "--" 
            if not (name + '\n') in completed:
                print(name, date)
                try:
                    if date != "--": #because we couldn't get all release dates using IMDB API
                        article = r"dataset/" + name.replace(' ', '_') + ".xml"
                        try:
                            with open(article, 'r', encoding="utf-8") as f :
                                di = xmltodict.parse(f.read())                    
                        except:
                            print('File not found!', article)
                            article = r"dataset/" + name + ".xml"
                            print('trying ', article)
                            try:
                                with open(article, 'r', encoding="utf-8") as f :
                                    di = xmltodict.parse(f.read()) 
                            except:    
                                print('File not found!', article)
                                with open('filesnotfound.txt', 'a', encoding='utf-8') as f:
                                    f.write(name + '\n')
                                continue
                        metrics, counts = AnalyzeValidEdits(name, date, di) # vaild means before and after 60 days
                        savethese(metrics, counts, name)
                    else:
                        print('Skipping ' + MovieName + '. No date found')
                    print('')
                    f = open("completed.txt", "a")
                    f.write(MovieName + '\n')
                    f.close()
                    print("Article "+ MovieName +" is done:")
                except:
                    print('Some error while analysing file ' + str(name.replace(' ','_')) + ".xml. Skipping!")
            else:
                print('Skipping ' + name)
        print(MovieName.split('||', ' ')[0] + ' is completed')

        
'''
    for movie in movieNames :
        name, url = movie.split('||')
        date = dates[name] if name in dates else "--" 
        print(name, date)
        if date != "--" : #because we couldn't get all release dates using IMDB API
            AnalyzeValidEdits(name, date) #vaild means before and after 60 days
        break
    '''
startTime = time.time()
getEachArticle()
endTime = time.time()
print("TIME ELAPSED = " + str(endTime - startTime))