from mysql import connector
from scipy import sparse, spatial
from sklearn.metrics.pairwise import cosine_similarity
import json
import sys

class SqlFunction():

    def getUserProfile(self):
        conn = connector.connect(host='hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='HSDBADMIN', password='NestiaHSPWD', database='recommend_system')
        cursor = conn.cursor()
        cursor.execute('select * from user_news_profile')
        queryResult = cursor.fetchall()
        cursor.close()
        conn.close()
        print('Get user profile successfully')

        output = {}
        scale = len(queryResult)
        counter = 0
        for item in queryResult:
            deviceId = item[0].decode('utf-8')
            history = json.loads(item[1].decode('utf-8'))
            TypeVec = json.loads(item[2].decode('utf-8'))
            SourceVec = json.loads(item[3].decode('utf-8'))
            output[deviceId] = {'history': history, "TypeVec": TypeVec, "SourceVec": SourceVec}
            counter += 1
            sys.stdout.write('\r' + 'Transforming user profile: %s%%  ' % round((counter/scale) * 100, 1))
            sys.stdout.flush()  # important
        print('Transform user profile successfully')
        return  output

class ComputeSim():

    def cosSim(self, vec1, vec2):
        similarity = 1 - spatial.distance.cosine(vec1, vec2)
        return similarity

    def buildSimilarityDict(self, matrix, deviceIdList):
        similarityDict = dict()
        # similarities = cosine_similarity(matrix)
        # print('Compute similarity successfully')
        scale = len(deviceIdList)
        counter1 = 0
        for m in range(len(deviceIdList)):
            mainId = deviceIdList[m]
            mainVec = matrix[m]
            similarityDict[mainId] = dict()
            counter2 = 0
            for n in range(len(deviceIdList)):
                subId = deviceIdList[n]
                subVec = matrix[n]
                similarityDict[mainId][subId] = self.cosSim(mainVec, subVec)
                counter2 += 1
                sys.stdout.write('\r' + 'Computing similarity: %s%%  ' % round((counter2/ scale) * 100, 1))
                sys.stdout.flush()  # important
            counter1 += 1
            print('Building similarity dict: %s%%  ' % round((counter1/scale) * 100, 1))
        print('Build similarity dict successfully')
        return similarityDict


def buildSimIndex():
    sqlFunction = SqlFunction()
    userProfile = sqlFunction.getUserProfile()
    computeSim = ComputeSim()

    vecMatrix = list()
    deviceList = list()
    for deviceId in userProfile.keys():
        ##currently, no further transformation for these two vectors
        tempVec = userProfile[deviceId]["TypeVec"] + userProfile[deviceId]["SourceVec"]
        vecMatrix.append(tempVec)
        deviceList.append(deviceId)
        ##here only take 500 samples
    similarityDict = computeSim.buildSimilarityDict(vecMatrix[:500], deviceList[:500])
    with open('sampleSimilarityDict.json', 'w', encoding='utf-8') as f:
        json.dump(similarityDict, f)
    f.close()
    print('Save output successfully')

if __name__ == '__main__':
    buildSimIndex()