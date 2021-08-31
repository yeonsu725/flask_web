from flask import Flask , render_template # flask 가져오기 
from data import Articles # data파일에서 함수이름 가져온거임 
import pymysql

db_connection = pymysql.connect(
	    user    = 'root',
        passwd  = '1234',
    	host    = '127.0.0.1',
    	db      = 'gangnam',
    	charset = 'utf8'
)

app = Flask(__name__)
# 서버 띄우기 
# __name__:자체내장변수 

@app.route('/hello')
def hello_world():
    return 'Hello World!'
# 반응하는 코드를 만드는 애 
# / : 경로 /뒤에 hello를 쓰면 접속주소가 http://localhost:5000/ 에서 -->http://localhost:5000/hello 이걸로 바뀜 

# if __name__ == '__main__':
#     app.run()
# 서버 띄우기 
# 왜 굳이 이걸 쓰냐?  플라스크를 실행시켰을 때 자체내장변수를 사용하여 if문을 만들고 main일 때만 앱을 실행시켜라 하는거고 python이 아닌걸로
# 실행시엔 실행을 못하게 하려고 이렇게 만든거다 

# 게시판 만들기 // flask 라이브러리를 이용한 웹 구현 
# front end - 보여지는 부분 
# back end - 기능을 하는 부분 (서버) -> back end 안에 database가 있음 // back end 안에 front end가 있는 것도 있고 외부에 있는 것도 있음 
# front end가 back end에 requst를 날리면 response를 해주는 방식 
# 우리가 하는 방식은 back end안에 database 와 front end가 같이 있는 방식으로 만들 것 
# flask 파이썬 라이브러리 및 프레임워크 를 사용하여 만들거야
# flask_web 안에 templates, static, app.py 의 폴더2개와 파일1개를 만들고 시작할 거임
# templates --> front end가 들어갈 거임 
# static 
# app.py -> 서버 즉 back end가 들어갈 거임 

# http://localhost:5000 경로로 get 방식으로 request 할때 index.html 파일을 랜더링 해주는 기능을 구현하기위하여 
# app.py에 다음과 같은 코드를 추가한다. 
# @ : 데코레이터, 처음꺼(함수나 메서드) 처리해주고나서 @에 붙어있는 애를 처리해줌

@app.route('/', methods=['GET', 'POST'])
def index():
    name = 'KIM'
    return render_template('index.html', data=name) # render_template 플라스크안에있는 라이브러리이기 때문에 위에서 import 해줘야함 
    # render_template 를 실행시키면 templates 라는 폴더를 찾게됨. 그안에있는 index.html파일의 내용이 localhost:5000에 표기됨
    # render_template는 index.html를 랜더링 해주면서 data를 실어보낼수 있음 

@app.route('/articles', methods=['GET','POST'])
def articles():
    # list_data = Articles() 가라 데이터 이제 지울거임 sql만들었으니까 
    cursor = db_connection.cursor()
    sql = 'SELECT * FROM list;' 
    cursor.execute(sql)
    topics = cursor.fetchall() # db에서 조회한 결과를 fetchall이라는 걸로 모든결과물을 불러와서 보여준다~ 
    print(topics)
    return render_template('articles.html', data=topics)

@app.route('/detail/<ids>')
# params 처리한다(=parameter(매개변수,인자) 처리한다) --> 현재 detail뒤에 1,2,3 id값이 변형되면서 오는데 여기다가 그걸 어떻게 표현하냐?? params 처리하면된다.
# 그때그때마다 변하는 값을 어떻게 받아오냐 parameter처리를 하여 받아온다 
# params 처리를 할때는 꺽쇄표시 <> 를 해야함 !! 
def detail(ids):
    # list_data = Articles() # 클릭시 상세페이지로 이동 
    cursor = db_connection.cursor()

    # 퀴리 조건문 
    sql = f'SELECT * FROM list WHERE id={int(ids)};' # https://bluese05.tistory.com/70
    cursor.execute(sql)
    topic = cursor.fetchone() # 여기선 한개만 받아옴 // 하나만 조회를 할때는 fetchone을 사용하면됨 
    print(topic)

    # for data in list_data:
    #     if data['id']==int(ids):
    #         article = data  # 이제 가라데이터가 사라지고 sql문으로 database를 불러오기때문에 for문을 사용하여 실행할 필요가 없음 
    return render_template('article.html', article=topic) 
    # Articles 가 article = data 이며 article=article의 오른쪽 article 


if __name__ == '__main__':
    app.run(debug=True)
