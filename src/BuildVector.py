from mysql import connector
from src import getNewsRecord
import json
import re

# {"history": [(id, time)],
#  "TypeVec": [],
#  "SourceVec": []}

class SqlFunction():

    def getNewsInformation(self):
        newsInformation = dict()
        conn = connector.connect(host='prod-mysql-nestia-food.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='readonly', password='nestiareadonly', database='news')
        cursor = conn.cursor()
        cursor.execute('select id, type, source_site from news')
        queryResult = cursor.fetchall()
        cursor.close()
        conn.close()
        for item in queryResult:
            newsInformation[item[0]] = {'type': item[1], 'source': item[2]}
        print('Get news information successfully')
        return newsInformation

    ## send queries batch by batch
    def sendVector(self, userNewsProfile):
        validIdPattern = re.compile('[0-9A-Za-z/-]{36,36}|[0-9a-z]{12,16}')
        values_to_insert = list()
        for item in userNewsProfile.keys():
            if validIdPattern.match(item):
                tempTarget = userNewsProfile[item]
                values_to_insert.append((item, str(tempTarget['history']),
                                         str(tempTarget['TypeVec']), str(tempTarget['SourceVec'])))
        query = "insert into user_news_profile (device_id, history, TypeVec, SourceVec) values (%s, %s, %s, %s)"

        conn = connector.connect(host='hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='HSDBADMIN', password='NestiaHSPWD', database='recommend_system')
        cursor = conn.cursor()

        position = 0
        batchNum = 1
        while True:
            tempValue = values_to_insert[position : position + 5000]
            position = position + 5000
            if tempValue == []:
                break
            cursor.executemany(query, tempValue)
            conn.commit()
            print('Finished insert for #%s batch, batch size: 5000' % batchNum)
            batchNum += 1

        cursor.close()
        conn.close()
        print('Send user vector successfully')

class VecFunction():

    def buildVec(self, newsHistory, newsInformation):
        typeVec = [0] * 28
        ## for source, 0 is original written by Nestia
        sourceVec = [0] * 52
        for pair in newsHistory:
            try:
                newsId = pair[0]
                newsType = newsInformation[newsId]['type']
                newsSource = newsInformation[newsId]['source']
                typeVec[newsType-1] += 1
                sourceVec[newsSource] += 1
            except:
                pass
        return typeVec, sourceVec

def buildVecFromLog():
    sqlFunction = SqlFunction()
    vecFunction = VecFunction()
    userNewsProfile = dict()

    userNewsCollection = getNewsRecord.minLog('2017-01-01', '2017-03-01')
    newsInformation = sqlFunction.getNewsInformation()


    for deviceId in userNewsCollection.keys():
        oneHistory = userNewsCollection[deviceId]
        userNewsProfile[deviceId] = {'history': oneHistory
                                    , 'TypeVec': []
                                    , 'SourceVec': []}
        userNewsProfile[deviceId]['TypeVec'], userNewsProfile[deviceId]['SourceVec']\
            = vecFunction.buildVec(oneHistory ,newsInformation)
    del userNewsProfile['']
    sqlFunction.sendVector(userNewsProfile)

    with open('userNewsProfile.json','w' ,encoding='utf-8') as f:
        json.dump(userNewsProfile, f)
    f.close()

if __name__ == '__main__':
    buildVecFromLog()
