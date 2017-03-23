from mysql import connector
import json
import sys
import pandas as pd
import numpy as np
from scipy import sparse
from sklearn import metrics
from matplotlib import pyplot as plt


class SqlFunction():

    def getUserHistory(self):
        conn = connector.connect(host='hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='HSDBADMIN', password='NestiaHSPWD', database='recommend_system')
        cursor = conn.cursor()
        cursor.execute('select device_id, history from user_news_profile')
        queryResult = cursor.fetchall()
        cursor.close()
        conn.close()
        print('Get user history successfully')

        output = {}
        scale = len(queryResult)
        counter = 0
        for item in queryResult:
            deviceId = item[0].decode('utf-8')
            history = json.loads(item[1].decode('utf-8'))
            output[deviceId] = history
            counter += 1
            sys.stdout.write('\r' + 'Transforming user history: %s%%  ' % round((counter/scale) * 100, 1))
            sys.stdout.flush()  # important
        print('Transform user history successfully')
        return output

class ComputeFunction():

    def computeSimilarity4SparseVector(self):
        return

    def buildHistoryMatrixFromHistory(self, userHistory):
        matrix = np.zeros((len(userHistory.keys()),50000))
        deviceIdMap = dict()
        row = 0
        for deviceId in userHistory.keys():
            historyList = userHistory[deviceId]
            deviceIdMap[row] = deviceId
            for record in historyList:
                col = record[0]
                matrix[row][col] += 1
            row += 1
        print('Build sparse vector successfully')
        return matrix, deviceIdMap

    def buildSimilarityMatrix(self, historyMatrix, sampleSize):
        sparseMatrix = sparse.csr_matrix(historyMatrix[:sampleSize])
        similarities = metrics.pairwise.cosine_similarity(sparseMatrix)
        return similarities

def buildSimFromNewsHistory():
    sqlFunction = SqlFunction()
    computeFunction = ComputeFunction()
    userHistory = sqlFunction.getUserHistory()
    historyMatrix, deviceIdMap = computeFunction.buildHistoryMatrixFromHistory(userHistory)

    similarities = computeFunction.buildSimilarityMatrix(historyMatrix, 5000)
    ##roughly %8 of total have no similarity with others
    rowNum = similarities.shape[0]
    similarUserThreshold = 10
    relationDict = dict()
    for i in range(rowNum):
        if round(similarities[i].sum(), 3) != 1:
            deviceId = deviceIdMap[i]
            similarities[i][i] = 0
            oneSimilarity = similarities[i]
            similarityOrder = oneSimilarity.argsort()[::-1]
            relationDict[deviceId] = list()
            for similarNum in range(similarUserThreshold):
                orderColumn = similarityOrder[similarNum]
                if round(oneSimilarity[orderColumn], 2)!= 0:
                    relationDict[deviceId].append(deviceIdMap[orderColumn])
    print('Build similarity pool successfully')
    with open('sample-relationshipTable.json', 'w', encoding='utf-8') as f:
        json.dump(relationDict, f)
    print('Build output successfully')

if __name__ == '__main__':
    buildSimFromNewsHistory()