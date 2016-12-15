

from module import DBManager
from module import pdf2text
import time
import datetime
import codecs
import json
from requests import get
import sys
import copy

dbManager = DBManager.DBManager('pdf_info')
pdfToText = pdf2text.Pdf2Text()


"""define 부분입니다"""
URL_JSON_FILE_PATH = 'dart_list.json'
DB_NAME = "Test"
DB_COLLECTION = "dart"


'''
    crawlBasicInformation에서 긁어온 url을 가지고
    나머지 세부 정보를 크롤링 하며 PDF를 다운로드 하는 함수입니다
'''
def downloadPdfFile(directoryPath):

    numOfDownloadedFile = 0
    with codecs.open(URL_JSON_FILE_PATH, 'rU', 'utf-8') as f:
        for line in f:
            time.sleep(10)
            numOfFileCount = numOfFileCount + 1
            # Json의 date파일이 년도별, 시간별로 나눠져 있지 않기 때문에 세 부분으로 쪼개고 다시  date로 넣어주는 작업

            try:
                inputDataToDatabase = json.loads(line)


                #날짜를 ISO 형식으로 바꾸는 것입니다 crawlBasicInformation에서 처리하지 못해 임시로 여기서 처리합니다
                time_temp = inputDataToDatabase['date'].split('.')
                time = datetime.datetime(int(time_temp[0]), int(time_temp[1]), int(time_temp[2]))
                inputDataToDatabase['date'] = time


                # pdf를 다운로드 받고 내용을 추출하여 text를 content에 넣으려고 하는 것
                # 오류가 나면 log파일에 어떤 compnay가 빠졌는지 기록하고 그 다음으로 넘어간다
                fileName = inputDataToDatabase['file_name']
                print ( str(inputDataToDatabase["company_name"]) + " 크롤링 시작합니다")
                pdfDownloadUrl = inputDataToDatabase["pdf_download_link"]

                #PDF파일을 다운로드 하고 FILE 시스템에 저장시키는 곳
                savePdfToFileSystem(pdfDownloadUrl, fileName, directoryPath)

                #다운로드 받은 PDF에서 text를 뽑아내는 과정
                extractedText = pdfToText.pdf2text(fileName, "/home/data/dart/2016/")

                inputDataToDatabase['page_number'] = len(extractedText)

                #페이지별로 표시를 해두기 위한 과정
                num =1
                for page in extractedText:
                    temp = {}
                    temp = copy.deepcopy(inputDataToDatabase)
                    temp['fake_id'] = str(temp['file_name']) + "-" + str(num)
                    temp['content'] = page
                    num = num +1
                    dbManager.Insert("test", temp)

                #dbManager.Insert('pdf_all_data', inputDataToDatabase)

            except:
                # nohup으로 돌릴때는 company_name을 끄도록해
                # print(toInputMongodbData["company_name"])
                print (str(inputDataToDatabase['company_name']) + "가 고장났습니다. 다시 한번 봐주시길 바랍니다")
                if f is not None:
                    f.close()
                sys.exit()


def savePdfToFileSystem(pdfDownloadUrl, fileName, directoryPath):
    pdfSavePath = str(directoryPath) + str(fileName)
    with open(pdfSavePath, "wb") as file:
        # get request
        response = get(pdfDownloadUrl)
        # write to file
        file.write(response.content)
    return