import json
import csv
##get news id from Feb data
##check accuracy for March data
import os

class MiningFunction():

    def miningFromLog(self, startDate, stopDate):
        currentDate = startDate
        userHistory = dict()
        while currentDate != stopDate:
            logPath = os.path.expanduser('/Users/Taran/Desktop/AmazonKeys/dataStore/data-' + currentDate + '.csv')
            with open(logPath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
            f.close()

def main():
    return
