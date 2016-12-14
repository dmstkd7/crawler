
'''
    author : eunsang jang
    date : 2016/11/23
    e-mail : eeunsang7@naver.com
    www.fsc.go.kr에 보도자료, 금융위의결정보, 주요업무계획 다운로드, 금융정책, 은행정책,
    보험정책, 중소서민정책, 금융소비자, 자본시장정책, 국제협력, 자체검사결과
    국회예산, 정부위원회현황 등을 다운로드 하는 것입니다
    CrawlProperties.py에서 각 속성(다운로드 링크, 레포트 네임, 날짜 등등) 을 가져오는 것이고
    DBManager.py에서는 mongodb를 연결하기 위한 class가 있습니다
    PdfDownloader.py 에서는 CrawlProperties 를 통해 얻어진 정보를 가지고 pdf를
    파일시스템에 저장 시키고 mongoDB에 데이터를 집어 넣는 것입니다
    pdfToText의 경우 pdfMiner를 이용하여 pdf를 text파일로 변환 시키는 클래스 입니다.

'''







'''
    author : eunsang jang
    date : 2016/11/23
    e-mail : eeunsang7@naver.com
    www.fsc.go.kr에 보도자료, 금융위의결정보, 주요업무계획 다운로드, 금융정책, 은행정책,
    보험정책, 중소서민정책, 금융소비자, 자본시장정책, 국제협력, 자체검사결과
    국회예산, 정부위원회현황 등을 다운로드 하는 것입니다
    CrawlProperties.py에서 각 속성(다운로드 링크, 레포트 네임, 날짜 등등) 을 가져오는 것이고
    DBManager.py에서는 mongodb를 연결하기 위한 class가 있습니다
    PdfDownloader.py 에서는 CrawlProperties 를 통해 얻어진 정보를 가지고 pdf를
    파일시스템에 저장 시키고 mongoDB에 데이터를 집어 넣는 것입니다
    pdfToText의 경우 pdfMiner를 이용하여 pdf를 text파일로 변환 시키는 클래스 입니다.

'''





from .crawlBasicInformation import crawlBasicInformation
from .downloadPdfFile import downloadPdfFile


'''
    금융위원회 목록 리스트는 다음과 같다
    0 - > "보도자료" : "http://www.fsc.go.kr/info/ntc_news_list.jsp?menu=7210100&bbsid=BBS0030",
    1 - > "금융위의결정보" : "http://www.fsc.go.kr/info/con_fscc_list.jsp?menu=7220100&bbsid=BBS0024",
    2 - > "금융정책" : "http://www.fsc.go.kr/policy/ply_comm_list.jsp?menu=7310100",
    3 - > "은행정책" : "http://www.fsc.go.kr/policy/ply_bank_list.jsp?menu=7310400",
    4 - > "보험정책" : "http://www.fsc.go.kr/policy/ply_insr_list.jsp?menu=7310500",
    5 - > "중소서민정책" : "http://www.fsc.go.kr/policy/ply_comp_list.jsp?menu=7310200",
    6 - > "금융소비자" : "http://www.fsc.go.kr/policy/ply_rest_list.jsp?menu=7310300",
    7 - > "자본시장정책" : "http://www.fsc.go.kr/policy/ply_capi_list.jsp?menu=7310600",
    8 - > "국제협력" : "http://www.fsc.go.kr/policy/ply_glob_list.jsp?menu=7310700",
    9 - > "자체감사결과" : "http://www.fsc.go.kr/policy/ply_conduct_list.jsp?menu=7310810&bbsid=BBS0125",
    10 - > "국회예산" : "http://www.fsc.go.kr/policy/ply_asse_list.jsp?menu=7310900&bbsid=BBS0008",
    11 - > "정부위원회현황" : "http://www.fsc.go.kr/policy/ply_gov_list.jsp?menu=7310815&bbsid=BBS0126"
    다음을 크롤링 하겠다

    2016년 주요업무계획 다운로드는 다운로드 하지 않았다

    !!!!!!!!! 만약 위의 LIST에서 제외시키고 싶거나 추가하고 싶다면 __init__.py부분의 downloadList에 데이터를 빼거나 추가하면 됩니다 !!!!!!!!!
'''


class Fsc_go_kr:
    def __init__(self, startDay, endDay, directoryPath):
        #이렇게 하는게 맞나???
        self.directoryPath = directoryPath
        self.startDay = startDay
        self.endDay = endDay
        self.downloadList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
        self.menuList = ["http://www.fsc.go.kr/info/ntc_news_list.jsp?menu=7210100&bbsid=BBS0030",
                        "http://www.fsc.go.kr/info/con_fscc_list.jsp?menu=7220100&bbsid=BBS0024",
                        "http://www.fsc.go.kr/policy/ply_comm_list.jsp?menu=7310100",
                        "http://www.fsc.go.kr/policy/ply_bank_list.jsp?menu=7310400",
                        "http://www.fsc.go.kr/policy/ply_insr_list.jsp?menu=7310500",
                        "http://www.fsc.go.kr/policy/ply_comp_list.jsp?menu=7310200",
                        "http://www.fsc.go.kr/policy/ply_rest_list.jsp?menu=7310300",
                        "http://www.fsc.go.kr/policy/ply_capi_list.jsp?menu=7310600",
                        "http://www.fsc.go.kr/policy/ply_glob_list.jsp?menu=7310700",
                        "http://www.fsc.go.kr/policy/ply_conduct_list.jsp?menu=7310810&bbsid=BBS0125",
                        "http://www.fsc.go.kr/policy/ply_asse_list.jsp?menu=7310900&bbsid=BBS0008",
                        "http://www.fsc.go.kr/policy/ply_gov_list.jsp?menu=7310815&bbsid=BBS0126"
                        ]


    '''
        startDartCrawling의 경우는 URL을 JSON으로 저장시키고 이후 JSON파일을 한 줄씩
        읽어 PDF를 다운로드 시킵니다
    '''
    def startCrawling(self):
        print("FSC 금융위원회를 Crawling 합니다. URL을 가져오고 이후 PDF를 다운로드 받습니다.")
        for numOfItem in self.downloadList:
            crawlBasicInformation(self.menuList[numOfItem], self.startDay, self.endDay)
        print("URL 자료를 잘 저장시켰습니다. 앞으로 PDF를 다운로드 시키겠습니다")
        downloadPdfFile(self.directoryPath)



    '''
        단순히 URL만 크롤링하는 것입니다
    '''
    def startOnlyUrlCrawling(self):
        print("FSC 금융위원회를 Crawling 만 합니다. PDF는 다운로드 하지 않습니다.")
        for numOfItem in self.downloadList:
            crawlBasicInformation(self.menuList[numOfItem], self.startDay, self.endDay)




    '''
        PDF만을 크롤링하는 것입니다
    '''
    def startOnlyPdfCrawling(self):
        print("FSC 금융위원회 PDF만 다운로드 합니다. Crawling은 하지 않습니다")
        downloadPdfFile(self.directoryPath)


