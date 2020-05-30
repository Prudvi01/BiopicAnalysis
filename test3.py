'''
fix the filenames in dataset/
'''
import os
dire = 'dataset/'
filenames = os.listdir(dire)

for filename in filenames:
    os.rename(dire + filename, dire + filename.replace(' ', '_'))
    print(filename)