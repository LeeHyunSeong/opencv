# 설치 필요 (API 라이브러리 - https://rekt77.tistory.com/103 참고)
from flask import Flask, make_response, request
import json
from StudentCard import *  # 학생증 이용 .py파일
import requests  # HTTP 요청 라이브러

App = Flask(__name__)  # 플라스크 객체 생성


@App.route('/studentcard', methods=['POST'])  # 학생 객체를 만들고 정보 업로드 및 json으로 업로드 함수
def studentcard():
    response = {'message': '', 'data': {}}
    status = 200

    try:
        print("Process student card routine")
        print("request img data: ")
        
        imgData = request.form['imgData']
        studentCard = StudentCard(imgData)
        studentCard.loadDataOfImg()
        studentCard.loadQRcode()

        response['message'] = 'Success'
        response['data'] = studentCard.getStudentInfo()
    except ApiError as e:
        status = e.status
        response['message'] = e.error
    finally:
        responseJSON = json.dumps(response)
        return make_response(responseJSON, status)


App.run(host='0.0.0.0', port='8091')  # 실행
