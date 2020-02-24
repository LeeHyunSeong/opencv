from flask import Flask, make_response	#설치 필요 (API 라이브러리 - https://rekt77.tistory.com/103 참고)
from student import Student				#학생증 이용 .py파일
import requests                                         #HTTP 요청 라이브러

APP = Flask(__name__)                                   #플라스크 객체 생성

@APP.route('/stu')					#학생 객체를 만들고 정보 업로드 및 json으로 업로드 함수
def stu():
        #URL = ''
        RESPONSE = requests.post(URL, data = {'key':'value'}) #이미지 post방식으로  text 받기
        ST = Student(RESPONSE.text)                     #학생 객체 생성(인자는 Base64 이미지 데이터)
        ST.LOADSTU()                                    #학생 정보 로드 함수
        ST.LOADQR()                                     #QR코드 로드 함수
        STATUS = ST.GETSTATUS()                         #http 통신상태 값 받는 함수 
        STJN = ST.GETJSON()                             #서버 통신을 위한 데이터를 json으로 받는 함수
        if STATUS == 401:                               #QR코드 로드 값이 fail일때
                return make_response(STJN, 401)         
        elif STATUS == 400:                             #학생증 로드를 실패했을 때
        	return make_response(STJN, 400)
        elif STATUS == 200:                             #정상 작동
                return STJN

APP.run()						#실행
