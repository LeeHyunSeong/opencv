from PIL import Image                                    #(영상 처리)
from pytesseract import *                                #설치 필요 (영상처리)https://shinminyong.tistory.com/5 참고
import re                                                #(영상처리)
import cv2                                               #설치 필요 (영상처리)https://076923.github.io/posts/Python-opencv-1/ 참고
import numpy as np                                       #설치 필요 (영상처리)https://076923.github.io/posts/Python-opencv-1/ 참고
import json                                              #(json 변환)
import pyzbar.pyzbar as pyzbar                           #설치 필요 (Qr코드 처리) https://www.opentutorials.org/module/3811/25284 참고
import matplotlib.pyplot as plt                          #(Qr코드 처리) https://www.opentutorials.org/module/3811/25284 참고
import requests                                          #(Qr코드 처리 값 해석) https://bcho.tistory.com/822 참고
import base64                                            #이미지 불러올 때를 위한 라이브러리 https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image/16214280 참고

class Student: #학생 클래스
    def __init__(self, DATA):                                        #사진과 최종 데이터 딕션너리 생성하는 생성자
        self.STUDIC = {}                                             #스캔 성공 시 json을 위한 딕션너리 생성                                          #로드 실패 시 데이터 딕션너리 생성
        self.HTTPDIC = {"message":"", "data":{}}                     #http 응답신호와 데이터를 합쳐서 보낼 딕션너리
        self.WORD = DATA.find(',')                                   #,의 위치 찾기
        self.DATA64 = DATA[WORD+1:]                                  #이미지 Base64 데이터에서 앞의 형식 문자열 삭제한 문자열
        self.IMGDATA = base64.b64decode(self.DATA64)                 #이미지 변환
        self.FILENAME = 'tmp/some_image.jpg'                         #이미지 저장
        with open(self.FILENAME, 'wb') as f:
            f.write(self.IMGDATA)
        self.IMG = cv2.imread("tmp/some_image.jpg")                  #이미지 불러오기
        self.H, self.W = self.IMG.shape[:2]                          #이미지 높이와 너비 구하기
        self.STATUS = 200                                            #http 응답 신호
        self.INFO = 'ok'                                             #http 응답 메시지
    
    def LOADSTU(self): #사진에서 데이터 저장 함수
        IMGINFO = self.IMG[int(self.H*0.6):int(self.H*0.85), int(self.W*0.28):int(self.W*0.73)]     #이미지 정보부분 짜르기
        TEXT = pytesseract.image_to_string(IMGINFO, lang='kor')      #이미지 속 텍스트 저장
        INFOLIST = re.split('\n', TEXT)                              #텍스트 리스트로 저장
        LIST = []                                                    #최종 정보 저장 리스트
        for i in INFOLIST:                                           #정보만 따로 분별해서 저장하는 작업
            if i != '' :
                LIST.append(i)
                
        self.STUDIC['name'] = LIST[0]                                #이름 추가
        self.STUDIC['depart'] = LIST[1]                              #학과 추가
        self.STUDIC['id'] = LIST[2]                                  #학번 추가
    
    def GETJSON(self): #json으로 변환하는 함수
        return json.dumps(self.HTTPDIC)                              #json 파일 생성
                           
    def LOADQR(self): #Qr코드 해석 후 role 저장 함수
        GRAY = cv2.cvtColor(self.IMG, cv2.COLOR_BGR2GRAY)            #이미지 보정
        plt.imshow(GRAY, cmap='gray')                                #이미지 보정
        DECODED = pyzbar.decode(GRAY)                                #QR코드 정보 = URL+위치 등
        QRDATA = []
        for d in decoded:                                                                       
            QRDATA.append(d.data.decode('utf-8'))                    #QR코드 값 = URL

        REQUEST = requests.get(QRDATA[0])                            #QR코드 값 해석
        QRINFO = REQUEST.text                                        #QR코드 값 저장
        QRLIST = re.split('"', QRINFO)                               #QR코드 값 분해
        LIST = []                                                    #QR코드 값 분해한 것을 저장하는 리스트
        for i in QRLIST:                                             #QR코드에 저장
            if i != '':
                list.append(i)
                
        if LIST[7] == "FAIL":                                        #읽은 값이 FAIL일때
            self.STUDIC['role'] = 'unknown'                          #학생 신분 파악 실패
            self.STATUS = 401                                        #QR코드 읽기 실패 >> 401
            self.INFO = 'Failed to recognize QR code'                #http 응답 메시지
            self.HTTPDIC['message'] = self.INFO                      #빈 데이터

        elif LIST[7] == "SUCCES":                                    #읽은 값이 SUCCES일 때
            self.STUDIC['role'] = 'student'                          #학생 신분 파악 성공
            self.STATUS = 200                                        #성공 >> 200
            self.INFO = 'Success'                                    #http 응답 메시지
            if (self.STUDIC['depart'].find(" ") >= 0) or (self.STUDIC['depart'].find("학과") < 0 and self.stu_dic['depart'].find("학부") < 0) or (self.STUDIC['name'].find(" ") >= 0) or (self.stu_dic['id'].find(" ") >= 0) or (not self.STUDIC['id'].isdigit()) or (not int(self.STUDIC['id']) < 50000):   #학생증 읽기 실패
                self.STATUS = 400                                    #학생증 읽기 실패 >> 400
                self.INFO = 'Failed to recognize ID card'            #http 응답 메시지

            self.HTTPDIC['message'] = self.INFO                      #http 응답 메시지

            if self.STATUS == 200:                                   #학생증 읽기 성공 >> 200
                self.HTTPDIC['data'] = self.STUDIC                   #학생증 데이터 저장

    def GETSTATUS(self): #http 응답 신호 얻는 함수
        return self.STATUS                                           #응답 신호 리턴
