


from module import DBManager
from urllib.request import urlopen
import json
import time
import copy
import uuid
import codecs
import requests
import datetime
from scrapy.http import HtmlResponse
from scrapy.selector import Selector


dbManager = DBManager.DBManager('link_info')



# AUTHENTICATION_KEY dart의 API를 이용하기 위한 인증키입니다.
# 지금은 장은상의 인증키입니다. 하루 10000건 까지 가능합니다.

'''
    define 목록
    AUTHENTICATION_KEY dart의 API를 이용하기 위한 인증키입니다. "장은상" 인증키 입니다
    INFINITE_NUM 단순 숫자
    CHECK_CAN_SEARCH는 DART를 크롤링할지 말지의 여부를 나타내는 것입니다
'''
AUTHENTICATION_KEY = '20cf7f9d2fa26ab78d7cd2f2079ae91825b6599d'
INFINITE_NUM = 987654321
CHECK_CAN_SEARCH = '1'
LINK_DIRECTORY = '/home/data/dart/2016'
URL_JSON_FILE_PATH = './dart_fss_or_kr/dart_list.json'


'''
    기본정보와 URL을 저장해 두는 함수입니다
    만약 crawling할 부분을 제외하고 싶다면 앞에 #를 달아 주석처리하시면 됩니다
'''
def crawlBasicInformation(startDay, endDay):
    crawling("A001", "정기공시", "사업보고서", startDay, endDay)
    crawling("A002", "정기공시", "반기보고서", startDay, endDay)
    crawling("A003", "정기공시", "분기보고서", startDay, endDay)
    crawling("B001", "주요사항보고서", "주요사항보고서P", startDay, endDay)
    crawling("B002", "주요사항보고서", "주요경영사항신고", startDay, endDay)
    crawling("B003", "주요사항보고서", "최대주주등과의거래신고", startDay, endDay)
    crawling("C001", "발행공시", "증권신고(지분증권)", startDay, endDay)
    crawling("C002", "발행공시", "증권신고(채무증권)", startDay, endDay)
    crawling("C003", "발행공시", "증권신고(파생결합증권)", startDay, endDay)
    crawling("C004", "발행공시", "증권신고(합병등)", startDay, endDay)
    crawling("C005", "발행공시", "증권신고(기타등)", startDay, endDay)
    crawling("C006", "발행공시", "소액공모(지분증권)", startDay, endDay)
    crawling("C007", "발행공시", "소액공모(채무증권)", startDay, endDay)
    crawling("C008", "발행공시", "소액공모(파생결합증권)", startDay, endDay)
    crawling("C009", "발행공시", "소액공모(합병등)", startDay, endDay)
    crawling("C010", "발행공시", "소액공모(기타)", startDay, endDay)
    crawling("C011", "발행공시", "호가중개시스템을통한소액매출", startDay, endDay)
    crawling("D001", "지분공시", "주식등의대량보유상황보고서", startDay, endDay)
    crawling("D002", "지분공시", "임원주요주주특정증권등소유상황보고서", startDay, endDay)
    crawling("D003", "지분공시", "의결권대리행사권유", startDay, endDay)
    crawling("D004", "지분공시", "공개매수", startDay, endDay)
    crawling("E001", "기타공시", "자기주식취득/처분", startDay, endDay)
    crawling("E002", "기타공시", "신탁계약체결/해지", startDay, endDay)
    crawling("E003", "기타공시", "합병등종료보고서", startDay, endDay)
    crawling("E004", "기타공시", "주식매수선택권부여에관한신고", startDay, endDay)
    crawling("E005", "기타공시", "사외이사에관한신고", startDay, endDay)
    crawling("E006", "기타공시", "주주총회소집공고", startDay, endDay)
    crawling("E007", "기타공시", "시장조성/안정조작", startDay, endDay)
    crawling("E008", "기타공시", "합병등신고서(자본시장법 이전)", startDay, endDay)
    crawling("E009", "기타공시", "금융위등록/취소(자본시장법 이전)", startDay, endDay)
    crawling("F001", "외부감사보고서", "감사보고서", startDay, endDay)
    crawling("F002", "외부감사보고서", "연결감사보고서", startDay, endDay)
    crawling("F003", "외부감사보고서", "결합감사보고서", startDay, endDay)
    crawling("F004", "외부감사보고서", "회계법인사업보고서", startDay, endDay)
    crawling("G001", "펀드공시", "증권신고(집합투자증권-신탁형)", startDay, endDay)
    crawling("G002", "펀드공시", "증권신고(집합투자증권-회사형)", startDay, endDay)
    crawling("G003", "펀드공시", "증권신고(집합투자증권-합병)", startDay, endDay)
    crawling("H001", "자산유동화", "자산유동화계획/양도등록", startDay, endDay)
    crawling("H002", "자산유동화", "사업/반기/분기보고서", startDay, endDay)
    crawling("H003", "자산유동화", "증권신고(유동화증권등)", startDay, endDay)
    crawling("H004", "자산유동화", "채권유동화계획/양도등록", startDay, endDay)
    crawling("H005", "자산유동화", "수시보고", startDay, endDay)
    crawling("H006", "자산유동화", "주요사항보고서", startDay, endDay)

    # 아직 I는 불가능하다
    # self.crawlingAPI("I001", "거래서공시", "수시공시", startDay, endDay)
    # self.crawlingAPI("I002", "거래서공시","공정공시", startDay, endDay)
    # self.crawlingAPI("I003", "거래서공시", "시장조치/안내",startDay, endDay)
    # self.crawlingAPI("I004", "거래서공시", "지분공시",startDay, endDay)
    # self.crawlingAPI("I005", "거래서공시", "증권투자회사", startDay, endDay)
    # self.crawlingAPI("I006", "거래서공시", "채권공시",startDay, endDay)

    crawling("J001", "공정위공시", "대규모내부거래관련", startDay, endDay)
    crawling("J002", "공정위공시", "대규모내부거래관련(구)", startDay, endDay)
    crawling("J004", "공정위공시", "기업집단현황공시", startDay, endDay)
    crawling("J005", "공정위공시", "비상장회사중요사항공시", startDay, endDay)
    crawling("J006", "공정위공시", "기타공정위공시", startDay, endDay)


'''
    dart 사이트에서 type별로 크롤링합니다.
    시작과 끝을 정할 수 있습니다.
'''
def crawling(dartType, tagName1,tagName2, startDay, endDay):
    countOfCrawlingItem = 0
    saveUrlList = []

    # -----------1부 dart api를 이용하여 웹 페이지 URL(PDF URL이 아님)을 가져오는 부분-----------
    for page in range(1, INFINITE_NUM):

       
        currentUrl = 'http://dart.fss.or.kr/api/search.json?' \
              'auth=' + AUTHENTICATION_KEY + \
              '&http://dart.fss.or.kr/api/search.xml?' \
              '&bsn_tp=' + dartType + \
              '&page_set=100&start_dt=' + str(startDay) + '&end_dt=' + str(endDay) + '&page_no=' + str(page)
        print (currentUrl)
        urlData = urlopen(currentUrl).read().decode('utf8')
        jsonData = json.loads(urlData)

        time.sleep(1)

        #현재 페이지가 0 이라면
        if (jsonData["total_page"] == 0):
            print ("크롤링할 자료가 없습니다")
            break

        # 크롤링을 다 했다면 다 했다고 말하고 끝낸다
        if (jsonData["total_page"] - page == -1):
            print ("크롤링을 끝맞췄습니다")
            break

        # 크롤링 할 아이템의 개수를 세놓은다
        # 그리고 크롤링 할 주소를 saveUrlList에 저장시켜놓는다
        for item in jsonData["list"]:
            countOfCrawlingItem = countOfCrawlingItem + 1
            rcp_no = copy.deepcopy(item["rcp_no"])
            saveUrlList.append(rcp_no)

    # -----------2부 웹페이지 url을 가지고 기본정보들을 가져오는 부분 -----------
    file = codecs.open(URL_JSON_FILE_PATH, 'a', encoding='utf-8')

    for countOfNum in range(countOfCrawlingItem):
        print (str(countOfNum) + "번째 진행되고 있습니다. 곧 완료 될것입니다")
        currentUrl = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=%d" % int(saveUrlList[countOfNum])
        time.sleep(5)
        responseContent = requests.get(currentUrl, stream=True)
        response = Selector(HtmlResponse(url=currentUrl, body=(responseContent.content)))
        sel = response.xpath('/html/head')

        #아이템 생성
        item = {}
        temp = sel.xpath('title/text()').extract()
        tempData = temp[0].strip('\r\n').split('/')
        item['company_name'] = tempData[0]
        item['title'] = ''
        item['publish_place'] = tempData[0]
        item['report_name'] = tempData[1]
        tempLink = ''.join(sel.xpath('//*[@id="north"]/div[2]/ul/li[1]/a/@onclick').extract())
        item['link'] = int(tempLink[17:31])
        tempPdfDownloadLink = ''.join(sel.xpath('//*[@id="north"]/div[2]/ul/li[1]/a/@onclick').extract())
        item['pdf_download_link'] = "http://dart.fss.or.kr/pdf/download/pdf.do?rcp_no=" + str(
        item['link']) + "&dcm_no=" + str(int(tempPdfDownloadLink[35:42]))
        item['link'] = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=" + str(item['link'])
        item['link_directory'] = LINK_DIRECTORY
        item['file_name'] = ''.join(str(uuid.uuid1()).split('-'))
        item['content'] = ''
        item['search_on'] = CHECK_CAN_SEARCH
        item['tag'] = [tagName1, tagName2]
        item['count_query'] = 0
        item['document_type'] = 'pdf'
        item['date'] = tempData[2]


        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        file.write(line)

    file.close()
