def convert_to_list(lines):
    output = []
    for x in lines:
        try:
            output.append(eval(x[:-1]))
        except:
            x = x.replace('NaN', '0')
            output.append(eval(x[:-1]))
    return output

def y_of_x(x):
    return [y for y in range(len(x))]

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

def dictdiff(dict1, dict2):
    '''
    Obviously only works if both dicts have the same keys
    Returns list of differences dict1 - dict2
    '''
    diff = []
    for key in dict1.keys():
        diff.append(dict1[key] - dict2[key])
    return diff