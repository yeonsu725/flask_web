from flask import Flask 
# flask 가져오기 

app = Flask(__name__)
# 서버 띄우기 
# __name__:자체내장변수 

@app.route('/')
def hello_world():
    return 'Hello World!'
# 반응하는 코드를 만드는 애 
# / : 경로 /뒤에 hello를 쓰면 접속주소가 http://localhost:5000/ 에서 -->http://localhost:5000/hello 이걸로 바뀜 

if __name__ == '__main__':
    app.run()
# 서버 띄우기 
# 왜 굳이 이걸 쓰냐?  플라스크를 실행시켰을 때 자체내장변수를 사용하여 if문을 만들고 main일 때만 앱을 실행시켜라 하는거고 python이 아닌걸로
# 실행시엔 실행을 못하게 하려고 이렇게 만든거다 
