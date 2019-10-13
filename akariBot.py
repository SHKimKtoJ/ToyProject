#-*- coding: utf-8 -*-

'''
커스텀 키보드 버튼을 이용하여 날씨&미세먼지 정보와 버스정보를 요청하게 만든 telegram Bot.
'기능'을 입력하여 커스텀 키보드를 시작하게 됨.
https 대응(ssl문제)을 위해 import certifi
'''
#import certifi
import urllib.request
import sys
import requests
import asyncio#비동기식 통신
import time
import telepot
import json
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
#from telepot.loop import MessageLoop
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open




#dicValue = {'hyunElemOpp' : '379001587', 'GNUtoWYApt' : '379001418', 'GNUtoGNU' : '379001419', 'CWNU' : '379000591'}
#dicBusNum = {'100' : '379001000', '101' : '379001010', '122' : '379001220', '160' : '379001600', '163' : '379001630', '164' : '379001640'}
#정류장과 노선 선택을 위한 dictionary
introMsg = '아래 버튼에서 원하는 기능을 선택해 주세요'#기능키보드 시작시 표시되는 문자열.
exitMsg = '키보드가 사라집니다. 다시 검색을 원하실때는 \'기능\'을 입력해 주세요'#기능키보드종료시 표시되는 문자열.
state = None#모든 버튼은 독립적으로 실행됨. 각 과정의 상태를 저장하기 위한 state//해당 state내부에 묶어두는 효과.





async def on_chat_message(msg): #func(msg):#커스템키보드 기능을 담당하는 함수.
    content_type, chat_type, chat_id = telepot.glance(msg)
    #들어오는 메시지의 정보 저장.
    print(content_type, chat_type, chat_id)#처리결과 확인용
    global state
    print(state)#각 과정의 state 상태를 확인
    #print(type(msg))
    print(msg)
    flag = False#버스정보를 받아와 출력을 위한 처리기능 동작을 위한 flag. false로 초기화 후 True인 경우 버스정보 php로 값을 보내주기 위한 기능을 실행.
    flagW = False#날씨정보용 flag
    station = ''
    busNo = ''
    curLet: str
    curLon: str
    #value에 삽입하여 get으로 보내기 위한 변수.
   
    
    if content_type == 'text':
        if state is None:
            if msg['text'] == '기능':
                await bot.sendMessage(chat_id, introMsg, reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "위치기반날씨", request_location = True), KeyboardButton(text = "버스")], [KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '기능'
        elif state == '기능':
            if msg['text'] == '버스':
                await bot.sendMessage(chat_id, introMsg, reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "정류장선택"), KeyboardButton(text = "정류장&노선선택")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '버스'
            elif msg['text'] == '키보드종료':
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
        elif state == '버스':
            if msg['text'] == '정류장선택':
                await bot.sendMessage(chat_id, introMsg, reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "현동초등학교맞은편"), KeyboardButton(text = "창원대학교종점")], [KeyboardButton(text = "경남대남부터미널(월영apt)"), KeyboardButton(text = "경남대남부터미널(경남대)")], [KeyboardButton(text = "월영아파트종점(월영1차apt)"), KeyboardButton(text = "월영아파트종점(월영동공원)")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '정류장선택'
            elif msg['text'] == '정류장&노선선택':
                await bot.sendMessage(chat_id, '정류장선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "현동초등학교맞은편"), KeyboardButton(text = "창원대학교종점")], [KeyboardButton(text = "경남대남부터미널(월영apt)"), KeyboardButton(text = "경남대남부터미널(경남대)")], [KeyboardButton(text = "월영아파트종점(월영1차apt)"), KeyboardButton(text = "월영아파트종점(월영동공원)")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '정류장&노선선택'
            elif msg['text'] == '이전메뉴':
                await bot.sendMessage(chat_id, introMsg, reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "위치기반날씨", request_location = True), KeyboardButton(text = "버스")], [KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '기능'
            elif msg['text'] == '키보드종료':
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
        elif state == '정류장선택':
            flag = True
            if msg['text'] == '현동초등학교맞은편':
                station = '379001587'
                state = '정류장선택'
            elif msg['text'] == '창원대학교종점':
                station = '379000591'
                state = '정류장선택'
            elif msg['text'] == '경남대남부터미널(월영apt)':
                station = '379001418'
                state = '정류장선택'
            elif msg['text'] == '경남대남부터미널(경남대)':
                station = '379001419'
                state = '정류장선택'
            elif msg['text'] == '월영아파트종점(월영1차apt)':
                station = '379001441'
                state = '정류장선택'
            elif msg['text'] == '월영아파트종점(월영동공원)':
                station = '379001443'
                state = '정류장선택'
            elif msg['text'] == '이전메뉴':
                flag = False
                await bot.sendMessage(chat_id, introMsg, reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "정류장선택"), KeyboardButton(text = "정류장&노선선택")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '버스'
            elif msg['text'] == '키보드종료':
                flag = False
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
            #state = None
        elif state == '정류장&노선선택':
            if msg['text'] == '현동초등학교맞은편':
                await bot.sendMessage(chat_id, '노선 선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "160"), KeyboardButton(text = "163")],[KeyboardButton(text = "164"), KeyboardButton(text = "254")],[KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = 'HDEopps'
            elif msg['text'] == '창원대학교종점':
                await bot.sendMessage(chat_id, '노선 선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "100"), KeyboardButton(text = "101")],[KeyboardButton(text = "122"), KeyboardButton(text = "이전메뉴")],[KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = 'cwnu'
            elif msg['text'] == '경남대남부터미널(월영apt)':
                await bot.sendMessage(chat_id, '노선 선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "160"), KeyboardButton(text = "163")],[KeyboardButton(text = "164"), KeyboardButton(text = "이전메뉴")],[KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = 'KNUWY'
            elif msg['text'] == '경남대남부터미널(경남대)':
                await bot.sendMessage(chat_id, '노선 선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "100"), KeyboardButton(text = "101")],[KeyboardButton(text = "122"), KeyboardButton(text = "이전메뉴")],[KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = 'KNU'
            elif msg['text'] == '월영아파트종점(월영1차apt)':
                await bot.sendMessage(chat_id, '노선 선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "251"), KeyboardButton(text = "254")],[KeyboardButton(text = "259"), KeyboardButton(text = "이전메뉴")],[KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = 'WYApt1st'
            elif msg['text'] == '월영아파트종점(월영동공원)':
                await bot.sendMessage(chat_id, '노선 선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "160"), KeyboardButton(text = "163")],[KeyboardButton(text = "164"), KeyboardButton(text = "254")],[KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = 'WYAptPark'
            elif msg['text'] == '이전메뉴':
                await bot.sendMessage(chat_id, introMsg, reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "정류장선택"), KeyboardButton(text = "정류장&노선선택")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '버스'
            elif msg['text'] == '키보드종료':
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
        elif state == 'HDEopps':
            flag = True
            if msg['text'] == '160':
                station = '379001587'
                busNo = '379001600'
                state = 'HDEopps'
            elif msg['text'] == '163':
                station = '379001587'
                busNo = '379001630'
                state = 'HDEopps'
            elif msg['text'] == '164':
                station = '379001587'
                busNo = '379001640'
                state = 'HDEopps'
            elif msg['text'] == '254':
                station = '379001587'
                busNo = '379002540'
                state = 'HDEopps'
            elif msg['text'] == '이전메뉴':
                flag = False
                await bot.sendMessage(chat_id, '정류장선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "현동초등학교맞은편"), KeyboardButton(text = "창원대학교종점")], [KeyboardButton(text = "경남대남부터미널(월영apt)"), KeyboardButton(text = "경남대남부터미널(경남대)")], [KeyboardButton(text = "월영아파트종점(월영1차apt)"), KeyboardButton(text = "월영아파트종점(월영동공원)")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '정류장&노선선택'
            elif msg['text'] == '키보드종료':
                flag = False
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
        elif state == 'cwnu':
            flag = True
            if msg['text'] == '100':
                station = '379000591'
                busNo = '379001000'
                state = 'cwnu'
            elif msg['text'] == '101':
                station = '379000591'
                busNo = '379001010'
                state = 'cwnu'
            elif msg['text'] == '122':
                station = '379000591'
                busNo = '379001220'
                state = 'cwnu'
            elif msg['text'] == '이전메뉴':
                flag = False
                await bot.sendMessage(chat_id, '정류장선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "현동초등학교맞은편"), KeyboardButton(text = "창원대학교종점")], [KeyboardButton(text = "경남대남부터미널(월영apt)"), KeyboardButton(text = "경남대남부터미널(경남대)")], [KeyboardButton(text = "월영아파트종점(월영1차apt)"), KeyboardButton(text = "월영아파트종점(월영동공원)")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '정류장&노선선택'
            elif msg['text'] == '키보드종료':
                flag = False
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
        elif state == 'KNUWY':
            flag = True
            if msg['text'] == '160':
                station = '379001418'
                busNo = '379001600'
                state = 'KNUWY'
            elif msg['text'] == '163':
                station = '379001418'
                busNo = '379001630'
                state = 'KNUWY'
            elif msg['text'] == '164':
                station = '379001418'
                busNo = '379001640'
                state = 'KNUWY'
            elif msg['text'] == '이전메뉴':
                flag = False
                await bot.sendMessage(chat_id, '정류장선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "현동초등학교맞은편"), KeyboardButton(text = "창원대학교종점")], [KeyboardButton(text = "경남대남부터미널(월영apt)"), KeyboardButton(text = "경남대남부터미널(경남대)")], [KeyboardButton(text = "월영아파트종점(월영1차apt)"), KeyboardButton(text = "월영아파트종점(월영동공원)")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '정류장&노선선택'
            elif msg['text'] == '키보드종료':
                flag = False
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
        elif state == 'KNU':
            flag = True
            if msg['text'] == '100':
                station = '379001419'
                busNo = '379001000'
                state = 'KNU'
            elif msg['text'] == '101':
                station = '379001419'
                busNo = '379001010'
                state = 'KNU'
            elif msg['text'] == '122':
                station = '379001419'
                busNo = '379001220'
                state = 'KNU'
            elif msg['text'] == '이전메뉴':
                flag = False
                await bot.sendMessage(chat_id, '정류장선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "현동초등학교맞은편"), KeyboardButton(text = "창원대학교종점")], [KeyboardButton(text = "경남대남부터미널(월영apt)"), KeyboardButton(text = "경남대남부터미널(경남대)")], [KeyboardButton(text = "월영아파트종점(월영1차apt)"), KeyboardButton(text = "월영아파트종점(월영동공원)")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '정류장&노선선택'
            elif msg['text'] == '키보드종료':
                flag = False
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
        elif state == 'WYApt1st':
            flag = True
            if msg['text'] == '251':
                station = '379001441'
                busNo = '379002510'
                state = 'WYApt1st'
            elif msg['text'] == '254':
                station = '379001441'
                busNo = '379002540'
                state = 'WYApt1st'
            elif msg['text'] == '259':
                station = '379001441'
                busNo = '379002590'
                state = 'WYApt1st'
            elif msg['text'] == '이전메뉴':
                flag = False
                await bot.sendMessage(chat_id, '정류장선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "현동초등학교맞은편"), KeyboardButton(text = "창원대학교종점")], [KeyboardButton(text = "경남대남부터미널(월영apt)"), KeyboardButton(text = "경남대남부터미널(경남대)")], [KeyboardButton(text = "월영아파트종점(월영1차apt)"), KeyboardButton(text = "월영아파트종점(월영동공원)")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '정류장&노선선택'
            elif msg['text'] == '키보드종료':
                flag = False
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
        elif state == 'WYAptPark':
            flag = True
            if msg['text'] == '160':
                station = '379001443'
                busNo = '379001600'
                state = 'WYAptPark'
            elif msg['text'] == '163':
                station = '379001443'
                busNo = '379001630'
                state = 'WYAptPark'
            elif msg['text'] == '164':
                station = '379001443'
                busNo = '379001640'
                state = 'WYAptPark'
            elif msg['text'] == '254':
                station = '379001443'
                busNo = '379002540'
                state = 'WYAptPark'
            elif msg['text'] == '이전메뉴':
                flag = False
                await bot.sendMessage(chat_id, '정류장선택', reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = "현동초등학교맞은편"), KeyboardButton(text = "창원대학교종점")], [KeyboardButton(text = "경남대남부터미널(월영apt)"), KeyboardButton(text = "경남대남부터미널(경남대)")], [KeyboardButton(text = "월영아파트종점(월영1차apt)"), KeyboardButton(text = "월영아파트종점(월영동공원)")], [KeyboardButton(text = "이전메뉴"), KeyboardButton(text = "키보드종료")]], resize_keyboard = True))
                state = '정류장&노선선택'
            elif msg['text'] == '키보드종료':
                flag = False
                await bot.sendMessage(chat_id, exitMsg, reply_markup = ReplyKeyboardRemove())#종료버튼.
                state = None
    elif content_type == 'location':#위치정보의 경우 봇에서 위치정보 제공 동의시 메시지에 등록됨.
        flagW = True
        curLet = str(msg['location']['latitude'])
        curLon = str(msg['location']['longitude'])
        state = '기능'
             
    
    if flag == True :
        value = {'station' : station, 'busNo' : busNo}
        req = requests.get('http://52.231.189.115/getBusAPI.php/get', params = value)#php에 _Get으로 보내기 위한 기능.
        url = urllib.request.urlopen(req.url).read()#값을 받은 페이지가 처리한 결과값을 읽어옴.
        message = url.decode('utf-8')#읽어온 결과값이 hexcode. 읽을 수 있게 utf-8로 디코딩.
        await bot.sendMessage(chat_id, message)
        
    elif flagW == True:
        flagD = False
        appkey = '57cbfd47-fb90-4e87-92bf-156ccc361d79'
        urlCurW = 'https://api2.sktelecom.com/weather/current/hourly?version=2&lat='+curLet+'&lon='+curLon+'&appKey='+appkey
        reqCurWeather = requests.get(url = urlCurW)
        jsonCur = reqCurWeather.json()
        city = str(jsonCur['weather']['hourly'][0]['grid']['city'])#미세먼지정보를 시,도 이름으로 호출하기 위한 변수
        county = str(jsonCur['weather']['hourly'][0]['grid']['county'])
        temCur = str(jsonCur['weather']['hourly'][0]['temperature']['tc'])
        temMin = str(jsonCur['weather']['hourly'][0]['temperature']['tmin'])
        temMax = str(jsonCur['weather']['hourly'][0]['temperature']['tmax'])
        windSpd = str(jsonCur['weather']['hourly'][0]['wind']['wspd'])
        humidity = str(jsonCur['weather']['hourly'][0]['humidity'])
        weatherState = str(jsonCur['weather']['hourly'][0]['sky']['name'])
        urlDust = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey=qj9in7MQl0zJbAx185AyjJX1lu9r1a0r24DbUg0uEuT9C0iK%2Fge9JYvwdFInIGaEXL3nUX8NqVUnwNOpZdFKEQ%3D%3D&numOfRows=20&pageSize=20&pageNo=1&startPage=1&sidoName='+city+'&ver=1.3&_returnType=json'
        reqDust = requests.get(url = urlDust)
        jsonDust = reqDust.json()
        #미세먼지 등급.
        if county == '창원시 마산합포구' or county == '창원시 마산회원구':#회원동측정소
            flagD = True
            stationName = str(jsonDust['list'][0]['stationName'])
            pm10Value = str(jsonDust['list'][0]['pm10Value'])
            pm10Grade = str(jsonDust['list'][0]['pm10Grade1h'])
            pm25Value = str(jsonDust['list'][0]['pm25Value'])
            pm25Grade = str(jsonDust['list'][0]['pm25Grade1h'])
            msgD = stationName+" 측정소의 현재 미세먼지 등급은 pm10: "+pm10Value+"㎍/㎥, "+pm10Grade+"등급 & pm2.5: "+pm25Value+"㎍/㎥, "+pm25Grade+"등급으로"
        elif county == '창원시 의창구':#용지동 측정소
            flagD = True
            stationName = str(jsonDust['list'][8]['stationName'])
            pm10Value = str(jsonDust['list'][8]['pm10Value'])
            pm10Grade = str(jsonDust['list'][8]['pm10Grade1h'])
            pm25Value = str(jsonDust['list'][8]['pm25Value'])
            pm25Grade = str(jsonDust['list'][8]['pm25Grade1h'])
            msgD = stationName+" 측정소의 현재 미세먼지 등급은 pm10: "+pm10Value+"㎍/㎥, "+pm10Grade+"등급 & pm2.5: "+pm25Value+"㎍/㎥, "+pm25Grade+"등급으로"
        elif county == '창원시 성산구':#사파동 측정소
            flagD = True
            stationName = str(jsonDust['list'][10]['stationName'])
            pm10Value = str(jsonDust['list'][10]['pm10Value'])
            pm10Grade = str(jsonDust['list'][10]['pm10Grade1h'])
            pm25Value = str(jsonDust['list'][10]['pm25Value'])
            pm25Grade = str(jsonDust['list'][10]['pm25Grade1h'])
            msgD = stationName+" 측정소의 현재 미세먼지 등급은 pm10: "+pm10Value+"㎍/㎥, "+pm10Grade+"등급 & pm2.5: "+pm25Value+"㎍/㎥, "+pm25Grade+"등급으로"
        elif county == '창원시 진해구':#경화동 측정소
            flagD = True
            stationName = str(jsonDust['list'][11]['stationName'])
            pm10Value = str(jsonDust['list'][11]['pm10Value'])
            pm10Grade = str(jsonDust['list'][11]['pm10Grade1h'])
            pm25Value = str(jsonDust['list'][11]['pm25Value'])
            pm25Grade = str(jsonDust['list'][11]['pm25Grade1h'])
            msgD = stationName+" 측정소의 현재 미세먼지 등급은 pm10: "+pm10Value+"㎍/㎥, "+pm10Grade+"등급 & pm2.5: "+pm25Value+"㎍/㎥, "+pm25Grade+"등급으로"
        else:
            flagD = False
            msgD = "현재 창원시 이외의 미세먼지 정보는 제공하지 않습니다."
            Dgrade = ""
        #등급에따른 결과
        
        # if pm10Grade == "":
        #     pm10Grade = '6'
        # if pm25Grade == "":
        #     pm25Grade = '6'
        #빈 스트링이 들어왔을때 else로 보내기 위한 값 지정. 추후 빈 스트링에 대한 메시지 필요시 해제할 예정
        if flagD == True:
            if pm10Grade == '4' or pm25Grade == '4':
                Dgrade = " \'매우나쁨\' 입니다. 외출을 자제해주세요."
            elif pm10Grade == '3' or pm25Grade == '3':
                Dgrade = " \'나쁨\' 입니다. 마스크 챙겨가세요!"
            elif pm10Grade == '2' or pm25Grade == '2':
                Dgrade = " \'보통\' 입니다."
            elif pm10Grade == '1' or pm25Grade == '1':
                Dgrade = " \'좋음\' 입니다."
            else:
                Dgrade = " 기상청api의 문제로 등급을 가져올 수 없습니다."
            
        msgW = county+"의 현재온도는 "+temCur+"도 최저온도는 "+temMin+"도 최고온도는 "+temMax+"도 풍속은 "+windSpd+"m/s 습도는 "+humidity+"% 현재 날씨는 \""+weatherState+"\" 입니다.\n"
        totalMsg = msgW+msgD+Dgrade
        await bot.sendMessage(chat_id, totalMsg)
        
    



TOKEN = '570273389:AAG3goKeDHBiRt_il8uqpjR2mV8G2spmrFU'
bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, {'chat' : on_chat_message}).run_forever())
print("idle")

loop.run_forever()

 



