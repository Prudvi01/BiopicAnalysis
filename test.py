import json
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

with open("MovieDetails.json",'r') as f :
    movieDetails = json.loads(f.read())

moviekeys = [x for x in movieDetails.keys()]
movieNames = []
for movie in moviekeys:
    name, url = movie.split('||')
    movieNames.append(name)
print("Number of MovieDetails = " + str(len(movieNames)))
with open("releaseDates.json",'r') as f :
     dates = json.loads(f.read())

datekeys = [x for x in dates.keys()]
print("Number of releaseDates = " + str(len(datekeys)))
notnull = 0
notnulllist = []
for date in dates.keys():
    
    if dates[date] != 'N/A':
        notnull += 1
        notnulllist.append(date)
print("Number of notnull = " + str(notnull))
count  = 0
common = []
for name in datekeys:
    if name in movieNames:
        count += 1
        common.append(name)


print("Number of common = " + str(count))
usable = intersection(common, notnulllist)
print("Total useable = " + str(len(usable)))

with open("useable.txt", "a") as f:
    for name in usable:
        f.write(name + '\n')

        