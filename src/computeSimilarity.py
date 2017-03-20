from mysql import connector

class SqlFunction():

    def getUserProfile(self):
        conn = connector.connect(host='hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='HSDBADMIN', password='NestiaHSPWD', database='recommend_system')
        cursor = conn.cursor()
        cursor.execute('select * from user_news_profile')
        queryResult = cursor.fetchall()

        output = {}
        for item in queryResult:
            output[item[0]] = {'history': item[1], "TypeVec": item[2], "SourceVec": item[3]}
        return  output

class ComputeSim():



def computeSim():
    sqlFunction = SqlFunction()
    userProfile = sqlFunction.getUserProfile()