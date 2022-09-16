from tkinter import N
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import datetime
import imp
import pandas as pd
from bs4 import BeautifulSoup as bs
from flask import Flask, redirect, render_template, request
import random
import numpy as np
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask_socketio import SocketIO, send
import pyautogui

app = Flask(__name__)

@app.route('/')
def MainMain():
    # ROOT URL로 접근 했을때 8SENDING 렌더링
    return render_template("MainMain.html")

@app.route('/Mainpage')
def Main():
    # ROOT URL로 접근 했을때 8SENDING 렌더링
    return render_template("Mainpage.html")

# @app.route('/Subpage')
# def sub():
#     return render_template("Subpage.html")

@app.route('/Subpage',methods = ['POST' ,'GET'])
def Subpage():
    if request.method == 'POST':
        result = request.form
        return render_template("/Subpage.html",result=result)

# @app.route('/SearchPOP',methods = ['POST' ,'GET'])
# def SearchPOP():
#     if request.method == 'POST':
#         result = request.form
#         return render_template("/SearchPOP.html",result=result)

@app.route('/SearchPOP_PD',methods = ['POST' ,'GET'])
def SearchPOP_PD():
    if request.method == 'POST':
        #p_env/chromedriver.exe
        chrome_option = Options()
        chrome_option.headless = True
        capability = DesiredCapabilities.CHROME
        capability["pageLoadStrategy"] = "none"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_option)
        driver.get("https://flight.naver.com/")
        time.sleep(2)

        #네이버항공권 홈페이지 접속후 편도 버튼 클릭

        do_query = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[1]/button[2]'
        driver.find_element(By.XPATH, do_query).click()
        time.sleep(0.7)

        #직항여부 

        do_query_direct = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[3]/button[2]'

        # # how = input("[1]직항 [2]경유 ( 번호를 입력해주세요. ex) 1 or 2 ")
        # how = 1
        driver.find_element(By.XPATH, do_query_direct).click()
        time.sleep(0.8)
        # #네이버항공권홈페이지에서 [직항만] 버튼 Html 태그를 xpath 형식으로 따옴
        # if (how == "1"):
        #     driver.find_element(By.XPATH, do_query_direct).click()
        #     time.sleep(1)

        #     # elif (how == "2"):
        #     #     driver.find_element(By.XPATH, do_query_direct).click()
        #     #     time.sleep(1)

        # # 출발지 도착지 



        #start = 출발지 데이터
        start = request.form['from']
        start = str(start)

        #end = 도착지 데이터
        end = request.form['to']
        end = str(end)

        query_start = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[1]/b'
        query_end = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]/b'
        textbox = '//*[@id="__next"]/div/div[1]/div[9]/div[1]/div/input'
        choose = '//*[@id="__next"]/div/div[1]/div[9]/div[2]/section/div/a[1]'

        # 출발지 입력
        driver.find_element(By.XPATH, query_start).click()
        time.sleep(0.5)

        driver.find_element(By.XPATH, textbox).click()
        driver.find_element(By.XPATH, textbox).send_keys(start)
        time.sleep(0.4)

        driver.find_element(By.XPATH, choose).click()
        time.sleep(0.3)

        # 도착지 입력
        driver.find_element(By.XPATH, query_end).click()
        time.sleep(0.8)

        driver.find_element(By.XPATH, textbox).click()
        driver.find_element(By.XPATH, textbox).send_keys(end)
        time.sleep(0.7)

        driver.find_element(By.XPATH, choose).click()
        time.sleep(0.6)

        # 날짜


        #startday = 가는날 데이터
        startday = request.form['deparure']
        startday = str(startday)
        #실제 현재 날짜
        now = datetime.datetime.now()
        #실제 현재 날짜(월)
        month = now.month
        # month = 1

        #웹에서 받아온 가는날 데이터를 월 로만 슬라이싱한 값
        startmonth=startday[1:2]
        #07/02/2022

        # 클릭
        do_query = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]'
        driver.find_element(By.XPATH, do_query).click()
        time.sleep(0.1)
        #웹에서 입력받은 가는날 값(월) - 현재 날짜(월)
        if((int(startmonth)-month)==0):
            driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[0].click()
            time.sleep(0.1)
        elif((int(startmonth)-month)==1):
            driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[1].click()
            time.sleep(0.1)
        elif((int(startmonth)-month)==2):
            driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[2].click()
            time.sleep(0.1)


        # 인원
        old = request.form['old']
        old = int(old)
        young = request.form['young']
        young = int(young)
        baby = request.form['baby']
        baby = int(baby)

        click = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[3]/button[1]'
        old_cnt = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[3]/div/div/div[1]/div[1]/button[2]'
        young_cnt = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[3]/div/div/div[1]/div[2]/button[2]'
        baby_cnt = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[3]/div/div/div[1]/div[3]/button[2]'

        driver.find_element(By.XPATH, click).click()
        time.sleep(0.1)

        if (old > 1):
            for i in range(old-1):
                driver.find_element(By.XPATH, old_cnt).click()
                time.sleep(0.1)

        if (young > 0):
            for i in range(young):
                driver.find_element(By.XPATH, young_cnt).click()
                time.sleep(0.1)

        if (baby > 0):
            for i in range(baby):
                driver.find_element(By.XPATH, baby_cnt).click()
                time.sleep(0.1)

        # 검색 클릭

        do_query = '//*[@id="__next"]/div/div[1]/div[4]/div/div/button'
        try:
            for i in range(10):
                driver.find_element(By.XPATH, do_query).click()
                time.sleep(0.1)
        except:
            print("클릭완료")

        # 정렬

        do_query = '//*[@id="__next"]/div/div[1]/div[6]/div/div[1]/div/div/button'
        cheap = '//*[@id="__next"]/div/div[1]/div[6]/div/div[1]/div/div/div/button[1]'

        try:
            driver.find_element(By.XPATH, do_query).click()
            time.sleep(5)
            driver.find_element(By.XPATH, cheap).click()
            time.sleep(5)

        except:
            print('')
                

            

        #모든정보를 가져오기위한 스크롤
        body=driver.find_element(By.CSS_SELECTOR, 'body')
        for i in range(20):
            body.send_keys(Keys.END)
            time.sleep(0.1)

        #데이터 담아줄 리스트 생성
        air_list =[]
        stime_list =[]
        start_list =[]
        etime_list=[]
        end_list=[]
        loading_list=[]
        price_list=[]

        # 각각 데이터 요소값
        air=driver.find_elements(By.CSS_SELECTOR,'b.name')
        stime=driver.find_elements(By.CSS_SELECTOR,'span.route_airport__3VT7M>b.route_time__-2Z1T')
        loading=driver.find_elements(By.CSS_SELECTOR,'i.route_info__1RhUH')
        start=driver.find_elements(By.CSS_SELECTOR,'i.route_code__3WUFO')
        price=driver.find_elements(By.CSS_SELECTOR,'div.item_price__1TxJh')
            
        # 리스트에 값을 저장
        for i in range(len(loading)):
            loading_list.append(loading[i].text)
        for i in range(len(air)):
            air_list.append(air[i].text)
        for i in range(0,len(stime),2):  
            stime_list.append(stime[i].text)
            start_list.append(start[i].text)
        for i in range(1,len(stime),2):
            etime_list.append(stime[i].text)
            end_list.append(start[i].text)
        for i in range(len(price)):
            price_list.append(price[i].text)

        #가져온 데이터들을 딕셔너리로 생성
        # dic = {'항공사':air_list,'출발시간':stime_list,'도착시간':etime_list,'소요시간':loading_list,'출발지':start_list,'도착지':end_list,'가격':price_list}
            # result=  pd.DataFrame(dic)
            # result.to_csv('제목.csv', encoding='EUC-KR')
            
        total_list = [air_list,stime_list,etime_list,loading_list,start_list,end_list,price_list]

        #데이터를 보여줄 웹페이지 파일에 전달(크롤링한 데이터가담긴 리스트)
        return render_template("SearchPOP_PD.html",total_list=total_list,old=old,young=young,baby=baby)

@app.route('/SearchPOP_OB',methods = ['POST' ,'GET'])
def SearchPOP_OB():
    if request.method == 'POST':  
            
        chrome_option = Options()
        chrome_option.headless = True
        capability = DesiredCapabilities.CHROME
        capability["pageLoadStrategy"] = "none"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_option)
        driver.get("https://flight.naver.com/")
        time.sleep(1)
        
        #네이버항공권 홈페이지 접속후 편도 버튼 클릭

        # do_query = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[1]/button[2]'
        # driver.find_element(By.XPATH, do_query).click()
        # time.sleep(0.1)

        #직항여부 

        do_query_direct = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[3]/button[2]'

        # # how = input("[1]직항 [2]경유 ( 번호를 입력해주세요. ex) 1 or 2 ")
        # how = 1
        driver.find_element(By.XPATH, do_query_direct).click()
        time.sleep(0.5)
        # #네이버항공권홈페이지에서 [직항만] 버튼 Html 태그를 xpath 형식으로 따옴
        # if (how == "1"):
        #     driver.find_element(By.XPATH, do_query_direct).click()
        #     time.sleep(1)

        #     # elif (how == "2"):
        #     #     driver.find_element(By.XPATH, do_query_direct).click()
        #     #     time.sleep(1)

        # # 출발지 도착지 



        #start = 출발지 데이터
        start = request.form['from']
        start = str(start)

        #end = 도착지 데이터
        end = request.form['to']
        end = str(end)

        query_start = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[1]/b'
        query_end = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]/b'
        textbox = '//*[@id="__next"]/div/div[1]/div[9]/div[1]/div/input'
        choose = '//*[@id="__next"]/div/div[1]/div[9]/div[2]/section/div/a[1]'

        # 출발지 입력
        driver.find_element(By.XPATH, query_start).click()
        time.sleep(0.1)

        driver.find_element(By.XPATH, textbox).click()
        driver.find_element(By.XPATH, textbox).send_keys(start)
        time.sleep(0.1)

        driver.find_element(By.XPATH, choose).click()
        time.sleep(0.1)

        # 도착지 입력
        driver.find_element(By.XPATH, query_end).click()
        time.sleep(0.1)

        driver.find_element(By.XPATH, textbox).click()
        driver.find_element(By.XPATH, textbox).send_keys(end)
        time.sleep(0.1)

        driver.find_element(By.XPATH, choose).click()
        time.sleep(0.1)

        # 날짜

        
        #startday = 가는날 데이터
        startday = request.form['deparure']
        startday = str(startday)

        #endday = 오는날 데이터
        endday = request.form['return']
        endday = str(endday)

        #실제 현재 날짜
        now = datetime.datetime.now()
        #실제 현재 날짜(월)
        month = now.month
        # month = 1

        #웹에서 받아온 가는날 데이터를 월 로만 슬라이싱한 값
        startmonth=startday[1:2]
        #07/02/2022
        
        #오는날 달이 7월 8월 9월 일 경우를 생각해야함
        endmonth = endday[1:2]
        print("-------------------------------------------"+endmonth+"-------------------------------------------")
        
        # 클릭(가는날)
        do_query = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]'
        driver.find_element(By.XPATH, do_query).click()
        time.sleep(0.1)

         #웹에서 입력받은 가는날 값(월) - 현재 날짜(월)
        if((int(startmonth)-month)==0 and (int(endmonth)-month)==0):
            driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[0].click()
            time.sleep(2)
            driver.find_elements(By.XPATH, "//b[text()="+endday[3:5]+"]")[0].click()
            time.sleep(2)
        
        elif((int(startmonth)-month)==0 and (int(endmonth)-month)==1):
            driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[0].click()
            time.sleep(2)
            driver.find_elements(By.XPATH, "//b[text()="+endday[3:5]+"]")[1].click()
            time.sleep(2)

        elif((int(startmonth)-month)==1 and (int(endmonth)-month)==1):
            driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[1].click()
            time.sleep(2)
            driver.find_elements(By.XPATH, "//b[text()="+endday[3:5]+"]")[1].click()
            time.sleep(2)

        elif((int(startmonth)-month)==1 and (int(endmonth)-month)==2):
            driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[1].click()
            time.sleep(2)
            driver.find_elements(By.XPATH, "//b[text()="+endday[3:5]+"]")[2].click()
            time.sleep(2)

        elif((int(startmonth)-month)==2 and (int(endmonth)-month)==2):
            driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[2].click()
            time.sleep(2)
            driver.find_elements(By.XPATH, "//b[text()="+endday[3:5]+"]")[2].click()
            time.sleep(2)

        
        
        # 인원
        old = request.form['old']
        old = int(old)
        young = request.form['young']
        young = int(young)
        baby = request.form['baby']
        baby = int(baby)

        click = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[3]/button[1]'
        old_cnt = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[3]/div/div/div[1]/div[1]/button[2]'
        young_cnt = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[3]/div/div/div[1]/div[2]/button[2]'
        baby_cnt = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[3]/div/div/div[1]/div[3]/button[2]'

        driver.find_element(By.XPATH, click).click()
        time.sleep(0.1)

        if (old > 1):
            for i in range(old-1):
                driver.find_element(By.XPATH, old_cnt).click()
                time.sleep(0.1)

        if (young > 0):
            for i in range(young):
                driver.find_element(By.XPATH, young_cnt).click()
                time.sleep(0.1)

        if (baby > 0):
            for i in range(baby):
                driver.find_element(By.XPATH, baby_cnt).click()
                time.sleep(0.1)

        # 검색 클릭

        do_query = '//*[@id="__next"]/div/div[1]/div[4]/div/div/button'
        try:
            for i in range(10):
                driver.find_element(By.XPATH, do_query).click()
                time.sleep(0.1)
        except:
            print("클릭완료")

        # 정렬

        do_query = '//*[@id="__next"]/div/div[1]/div[6]/div/div[1]/div/div/button'
        cheap = '//*[@id="__next"]/div/div[1]/div[6]/div/div[1]/div/div/div/button[1]'

        try:
            driver.find_element(By.XPATH, do_query).click()
            time.sleep(5)
            driver.find_element(By.XPATH, cheap).click()
            time.sleep(5)

        except:
            print('')
                
        #모든정보를 가져오기위한 스크롤
        body=driver.find_element(By.CSS_SELECTOR, 'body')
        for i in range(20):
            body.send_keys(Keys.END)
            time.sleep(0.1)

        #데이터 담아줄 리스트 생성

        air_list =[]

        go_stime=[] # 출발시간 ex (한국 -> 일본)
        go_etime=[] # 도착시간 ex (한국 -> 일본)

        go_start=[] # 출발공항 ex (한국 -> 일본)
        go_end=[] #출발 -> 도착공항 ex (한국 -> 일본)
        #20~28
        go_total=[] # 한국 -> 일본 총 소요시간

        back_stime=[] # 출발시간 ex (일본 -> 한국)
        back_start=[] # 출발공항 ex (일본 -> 한국)

        back_etime=[] # 도착시간 ex (일본 -> 한국)
        back_end=[] # 도착공항 ex (일본 -> 한국)

        back_total=[] # 일본 -> 한국 총 소요시간

        price_list=[]

        a = [] # 서로 다른 비행기 

        airplane_differ_name = driver.find_elements(By.CSS_SELECTOR,'div.concurrent_RoundDiffAL__22zB4 > div > div > b')
        # (왕복) 서로 다른 비행기의 이름
        for i in airplane_differ_name :
            a.append(i.text)

        # (서로다른 비행기) 리스트 요소를 2개로 묶어주기 위해 씀
        for i in range(0,len(airplane_differ_name),2):
            air_list.append(a[i:i+2])

        # 각각 데이터 요소값

        #air=driver.find_elements(By.CSS_SELECTOR,'div.concurrent_RoundDiffAL__22zB4 > div > div > b')
        airplane_differ_departure_time = driver.find_elements(By.CSS_SELECTOR,'div.concurrent_RoundDiffAL__22zB4 > div.route_Route__2UInh')
        differ_departure_arrival =[] # 서로 다른 비행기의 시간표
        result_differ_time = []
        # 출발 시간 - 도착 시간 (왕복) - 서로 다른 비행기
        for i in airplane_differ_departure_time :
            differ_departure_arrival.append(i.text)
        
        for i in range(0,len(airplane_differ_departure_time),2):
            result_differ_time.append(differ_departure_arrival[i:i+2])
    

        loading=driver.find_elements(By.CSS_SELECTOR,'i.route_info__1RhUH')
        start=driver.find_elements(By.CSS_SELECTOR,'i.route_code__3WUFO')
        price=driver.find_elements(By.CSS_SELECTOR,'div.item_price__1TxJh')


        # 리스트에 값을 저장

   

        for i in range(len(airplane_differ_name)):
            air_list.append(airplane_differ_name[i].text.replace("["," "))

        temp2=[]
        for i in range(0,len(result_differ_time)) :
            temp = result_differ_time[i]
            temp2 = ','.join(temp)
            go_stime.append(temp2[0:5]) # 항공사 이름
            go_start.append(temp2[5:8]) # 출발시간
            go_etime.append(temp2[8:14]) # 출발공항 (8:13)
            go_end.append(temp2[14:17]) # 도착시간
            go_total.append(temp2[18:30]) # 소요시간
            back_stime.append(temp2[31:36]) # 출발시간
        
            back_start.append(temp2[36:39]) # 출발공항
            back_etime.append(temp2[40:45]) # 도착시간
            back_end.append(temp2[45:49]) # 도착공항
            back_total.append(temp2[48:61]) #소요시간

        for i in range(len(price)):
            price_list.append(price[i].text)

        #가져온 데이터들을 딕셔너리로 생성
        # dic = {'항공사':air_list,'출발시간':stime_list,'도착시간':etime_list,'소요시간':loading_list,'출발지':start_list,'도착지':end_list,'가격':price_list}
            # result=  pd.DataFrame(dic)
            # result.to_csv('제목.csv', encoding='EUC-KR')
            
        total_list = [air_list, go_stime, go_start, go_etime, go_end, go_total, back_stime, back_start, back_etime, back_end, back_total, price_list]
                    # 항공사이름 / 출발시간 /출발공항 / 도착시간 /도착공항 /소요시간 // 츌발시간 / 출발공항 / 도착시간   / 도착공항  /소요시간 / 가격

        #데이터를 보여줄 웹페이지 파일에 전달(크롤링한 데이터가담긴 리스트)
        return render_template("SearchPOP_OB.html",total_list=total_list,old=old,young=young,baby=baby)

@app.route('/SearchPOP_2')
def SearchPOP_2():
    return render_template("/SearchPOP_2.html")

@app.route('/SearchPOP_3')
def SearchPOP_3():
    return render_template("/SearchPOP_3.html")

@app.route('/SearchPOP_2_2',methods = ['POST' ,'GET'])
def SearchPOP_2_2():
    if request.method == 'POST':  
        url = 'https://m-flight.naver.com/' # 네이버 항공권 홈페이지 url
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome('p_env/chromedriver.exe', options=options) # 크롬 드라이버 설치후 driver 객체에 크롬창 open 요청
        driver.get(url) # driver 객체에 url 연결하고 네이버항공권 홈페이지를 크롬에서 open
        # 출발지 도착지 
        start = request.form["from"]
        start = str(start)
        end = request.form["to"]
        end = str(end)
        query_start = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[1]/b'
        query_end = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]/b'
        textbox = '//*[@id="__next"]/div/div[1]/div[9]/div[1]/div/input'
        choose = '//*[@id="__next"]/div/div[1]/div[9]/div[2]/section/div/a[1]'
        # 출발지 입력
        driver.find_element(By.XPATH, query_start).click()
        time.sleep(1)
        driver.find_element(By.XPATH, textbox).click()
        driver.find_element(By.XPATH, textbox).send_keys(start)
        time.sleep(1)
        driver.find_element(By.XPATH, choose).click()
        time.sleep(1)
        # 도착지 입력
        driver.find_element(By.XPATH, query_end).click()
        time.sleep(1)
        driver.find_element(By.XPATH, textbox).click()
        driver.find_element(By.XPATH, textbox).send_keys(end)
        time.sleep(1)
        driver.find_element(By.XPATH, choose).click()
        time.sleep(1)

        # #startday = 가는날 데이터
        # startday = request.form['deparure']
        # startday = str(startday)

        # #실제 현재 날짜
        # now = datetime.datetime.now()
        # #실제 현재 날짜(월)
        # month = now.month
        # # month = 1

        # #웹에서 받아온 가는날 데이터를 월 로만 슬라이싱한 값
        # startmonth=startday[1:2]
        # #07/02/2022

        # do_query = '//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]'
        # driver.find_element(By.XPATH, do_query).click()
        # time.sleep(0.1)

        #  #웹에서 입력받은 가는날 값(월) - 현재 날짜(월)
        # if((int(startmonth)-month)==0):
        #     driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[0].click()
        #     time.sleep(2)
            
        # elif((int(startmonth)-month)==1):
        #     driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[1].click()
        #     time.sleep(2)
        # elif((int(startmonth)-month)==2):
        #     driver.find_elements(By.XPATH, "//b[text()="+startday[3:5]+"]")[2].click()
        #     time.sleep(2)


        #추천일정 클릭 
        driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,"//button[text()='추천일정']").click()
        time.sleep(1)
        minus = driver.find_element(By.CSS_SELECTOR,'button.info_inner__OxiW8')
        plus = driver.find_element(By.CSS_SELECTOR,'button.info_outer__2Jw68')
        howlong = request.form["chda"]
        howlong=int(howlong[1])
        if (howlong==1):
            for i in range(2):
                minus.click()
                time.sleep(2)
        elif(howlong==2):
                minus.click()
                time.sleep(2)
        elif(howlong==3):
            ""
        elif(howlong==4):
                plus.click()
                time.sleep(2)
        elif(howlong==5):
            for i in range(2):
                plus.click()
                time.sleep(2)
        elif(howlong==6):
            for i in range(3):
                plus.click()
                time.sleep(2)
        elif(howlong==7):
            for i in range(4):
                plus.click()
                time.sleep(2)
        s_list = [] # 출발일
        e_list=[] # 도착일
        p_list=[] # 가격
        total_list=[]
        path = '//*[@id="__next"]/div/div[1]/div[9]/div[2]/div[1]/div[2]/ul/li['
        for i in range(10):
            start=driver.find_element(By.XPATH,path+str(i+1)+']/span/b[1]').text
            s_list.append(start)
            end=driver.find_element(By.XPATH,path+str(i+1)+']/span/b[2]').text
            e_list.append(end)
            price=driver.find_element(By.XPATH,path+str(i+1)+']/strong').text
            p_list.append(price)
        total_list=[s_list,e_list,p_list]
        return render_template("SearchPOP_2_2.html",total_list=total_list,howlong=howlong)

@app.route('/SearchPOP_3_3',methods = ['POST' ,'GET'])
def SearchPOP_3_3():
    if request.method == 'POST':  

        url = 'https://m-flight.naver.com/flights/everywhere/monthly/SEL'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver=webdriver.Chrome('p_env/chromedriver.exe',options=options)
        driver.get(url)
        driver.implicitly_wait(time_to_wait=10)
        
        
        #출발지 클릭
        path='#__next>div>div>section>div.everywhere_search__1oatc>div.layout_small__3cNDY>div>div>div.searchCondition_top__ytaK_>strong>button:nth-child(1)'
        driver.find_element(By.CSS_SELECTOR,path).click()
        
        # path='//*[@id="__next"]/div/div/section/div[1]/div[2]/div/div/div/div/div[1]/button[1]/b'
        # driver.find_element(By.XPATH,path).click()
        
        #출발지 입력받기
        where = request.form["from"]
        where = str(where)
        if (where==1) :
            driver.find_element(By.XPATH,"//i[text()='인천국제공항']").click()
        elif (where==2) :
            driver.find_element(By.XPATH,"//i[text()='김포국제공항']").click()
        elif (where==3) :
            driver.find_element(By.XPATH,"//i[text()='김해국제공항']").click()
        
        
        # 조건 클릭
        driver.find_element(By.CSS_SELECTOR,"#__next>div>div>main>article>div.everywhere_filters__r7GVb>div>button:nth-child(3)").click()
        
        #스크롤
        pyautogui.moveTo(918, 942)
        pyautogui.click(clicks=5)
        pyautogui.sleep(0.1)
        
        
        money = request.form["pr"]
        money = str(money)
        print(pyautogui.position())
        
        if (money==1) : 
            # 1~50만
            pyautogui.moveTo(898,899)
            pyautogui.drag(-735,0,duration=2)
        
        elif (money==2) :
            # 50~100만
            pyautogui.moveTo(898,899)
            pyautogui.drag(-590,0,duration=2)
        
        
        elif (money==3) :
            # 100~150만
            pyautogui.moveTo(898,899)
            pyautogui.drag(-445,0,duration=2)
        
        elif (money==4) :
            # 150~200만
            pyautogui.moveTo(898,899)
            pyautogui.drag(-290,0,duration=2)
        
        
        elif (money==5) :
            # 200~250만
            pyautogui.moveTo(898,899)
            pyautogui.drag(-140,0,duration=2)
        
        
        elif (money==6) :
            #250-300만
            print("")
        
        driver.find_element(By.XPATH,"//button[text()='확인']").click()
        time.sleep(5)
        
        c_list=[] #추천여행지
        h_list=[] #소요시간
        p_list=[] #가격
        index=[]
        total_list = []
        for i in range(1, 6):
            path='//*[@id="__next"]/div/div/main/article/div[2]/div/div[2]/div['
        
            city=driver.find_element(By.XPATH,path+str(i)+']/button[1]/div/strong/span[2]/i').text
            how=driver.find_element(By.XPATH,path+str(i)+']/button[1]/div/i').text
            price=driver.find_element(By.XPATH,path+str(i)+']/button[1]/div/b/span[1]').text
        
            c_list.append(city)
            h_list.append(how)
            p_list.append(price)
            index.append(i)
        
        dic = {'추천여행지':c_list, "소요시간":h_list,"가격":p_list, '번호':index}
        total_list = [index,c_list,h_list,p_list]


        return render_template("SearchPOP_3_3.html",total_list=total_list)


questions = {
    1: ' 일본 방문이 처음이신가요 ? ',
    2: ' 원하는 숙박시설 유형은 전통적인 숙소인가요 ?',
    3: ' 온천 좋아하시나요 ?',
    4: ' 놀이공원 좋아하시나요 ?',
    5: ' 겨울 분위기를 좋아하시나요 ?',
    6: ' 하얀 해변에 코발트빛으로 가득찬 바다와 수상스키 그리고 스노쿨링을 즐기고 싶나요 ?',
    7: ' 원시림과 비롯한 역사적 명소를 보고 싶나요 ? ',
    8: ' 먹방여행을 즐기고 싶으신가요 ? ',
    9: ' 일본 캐릭터 굿즈를 좋아하고 수집 욕구가 많으신가요 ? ',
    10:' 별 구경을 좋아하시나요 ?',
}

cities = [
    {'city': '도쿄[Tokyo]',              'answers': {1: 1, 2: 0.25, 3: 0.75, 4: 0.5, 5: 0.5, 6: 0, 7: 0.25, 8: 0.25, 9: 1, 10: 1}},
    {'city': '오사카[Osaka]',            'answers': {1: 1, 2: 1, 3: 1, 4: 0.75, 5: 0, 6: 0, 7: 1, 8: 1, 9: 1, 10: 0.25}},
    {'city': '나고야[Nagoya]',           'answers': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.75, 6: 0.25, 7: 0, 8: 1, 9: 0, 10: 0}},
    {'city': '후쿠오카[Fukuoka]',        'answers': {1: 1, 2: 0.75, 3: 0, 4: 0, 5: 0.25 , 6: 1, 7: 0.25 , 8: 0.75, 9: 0, 10: 0.5}},
    {'city': '오키나와[Okinawa]',        'answers': {1: 0, 2: 0.5, 3: 0, 4: 0, 5: 0.25, 6: 0.75, 7: 1, 8: 0, 9: 0, 10: 1}},
    {'city': '삿포로[Sapporo]',          'answers': {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0.25, 9: 0.25, 10: 1}},
]

questions_so_far = []
answers_so_far = []

@app.route('/survey_2')
def survey_2():
    global questions_so_far, answers_so_far

    question = request.args.get('question')
    answer = request.args.get('answer')
    
    if question and answer:
        questions_so_far.append(int(question))
        answers_so_far.append(float(answer))

    probabilities = calculate_probabilites(questions_so_far, answers_so_far)
    print("probabilities", probabilities)

    questions_left = list(set(questions.keys()) - set(questions_so_far))
    if len(questions_left) == 0:
        result = sorted(
            probabilities, key=lambda p: p['probability'], reverse=True)[0]
        return render_template('survey_2.html', result=result['city'])
    else:
        next_question = random.choice(questions_left)
        return render_template('survey_2.html', question=next_question, question_text=questions[next_question])

def calculate_probabilites(questions_so_far, answers_so_far):
    probabilities = []
    for city in cities:
        probabilities.append({
            'city': city['city'],
            'probability': calculate_city_probability(city, questions_so_far, answers_so_far)
        })

    return probabilities

def calculate_city_probability(city, questions_so_far, answers_so_far):
    
    P_city = 1 / len(cities)

    P_answers_given_city = 1
    P_answers_given_not_city = 1
    for question, answer in zip(questions_so_far, answers_so_far):
        P_answers_given_city *= max(
            1 - abs(answer - city_answer(city, question)), 0.01)

        P_answer_not_city = np.mean([1 - abs(answer - city_answer(not_city, question))
                                          for not_city in cities
                                          if not_city['city'] != city['city']])
        P_answers_given_not_city *= max(P_answer_not_city, 0.01)

    P_answers = P_city * P_answers_given_city + \
        (1 - P_city) * P_answers_given_not_city

    P_city_given_answers = (
        P_answers_given_city * P_city) / P_answers

    return P_city_given_answers

def city_answer(city, question):
    if question in city['answers']:
        return city['answers'][question]
    return 0.5

app.config['SECRET'] = "secret!123"
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(message):
    print("Received message : " + message)
    if message != "User connected!":
        send(message, broadcast=True)

@app.route('/')
def index():
    return render_template("Subpage.html")

if __name__=='__main__':
    app.run(debug=True)
    socketio.run(app, host="127.0.0.1") 