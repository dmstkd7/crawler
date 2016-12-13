
from module import DBManager
from module import pdf2text

import json
import codecs
import datetime

"""define 부분입니다"""
URL_JSON_FILE_PATH = 'fsc_list.json'


dbManager = DBManager.DBManager('pdf_info')
pdfToText = pdf2text.Pdf2Text()


'''
    crawlBasicInformation에서 긁어온 url을 가지고
   크롤링 하며 PDF를 다운로드 하는 함수입니다
'''

def downloadPdfFile(directoryPath):


    numOfDownloadedFile = 0

    with codecs.open(directoryPath, 'rU', 'utf-8') as f:
        for line in f:
            item = {}

            numOfFileCount = numOfFileCount + 1
            # Json의 date파일이 년도별, 시간별로 나눠져 있지 않기 때문에 세 부분으로 쪼개고 다시  date로 넣어주는 작업
            toInputMongodbData = json.loads(line)

            time_temp = toInputMongodbData['date'].split('-')
            time = datetime.datetime(int(time_temp[0]), int(time_temp[1]), int(time_temp[2]))
            toInputMongodbData['date'] = time

            try:
                # pdf를 다운로드 받고 내용을 추출하여 text를 content에 넣으려고 하는 것
                # 오류가 나면 log파일에 어떤 compnay가 빠졌는지 기록하고 그 다음으로 넘어간다
                file_name = toInputMongodbData['file_name']
                print
                toInputMongodbData["company_name"],;
                print
                "가 다운로드 중입니다"
                url = toInputMongodbData["pdf_download_link"]
                print
                url
                path = str(link_directory) + str(file_name)
                print
                "11"
                self.download(url, path)
                print
                "22"
                toInputContent = pdfToText.pdf2text(file_name, link_directory)
                toInputMongodbData['page_number'] = len(toInputContent)
                toInputMongodbData['target_site_name'] = 'fsc'
                toInputMongodbData['link_directory'] = link_directory
                # toInputMongodbData['content'] = toInputContent
                num = 1;
                for page in toInputContent:
                    print
                    page
                    temp = {}
                    temp = copy.deepcopy(toInputMongodbData)
                    temp['fake_id'] = str(temp['file_name']) + "-" + str(num)
                    temp['content'] = page
                    num = num + 1
                    dbManager.Insert('test', temp)
            except:
                # nohup으로 돌릴때는 company_name을 끄도록해
                # print(toInputMongodbData["company_name"])
                print
                toInputMongodbData['company_name'],;
                print
                "가 고장 났습니다 다시 한 번 봐주시길 바랍니다"
                if f is not None:
                    f.close()
                numOfFileCount = numOfFileCount + 1
                sys.exit()

                # 첫번째 변수는 어떤 id로 넣을건지, 두번째는 어떤 데이터가 들어갈지 정해주는 것
                # dbManager.Insert('fsc', toInputMongodbData)