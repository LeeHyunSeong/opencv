from flask import Flask, make_response	#설치 필요 (API 라이브러리 - https://rekt77.tistory.com/103 참고)
from main import Student				#학생증 이용 .py파일

app = Flask(__name__) 

@app.route('/stu')					#학생 객체를 만들고 정보 업로드 및 json으로 업로드 함수
def stu():
        f = open("C:/Users/Samsung/Desktop/data.txt", 'r')
        data = f.read()
        f.close()
        st = Student(data)
        st.load_stu()
        st.load_Qr()
        status = st.get_Status()
        stjn = st.getJson()
        if status == 401:
                return make_response(stjn, 401)
        elif status == 400:
        	return make_response(stjn, 400)
        elif status == 200:
                return stjn

app.run()						#실행
