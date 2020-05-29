# import os,json
# files = os.listdir('results/counts')
# countfiles = []
# for item in files:
#     countfiles.append(item[:-11].replace('_', ' '))

# with open("MovieDetails.json",'r') as f :
#     movieDetails = json.loads(f.read())

# movieNames = [x for x in movieDetails.keys()]
# movievalues = [x for x in movieDetails.values()]
# completedfiles = []
# for item in movieDetails.keys():
#     personactordictlist = movieDetails[item]
#     for eachdict in personactordictlist:
#         eachdictkeys = eachdict.keys()
#         for eachkey in eachdictkeys:
#             if eachkey.split('||')[0] in countfiles:
#                 completedfiles.append(item)

# print(len(completedfiles))
# with open('completed.txt', 'w', encoding = 'utf-8') as f:
#     for item in completedfiles:
#         f.write(item)
#         f.write('\n')

# print([x for x in movievalues[0][0].keys()][0].split('||')[0])

print('TEST 3')