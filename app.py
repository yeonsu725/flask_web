from flask import Flask , render_template, redirect, request, session, url_for  # flask 가져오기 session : 로그인유지기능 만들기 
# from data import Articles # data파일에서 함수이름 가져온거임 db가 mysql로 바뀌면서 이제 필요없어짐 
import pymysql
from passlib.hash import pbkdf2_sha256
from functools import wraps 
from pymongo import MongoClient


app = Flask(__name__)
# 서버 띄우기 
# __name__:자체내장변수 

client = MongoClient("mongodb+srv://root:1234@cluster0.g4bac.mongodb.net/test?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
db = client.gangnam
db_user = client.users

list = db.list 
users = db_user.users


app.config['SECRET_KEY'] = 'gangnam' 

db_connection = pymysql.connect(
	    user    = 'root',
        passwd  = '1234',
    	host    = '127.0.0.1',
    	db      = 'gangnam',
    	charset = 'utf8'
)

# 권한을 부여해서 로그인 상태에서만 편집, 삭제, 글쓰기가 가능하게 하는 기능을 구현한다.
# 로그인 , 관리자 체크하는 함수를 만들어서 데코레이트를 만들어준다. 
def is_logged_in(f): # f: 함수, 인자값으로 함수를 받는구나 하고 알면됨 
    @wraps(f)
    def wrap(*args, **kwargs): # 얼마만큼의 정보를 받을지 모르기에 가변인자와 키가변인자를 받는다고 써놓는다.
        if 'is_logged' in session:
            return f(*args, **kwargs) # pass와 같은 의미 
        else:
            return redirect(url_for('login')) # /login = url_for('login') 같은 의미 
    return wrap 

# 삭제는 admin(관리자)만 할수있도록 만들어보기
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['email'] == '2@naver.com':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('articles'))
    return wrap 


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
    print(len(session))
    return render_template('index.html', data=name, user=session) # render_template 플라스크안에있는 라이브러리이기 때문에 위에서 import 해줘야함 
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
    return render_template('articles.html', data=topics, user=session)




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
    #         article = data  # 이제 가라데이터가 사라지고 sql문으로 database(= schema)를 불러오기때문에 for문을 사용하여 실행할 필요가 없음 
    return render_template('article.html', article=topic, user=session) 
    # Articles 가 article = data 이며 article=article의 오른쪽 article 
    # 가라데이터 data.py는 딕셔너리 형태의 데이터였음 하지만 sql문으로 만든 database는 튜플형태로 반환을 함
    # 그래서 article , articles.html 의 데이터를 딕셔너리 형태에서 튜플문으로 바꿔줘야지 표기가 된다. 




@app.route('/delete/<ids>', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def delete(ids):
    cursor = db_connection.cursor()
    sql = f'DELETE FROM list WHERE (id = {ids});' # 삭제하는 거니까 선택select가 아닌 delete 
    cursor.execute(sql)
    db_connection.commit() # 수정하거나 추가하거나 삭제하면 commit을 사용하는거임 fetch는 조회할때 쓰는거임 
    
    return redirect('/articles') # 이렇게 하면 @app.route('/articles' 여기로 가서 다시 실행하는거임 
    # render_template 을 사용하면 데이터를 또 줘야하자나 우린 삭제한건데 데이터를 넣을 필요는 없지??? 



# 웹상에서 데이터 저장기능 만들기 
@app.route('/add_article', methods = ['GET', 'POST'])
@is_logged_in
def add_article():
    # get 이냐 post에 따라 다르게
    if request.method == 'GET':
        return render_template('add_article.html', user=session)
   
    else:
        title = request.form["title"]
        desc = request.form["desc"]
        author = request.form["author"]
        # 위에서 form으로 잘 받아왔기 때문에 db에 저장하는게 이제 필요함!!

        list.insert_one({"title":title, "description":desc, "author":author})

        # db에 저장하려면 cursor = db_connection.cursor()이거 필요함!
        cursor = db_connection.cursor()
        sql = f"INSERT INTO list (title, description, author) VALUES ('{title}', '{desc}', '{author}');"
        # description 은 sql문의 컬럼이고 request.form[desc]는 add_article.html의 name과 같아야함
        # 그리고 desc와 '{desc}' 가 같은 거임 
        cursor.execute(sql)
        db_connection.commit()
        return redirect('/articles')

# 편집버튼 활성화 시키기 
@app.route('/edit_article/<ids>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(ids):
    if request.method == 'GET':
        cursor = db_connection.cursor()
        sql = f'SELECT * FROM list WHERE id={int(ids)};'
        cursor.execute(sql)
        topic = cursor.fetchone()


        return render_template('edit_article.html', article=topic) 
    else: 
        title = request.form["title"]
        desc = request.form["desc"]
        author = request.form["author"]
        # request 클라이언트가 요청하는 걸 request라고 함 
        # 요청을 날릴때 get, post던지 엄청 많은 양을 날림, 그 많은 정보중에서 필요한 것만 날려주는게 request 다.
        # 그 중 request의 메서드중 form 이라는 걸 이용하면 클라이언트가 요청(request)한 것중에 form형식을 받아볼수 있는 거임 

        cursor = db_connection.cursor()
        sql = f"UPDATE list SET title = '{title}', description = '{desc}', author = '{author}' WHERE (id = {int(ids)});"
        cursor.execute(sql)
        db_connection.commit()
        return redirect('/articles')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', user=session)
    else:
        username = request.form['username']
        email = request.form['email']
        password = pbkdf2_sha256.hash(request.form['password']) # 비밀번호 암호화 
        users.insert_one({"username":username, "email":email, "password":password})
        cursor = db_connection.cursor()

        #중복체크 만들기
        sql_1 = f"SELECT * FROM users WHERE email='{email}'" # 세미콜론 없어도 됨 
        cursor.execute(sql_1)
        user = cursor.fetchone() 
        print(user)

        if user == None:
            sql = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}');"
            cursor.execute(sql)
            db_connection.commit()
            return redirect('/') # 이메일을 입력했을 시 같은 이메일이 없다면 즉, 중복이 아니라면 홈화면으로 돌아가고 
        else:
            return redirect('/register') # none이 아니고 중복된 이메일을 입력했을 시 다시 회원가입 화면으로 ㄱㄱ!
            
# 로그인 만들기
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', user=session)
    else:
        email = request.form['email']
        password = request.form['password']
        sql_1 = f"SELECT * FROM users WHERE email='{email}'"
        cursor = db_connection.cursor()
        cursor.execute(sql_1)
        user = cursor.fetchone()
        print(user)

        if user == None:
            # user가 none이면 아이디 틀리게 친거니까 로그인화면으로 보내버리자 
            return redirect('/login')
        
        else:
            #비번 맞는지 비교해야지  
            result = pbkdf2_sha256.verify(password, user[3])   
            if result == True:
                # 로그인 유지기능 만들기 , secret 키가 필요함 
                session['id'] = user[0] # index 번호 
                session['username'] = user[1] # username
                session['email'] = user[2] # email
                session['date'] = user[4] # create_at
                session['is_logged'] = True
                
                print(session)
                return redirect('/')
            else:
                return redirect('/login')


# 로그아웃 만들기
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear() # session 지워주는 역할을 함 
    return redirect('/')

# 권한을 부여해서 로그인 상태에서만 편집, 삭제, 글쓰기가 가능하게 하는 기능을 구현한다.
# 로그인, 로그아웃, 관리자 체크하는 함수를 만들어서 데코레이트를 만들어준다. 




if __name__ == '__main__':
    app.run(debug=True)

