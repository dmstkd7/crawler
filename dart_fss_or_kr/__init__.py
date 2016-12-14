


'''
    author : eunsang jang
    date : 2016/12/10
    e-mail : eeunsang7@naver.com
    dart.fss.or.kr에 정기공시(사업 보고서, 반기보고서, 분기 보고서), 외부감사관련(감사보고서)
    를 크롤링 하기 위한 dart package 입니다.
    CrawlProperties.py에서 각 속성(다운로드 링크, 레포트 네임, 날짜 등등) 을 가져오는 것이고
    DBManager.py에서는 mongodb를 연결하기 위한 class가 있습니다
    PdfDownloader.py 에서는 CrawlProperties 를 통해 얻어진 정보를 가지고 pdf를
    파일시스템에 저장 시키고 mongoDB에 데이터를 집어 넣는 것입니다
    pdfToText의 경우 pdfMiner를 이용하여 pdf를 text파일로 변환 시키는 클래스 입니다.

'''


from .crawlBasicInformation import crawlBasicInformation
from .downloadPdfFile import downloadPdfFile


'''
    define 목록
    LINK_DIRECTORY는 DART의 PDF 파일 저장 위치를 의미한다.
'''


class Dart_fss_or_kr:
    def __init__(self, startDay, endDay):
        #이렇게 하는게 맞나???
        self.PATH_DIRECTORY = '/home/data/dart/2016/'
        self.startDay = startDay
        self.endDay = endDay

    '''
        startDartCrawling의 경우는 URL을 JSON으로 저장시키고 이후 JSON파일을 한 줄씩
        읽어 PDF를 다운로드 시킵니다
    '''
    def startCrawling(self):
        print("공시자료 Dart를 Crawling 합니다. URL을 가져오고 이후 PDF를 다운로드 받습니다.")
        crawlBasicInformation(self.startDay, self.endDay)
        print("URL 자료를 잘 저장시켰습니다. 앞으로 PDF를 다운로드 시키겠습니다")
        downloadPdfFile(self.PATH_DIRECTORY)



    '''
        단순히 URL만 크롤링하는 것입니다
    '''
    def startOnlyUrlCrawling(self):
        crawlBasicInformation(self.startDay, self.endDay)



    '''
        PDF만을 크롤링하는 것입니다
    '''
    def startOnlyPdfCrawling(self):
        downloadPdfFile(self.PATH_DIRECTORY)



