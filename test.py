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

hash = pbkdf2_sha256.hash("1234") # 가상환경 밖으로 나가서 실행해야지 실행가능 --> 버전 1.7.2로 업글하여 이제 실행가능해짐!! 
# 지금 hash코드를 사용하여 1234 를 -->$29000$6N17jzEGwPh/j1HqHSMEoA$T4ResHFz2h8hgahD9aARWTKSWLTugduzqG4ChThvugo 이렇게 바꾼거임 
# 이게 비번 암호화 
print(hash)


result = pbkdf2_sha256.verify("1234", hash) 
print(result) # true, false로 표기됨
# hash로 바꾼 비밀번호를 원 형태로 확인하는 것은 불가능하지만 (해커는 가능) verify라는 메서드를 사용하여 비밀번호가 같은지의 여부를 알 수 있음 
# true & false로 반환함 
