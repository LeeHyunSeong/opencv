import base64  # 이미지 불러올 때를 위한 라이브러리 https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image/16214280 참고
import requests  # (Qr코드 처리 값 해석) https://bcho.tistory.com/822 참고
# (Qr코드 처리) https://www.opentutorials.org/module/3811/25284 참고
import matplotlib.pyplot as plt
# 설치 필요 (Qr코드 처리) https://www.opentutorials.org/module/3811/25284 참고
import pyzbar.pyzbar as pyzbar
# 설치 필요 (영상처리)https://076923.github.io/posts/Python-opencv-1/ 참고
import cv2  # 설치 필요 (영상처리)https://076923.github.io/posts/Python-opencv-1/ 참고
from pytesseract import *  # 설치 필요 (영상처리)https://shinminyong.tistory.com/5 참고
from ApiError import *  # 사용자 정의 에러 클래스 포함
import re
import random
import os

class StudentCard:  # 학생증 클래스
    IMG_PATH = 'tmp/studentCard' + str(random.randint(0,100)) + '.png'

    def __init__(self, imgStr):
        self.studentInfo = {}

        metadataLen = imgStr.find(',')
        if not self.__checkImageType(imgStr[:metadataLen]):
            raise ImageTypeUnmatchError
        self.imgData = base64.b64decode(imgStr[metadataLen+1:])
        with open(self.IMG_PATH, 'wb') as f:
            f.write(self.imgData)
        self.img = cv2.imread(self.IMG_PATH)
        self.h, self.w = self.img.shape[:2]

    def loadDataOfImg(self):  # 사진에서 데이터 저장 함수
        infoROI = self.img[int(self.h*0.6):int(self.h*0.85),
                           int(self.w*0.28):int(self.w*0.73)]
        strOfImage = image_to_string(infoROI, lang='kor')
        strOfImg = strOfImage.strip("'")
        datas = strOfImg.split('\n')
        results = list(
            filter(lambda data: True if data != '' else False, datas))
        self.studentInfo['name'] = results[0]
        self.studentInfo['department'] = results[1]
        self.studentInfo['id'] = results[2]
        if not self.__checkStudentInfo():
            raise StudentCardReadError

    def __checkImageType(self, imgType):
        regex =  re.compile(r'^(data:image/\w{3,4};base64)$')
        if regex.search(imgType):
            return True
        else:
            return False

    def __checkStudentInfo(self):
        if self.studentInfo['department'].find(" ") >= 0:
            return False
        if self.studentInfo['department'].find("학과") < 0 and self.studentInfo['department'].find("학부") < 0:
            return False
        if self.studentInfo['name'].find(" ") >= 0:
            return False
        if self.studentInfo['id'].find(" ") >= 0:
            return False
        if not self.studentInfo['id'].isdigit():
            return False
        if int(self.studentInfo['id']) < 50000:
            return False

        return True

    def loadQRcode(self):  # Qr코드 해석 후 role 저장 함수
        grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        QRcode = pyzbar.decode(grayImg)
        values = list(map(lambda value: value.data.decode('utf-8'), QRcode))
        response = requests.get(values[0])
        QRdatas = response.text.split('"')
        results = list(
            filter(lambda data: True if data != '' else False, QRdatas))

        if results[7] == "FAIL":
            raise QRcodeReadError
        elif results[7] == "SUCCES":
            self.studentInfo['role'] = 'student'

    def getStudentInfo(self):
        return self.studentInfo

    def removeFile(self):
        os.remove(IMG_PATH)
