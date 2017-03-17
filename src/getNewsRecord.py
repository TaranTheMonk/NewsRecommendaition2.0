import os
import time
from datetime import datetime
import csv
import re


class TimeFunction():

    def oneMoreDay(self, previousDay):
        currentValue = time.mktime(time.strptime(previousDay, "%Y-%m-%d"))
        currentValue += 24*60*60
        future = datetime.strftime(datetime.fromtimestamp(currentValue), "%Y-%m-%d")
        return future

def minLog(startDate, stopDate):
    timeFunction = TimeFunction()
    currentDate = startDate
    newsDetailPattern = re.compile('news/\d+$')
    userNewsCollection = dict()

    while currentDate != stopDate:
        path = os.path.expanduser('/Users/Taran/Desktop/AmazonKeys/dataStore/data-' + currentDate + '.csv')
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(line.replace('\0','') for line in f)
            for row in reader:
                if newsDetailPattern.search(row[1]):
                    newsId = int(row[1].split('/')[-1])
                    recordTime = row[4][:10]
                    if not row[5] in userNewsCollection.keys():
                        userNewsCollection[row[5]] = list()
                    userNewsCollection[row[5]].append((newsId, recordTime))
        f.close()
        print(currentDate)
        currentDate = timeFunction.oneMoreDay(currentDate)
    return userNewsCollection