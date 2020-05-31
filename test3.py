import os,json
files = os.listdir('results/counts')
countfiles = []
for item in files:
    countfiles.append(item[:-11].replace('_', ' '))

print(len(countfiles))
with open('completed.txt', 'w', encoding = 'utf-8') as f:
    for item in countfiles:
        f.write(item)
        f.write('\n')
