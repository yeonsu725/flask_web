import pymysql


db_connection = pymysql.connect(
	    user    = 'root',
        passwd  = '1234',
    	host    = '127.0.0.1',
    	db      = 'gangnam',
    	charset = 'utf8'
)

cursor = db_connection.cursor()

sql = 'SELECT * FROM list;' 

# cursor가 명령어를 날림, mysql하고 연결시켜서(import pymysql) 새로운 인스턴스(db_connection)와 연결하고 커서로 명령어 날림 
cursor.execute(sql)

topics = cursor.fetchall()

print(topics)