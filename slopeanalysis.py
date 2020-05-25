"""
Finds the difference between the slopes of all revisions,
60 and 120 frames.
"""


from helper import convert_to_list, printProgressBar, y_of_x, dictdiff
import os, io

def countslopes():
    countslopesfile = open('countslopes.txt', 'w', encoding="utf-8")
    files = os.listdir('results/slopes/counts/')
    for filename in files:
        if filename != '.DS_Store' and filename != '.gitignore':
            with io.open('results/slopes/counts/' + filename, 'r') as f:
                lines = f.readlines()
                countslopes = convert_to_list(lines)

        revall = countslopes[0]
        rev60 = countslopes[1]
        rev120 = countslopes[2]
        # print(countslopes)
        dictdiff60 = dictdiff(rev60, revall)
        dictdiff120 = dictdiff(rev120, revall)
        countslopesfile.write(filename[:-4] + '\n')
        countslopesfile.write(str(dictdiff60) + '\n')
        countslopesfile.write(str(dictdiff120) + '\n')
        # print(dictdiff(rev60, revall))
        # print(dictdiff(rev120, revall))

    countslopesfile.close()

def metricslopes():
    metricslopesfile = open('metricslopes.txt', 'w', encoding="utf-8")
    files = os.listdir('results/slopes/metrics/')
    for filename in files:
        if filename != '.DS_Store' and filename != '.gitignore':
            with io.open('results/slopes/metrics/' + filename, 'r') as f:
                lines = f.readlines()
                countslopes = convert_to_list(lines)

        revall = countslopes[0]
        rev60 = countslopes[1]
        rev120 = countslopes[2]
        # print(countslopes)
        dictdiff60 = dictdiff(rev60, revall)
        dictdiff120 = dictdiff(rev120, revall)
        metricslopesfile.write(filename[:-4] + '\n')
        metricslopesfile.write(str(dictdiff60) + '\n')
        metricslopesfile.write(str(dictdiff120) + '\n')
        # print(dictdiff(rev60, revall))
        # print(dictdiff(rev120, revall))

    metricslopesfile.close()

metricslopes()