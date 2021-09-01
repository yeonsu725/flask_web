# import pymysql


# db_connection = pymysql.connect(
# 	    user    = 'root',
#         passwd  = '1234',
#     	host    = '127.0.0.1',
#     	db      = 'gangnam',
#     	charset = 'utf8'
# )

# cursor = db_connection.cursor()

# sql = 'SELECT * FROM list;' 

# # cursor가 명령어를 날림, mysql하고 연결시켜서(import pymysql) 새로운 인스턴스(db_connection)와 연결하고 커서로 명령어 날림 
# cursor.execute(sql)

# topics = cursor.fetchall()

# print(topics)
# ---------------------------------------------------------------------------------------------------------------
# mysql 비밀번호 암호화 하기 

from passlib.hash import pbkdf2_sha256

hash = pbkdf2_sha256.hash("1234") # 가상환경 밖으로 나가서 실행해야지 실행가능 
# 지금 hash코드를 사용하여 1234 를 -->$pbkdf2-sha256$29000$6N17jzEGwPh/j1HqHSMEoA$T4ResHFz2h8hgahD9aARWTKSWLTugduzqG4ChThvugo 이렇게 바꾼거임 
# 이게 비번 암호화 
print(hash)


result = pbkdf2_sha256.verify("1234", hash) 
# 이 함수를 사용하여 비밀번호가 같은지를 알 수는 있음 !! 
print(result) # true, false로 표기됨


