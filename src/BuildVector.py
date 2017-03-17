from mysql import connector
from src import getNewsRecord

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
            newsInformation[item] = {'type': item[1], 'source': item[2]}
        print('Get news information successfully')
        return newsInformation

    def sendVector(self, userNewsProfile):
        conn = connector.connect(host='prod-mysql-nestia-food.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='readonly', password='nestiareadonly', database='news')
        cursor = conn.cursor()
        cursor.close()
        conn.close()
        print('Send user vector successfully')
        return

class VecFunction():

    def buildTypeVec(self):
        return

    def BuildSourceVec(self):
        return

def main():
    sqlFunction = SqlFunction()
    vecFunction = VecFunction()
    userNewsProfile = dict()

    userNewsCollection = getNewsRecord.minLog('2017-01-01', '2017-03-17')
    newsInformation = sqlFunction.getNewsInformation()

    for deviceId in userNewsCollection.keys():
        userNewsProfile[deviceId] = {'history': userNewsCollection[deviceId]
                                    , 'TypeVec': []
                                    , 'SourceVec': []}

