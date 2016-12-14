'''
    author : eunsang jang
    date : 2016/11/11
    e-mail : eeunsang7@naver.com
    www.sec.gov 홈페이지를 다 크롤링 해오는 프로그램입니다.
    main에서 어떤 것을 크롤링 할 것인지, 날짜를 정해서 크롤링을 합니다.

'''

'''
    특이점 :
        1. sec 홈페이지 같은경우 비동기적으로 마우스가 밑에 갔다는 이벤트가 발생했을 때 자료를 긁어옵니다
        그렇기에 ftp에서 sitemap.quartelyindex1.xml 등과 같은 것을 받아서 미리 sec 폴더에 넣어놔야 합니다
        이점을 꼭 기억하시기 바랍니다.

        2. html-> pdf를 바꾸는 작업은 display를 필요로 하는 작업입니다. 우분투 서버의 경우 디스플레이가 존재하지 않기 때문에
        가상의 디스플레이를 생성해주어야 잘 돌아갑니다. 그렇기에 sec을 크롤링 하고 싶으시다면 xvfb-run python ~~~~ 이런식으로 돌리셔야 합니다
'''


from .crawlBasicInformation import crawlBasicInformation
from .downloadPdfFile import downloadPdfFile


'''
    define 목록
    LINK_DIRECTORY는 DART의 PDF 파일 저장 위치를 의미한다.
'''


class Sec_gov:
    def __init__(self, startDay, endDay):
        #이렇게 하는게 맞나?????
        self.PATH_DIRECTORY = '/home/data/sec/2016/'
        print("sec를 크롤링 하기 시작하였습니다")


    '''
        startDartCrawling의 경우는 URL을 JSON으로 저장시키고 이후 JSON파일을 한 줄씩
        읽어 PDF를 다운로드 시킵니다
    '''

    def startCrawling(self):
        print("공시자료 Dart를 Crawling 합니다. URL을 가져오고 이후 PDF를 다운로드 받습니다.")
        crawlBasicInformation()
        print("URL 자료를 잘 저장시켰습니다. 앞으로 PDF를 다운로드 시키겠습니다")
        downloadPdfFile(self.PATH_DIRECTORY)



    '''
        단순히 URL만 크롤링하는 것입니다
    '''
    def startOnlyUrlCrawling(self):
        crawlBasicInformation()



    '''
        PDF만을 크롤링하는 것입니다
    '''
    def startOnlyPdfCrawling(self):
        downloadPdfFile(self.PATH_DIRECTORY)



