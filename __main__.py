

'''
    author : eunsang jang
    date : 2016/11/11
    e-mail : eeunsang7@naver.com

    매우매우 기본적인 crawler 기본 툴입니다

    특이점:
        1. sec_gov의 크롤링을 한다면  xvfb-run python "~~~~~~" 이런식으로 돌리셔야 합니다
'''


import dart_fss_or_kr

startDay = 20161101
endDay = 20161210

dart_fss_or_kr = dart_fss_or_kr.Dart_fss_or_kr(startDay, endDay);


dart_fss_or_kr.startOnlyUrlCrawling()
