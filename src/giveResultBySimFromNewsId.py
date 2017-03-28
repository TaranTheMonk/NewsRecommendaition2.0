import json
from mysql import connector
from src import buildSimByNewsId
import sys

class RecommendationFunction():
    def getSimilarPeoplePool(self):
        with open('sample-relationshipTable.json', 'r', encoding='utf-8') as f:
            similarPeoplePool = json.load(f)
        f.close()
        return  similarPeoplePool

    def buildNewsPool(self, userHistory, relationshipTable, numFromOne, numSimilarUser):
        newsPoolDict = dict()
        processCounter = 0
        scale = len(relationshipTable.keys())
        for deviceId in relationshipTable.keys():
            ##newsRecordPair = [news id, record time]
            banList = {newsRecordPair[0] for newsRecordPair in userHistory[deviceId]}
            ##deviceIdPair = [deviceId, similarity score]
            relationship = [deviceIdPair[0] for deviceIdPair in relationshipTable[deviceId][:numSimilarUser] if deviceIdPair[1] != 1]
            newsPoolDict[deviceId] = list()
            for similarDeviceId in relationship:
                for i in range(numFromOne):
                    try:
                        newsId = userHistory[similarDeviceId][i][0]
                        if not newsId in banList:
                            banList.add(newsId)
                            newsPoolDict[deviceId].append(newsId)
                    except:
                        break
            processCounter += 1
            sys.stdout.write('\r' + 'Building news pool: %s%%  ' % round((processCounter/scale) * 100, 1))
            sys.stdout.flush()  # important
        return newsPoolDict

    def selectNewsFromPool(self):
        return

def giveRecommendation():
    recommendationFunction = RecommendationFunction()
    sqlFunction = buildSimByNewsId.SqlFunction()
    userHistory = sqlFunction.getUserHistory()
    with open('sample-relationshipTable.json', 'r', encoding='utf-8') as f:
        relationshipTable = json.load(f)
    f.close()
    print('Building news pool from similar user...')
    newsPoolDict = recommendationFunction.buildNewsPool(userHistory, relationshipTable, 10, 10)
    print('Build news pool from similar user successfully!')
    with open('newsPoolDict.json', 'w', encoding='utf-8') as f:
        json.dump(newsPoolDict, f)
    f.close()
    print('Save output successfully')

if __name__ == '__main__':
    giveRecommendation()