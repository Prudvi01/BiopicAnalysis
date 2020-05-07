import json
import xmltodict
import datetime
import requests
import time
import textstat
import mwparserfromhell
import pandas as pd
import matplotlib.pyplot as plt

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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

def getORES(revid): 
    '''
    Uses API to get the scores of a "batch of revisions", optimal batch size is 50
    '''
    url = "https://ores.wikimedia.org/v3/scores/enwiki/?revids=" + str(revid)
    page = requests.get(url)
    di = json.loads(page.text)
    return di['enwiki']['scores']

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
    plt.savefig('results/metrics/'+article_name+'error.png',bbox_inches = "tight",dpi=800)
    
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
        


def plottheseforchristsake(allORES, metrics, counts):
    plotmetrics(metrics)
    plotcounts(counts)




def AnalyzeValidEdits(name, date):
    '''
    Valid edits means the ones within a period of 2 months
    For each valid edit, it does the following 3 tasks
    1) Get its ORES score
    2) Get its readability metrics
    3) Count wikilinks, references and number of words
    '''
    article = "testData/" + name.replace(' ','_') + ".xml"
    with open(article, 'r') as f :
        di = xmltodict.parse(f.read())
    
    revisions = [x for x in di['page']['revision']] #list of all articles for a movie
    revs = [] #Batch of revisions for ORES Analysis
    allORES = [] #will store ORES scores for all revisions
    metrics = []
    counts = []
    revi = 0
    revilimit = len(revisions)
    article_name = 'Walt_Disney'
    printProgressBar(0, revilimit, prefix = 'Progress:', suffix = 'Complete', length = 50)
    breaker = 0
    breaker1 = 0
    breaker2 = 0

    for i in range(0, revilimit) :
        revi += 1
        printProgressBar(revi, revilimit, prefix = article_name, suffix = 'Complete', length = 50)
        diff, APIdate, RevisionDate = dateDifference(date, revisions[i]['timestamp'].split('T')[0])
        if RevisionDate > APIdate:
            if breaker == 0:
                breaker = 1
                metrics.append('reviafterrelease')
                counts.append('reviafterrelease')
                reviafterrelease = i # First revision after release
                firstrevidateafterelease = RevisionDate # Revision date afte the movie release
        if diff < -60 :
            continue
        if diff > -60:
            if breaker1 == 0:
                breaker1 = 1
                metrics.append('startrevi')
                counts.append('startrevi')
        if diff > 60:
            if breaker2 == 0:
                breaker2 = 1
                metrics.append('endrevi')
                counts.append('endrevi')
        if diff > 60:
            allORES.append(getORES(revids))
            break

        
        
        #print(i, end=',')
        try:
            metrics.append(getReadabilityMetrics(revisions[i]['text']['#text']))
            counts.append(getCounts(revisions[i]['text']['#text']))
            revs.append(revisions[i]['id'])
        except:
            pass
        
        if len(revs) >= 50 : #since ORES scores are to be calculated in batches of 50s
            revids = str(revs).replace(', ','|')[1:-1].replace("'","")
            revs = []
            allORES.append(getORES(revids))
    print(allORES[0])
    print(reviafterrelease)
    print(firstrevidateafterelease)
    plottheseforchristsake(allORES, metrics, counts)
    return allORES
    
def getEachArticle() :
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

    name = "Walt Before Mickey||/wiki/Walt_Before_Mickey"
    
    i = 0
    namefordate = "Walt Before Mickey"
    print(list(movieDetails[name][i].keys())[i].split('||'))
    name, url = list(movieDetails[name][i].keys())[i].split('||')
    date = dates[namefordate] if namefordate in dates else "--" 
    print(name, date)
    if date != "--" : #because we couldn't get all release dates using IMDB API
        output = AnalyzeValidEdits(name, date) #vaild means before and after 60 days
        
    df = pd.DataFrame(output) 
    df.to_csv(name + '.csv', index=False)
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