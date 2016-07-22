import os
import argparse
import csv
import time
from datetime import datetime

from textgrid import TextGrid, IntervalTier

now = datetime.now()
date = str(now.year)+str(now.month)+str(now.day)

csv_name = 'comparetextgrids' + date + '.csv'

parser = argparse.ArgumentParser()
parser.add_argument('dir1')
parser.add_argument('dir2')
args = parser.parse_args()
tgdirectory1 = os.path.expanduser(args.dir1)
tgdirectory2 = os.path.expanduser(args.dir2)

print ('hi')

def load_textgrid(path):
    tg = TextGrid()
    try:
        tg.read(path)
    except ValueError as e:
        print('The file {} could not be parsed: {}'.format(path, str(e)))
    return tg

def parse_discourse(path):
    tg = load_textgrid(path)

    #Parse the tiers
    phonesandwordsandsp = []
    sp = []
    for i, ti in enumerate(tg.tiers):
        if ti.name != 'soi':
         #   continue
            intervals = []
            nospintervals = []
            for x in ti:
                intervals.append(x)
            for j in intervals:
                if j.mark.strip() != 'sil':
                    nospintervals.append(j)
                else:
                    sp.append(j)
            for interval in nospintervals:
                if interval.mark.strip() == '':
                    nospintervals.remove(interval)
            phonesandwordsandsp.append(nospintervals)
        else:
            intervals = []
            nospintervals = []
            for x in ti:
                intervals.append(x)
            for j in intervals:
                nospintervals.append(j)
            for interval in nospintervals:
                if interval.mark.strip() == '':
                    nospintervals.remove(interval)
            #print (nospintervals)
            phonesandwordsandsp.append(nospintervals)
    phonesandwordsandsp.append(int(len(sp)/2))
    #print (phonesandwordsandsp)
    return (phonesandwordsandsp)

def WordComparison(a, b):
    if len(a[0]) == len(b[0]):
        phonedifferences = []
        for num in range(0,len(a[0])):
            if a[0][num].minTime > b[0][num].minTime:
                mindiff = a[0][num].minTime - b[0][num].minTime
            else:
                mindiff = b[0][num].minTime - a[0][num].minTime
            if a[0][num].maxTime > b[0][num].maxTime:
                maxdiff = a[0][num].maxTime - b[0][num].maxTime
            else:
                maxdiff = b[0][num].maxTime - a[0][num].maxTime
            phonedifferences.append(mindiff)
            phonedifferences.append(maxdiff)
            #print (a[0][num].mark.strip(), b[0][num].mark.strip(), mindiff, maxdiff)
        totalphonediff = sum(phonedifferences) / len(phonedifferences)
        return totalphonediff
        #print ('Average difference for phones:', totalphonediff)
    else:
        return ('different lengths:', len(a[0]), len(b[0]))

def PhoneComparison(a, b):
    if len(a[1]) == len(b[1]):
        worddifferences = []
        for num in range(0,len(a[1])):
            if a[1][num].minTime > b[1][num].minTime:
                mindiff = a[1][num].minTime - b[1][num].minTime
            else:
                mindiff = b[1][num].minTime - a[1][num].minTime
            if a[1][num].maxTime > b[1][num].maxTime:
                maxdiff = a[1][num].maxTime - b[1][num].maxTime
            else:
                maxdiff = b[1][num].maxTime - a[1][num].maxTime
            worddifferences.append(mindiff)
            worddifferences.append(maxdiff)
            #print (a[1][num].mark.strip(), b[1][num].mark.strip(), mindiff, maxdiff)
        totalworddiff = sum(worddifferences) / len(worddifferences)
        return totalworddiff
        #print ('Average difference for words:', totalworddiff)
    else:
        #print ('different lengths:', len(a[1]), len(b[1]))
        return ('different lengths:', len(a[1]), len(b[1]))

def SpCountComparison(a, b):
    if a[-1] > b[-1]:
        return (a[-1]-b[-1])
        #print ('Difference in silence counts:', a[2]-b[2])
    else:
        return (b[-1]-a[-1])
        #print ('Difference in silence counts:', b[2]-a[2])

def SOIComparison(a, b):
    if len(a) == 4 and len(b) == 4:
        soidifferences = []
        for num in range(0,len(a[2])):
            if a[2][num].minTime > b[2][num].minTime:
                mindiff = a[2][num].minTime - b[2][num].minTime
            else:
                mindiff = b[2][num].minTime - a[2][num].minTime
            if a[2][num].maxTime > b[2][num].maxTime:
                maxdiff = a[2][num].maxTime - b[2][num].maxTime
            else:
                maxdiff = b[2][num].maxTime - a[2][num].maxTime
            soidifferences.append(mindiff)
            soidifferences.append(maxdiff)
            #print (a[1][num].mark.strip(), b[1][num].mark.strip(), mindiff, maxdiff)
        totalsoidiff = sum(soidifferences) / len(soidifferences)
        return totalsoidiff
        #print ('Average difference for words:', totalworddiff)

firstdir = []
for root, dirs, files in os.walk(tgdirectory1):
    for name in files:
        tgfile1 = os.path.join(root, name)
        if tgfile1.endswith('TextGrid'):
            firstdir.append(tgfile1)
print (len(firstdir))

seconddir = []
for root, dirs, files in os.walk(tgdirectory2):
    for name in files:
        tgfile2 = os.path.join(root, name)
        if tgfile2.endswith('TextGrid'):
            seconddir.append(tgfile2)
print (len(seconddir))

csv_columns = ['tg','Average difference for words','Average difference for phones', 'Average difference for SOI', 'Difference in silence counts']  

firstdirfiles = []
for num in firstdir:
    dog = num.split('/')
    if dog[-2] != '0_oldTextGrids':
        firstdirfiles.append((dog[-1], num))
#print (firstdirfiles)

seconddirfiles = []
for num in seconddir:
    dog = num.split('/')
    if dog[-2] != '0_oldTextGrids':
        seconddirfiles.append((dog[-1], num))

#for num in range(0, len(firstdir)):
for num1 in firstdirfiles:
    for num2 in seconddirfiles:
        if num1[0] == num2[0]:
            a = parse_discourse(num1[1])
            b = parse_discourse(num2[1])
        #parse_discourse(firstdir[0])
            fdn = num1[0]
            wc = WordComparison(a, b)
            pc = PhoneComparison(a, b)
            soic = SOIComparison(a, b)
            sp = SpCountComparison(a, b)        

            dict_data = [
                {'tg': fdn, 'Average difference for words': wc, 'Average difference for phones': pc, 'Average difference for SOI': soic, 'Difference in silence counts': sp}
                ]

            if not os.path.exists(csv_name):
                open(csv_name, 'a')
                with open(csv_name, 'a') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                    writer.writeheader()

            with open(csv_name, 'a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                writer.writerow(dict_data[0])
