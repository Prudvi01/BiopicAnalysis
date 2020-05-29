
'''
import json


with open('filesnotfound.txt', 'r') as f:
    filesnotfound = f.readlines()
    filesnotfound = list(dict.fromkeys(filesnotfound))

with open('filenames.txt', 'r') as f:
    filenames = f.readlines()
    filenames = list(dict.fromkeys(filenames))
filenames = [x.replace('_', ' ')[:-5] for x in filenames]
count = 0
print(filenames[0])
for item in filesnotfound:
    if item in filenames:
        count +=1
print(count)

print(len(mylist))

with open('filesnotfound.txt', 'w') as f:
    for item in mylist:
        f.write("%s" % item)
   
with open("releaseDates.json",'r') as f :
    dates = json.loads(f.read())

for name in dates.keys():
    if dates[name][-4:] == '--':
        continue
    if int(dates[name][-4:]) < 2001:
        print(name)
'''

print('TEST 2')