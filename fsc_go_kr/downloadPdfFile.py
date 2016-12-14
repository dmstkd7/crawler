
from module import DBManager
from module import pdf2text
from module import LogManage

import json
import codecs
import copy
import requests
import time

from selenium import webdriver
from requests import get

"""define 부분입니다"""
URL_JSON_FILE_PATH = 'fsc_list.json'
DB_NAME = "Test"
DB_COLLECTION = "fsc"



logManage = LogManage()
dbManager = DBManager.DBManager(DB_NAME)
pdfToText = pdf2text.Pdf2Text()
driver = webdriver.PhantomJS(executable_path='/usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')


'''
    crawlBasicInformation에서 긁어온 url을 가지고
   크롤링 하며 PDF를 다운로드 하는 함수입니다
'''
def downloadPdfFile(directoryPath):
    try:

        numOfDownloadedFile = 0
        with codecs.open(URL_JSON_FILE_PATH, 'rU', 'utf-8') as f:
            for line in f:
                numOfDownloadedFile = numOfDownloadedFile + 1

                inputDataToDatabase = json.loads(line)

                # pdf를 다운로드 받고 내용을 추출하여 text를 content에 넣으려고 하는 것
                # 오류가 나면 log파일에 어떤 compnay가 빠졌는지 기록하고 그 다음으로 넘어간다
                fileName = inputDataToDatabase['file_name']
                print (str(inputDataToDatabase["company_name"]) + "가 다운로드 중입니다")
                logManage.writeInfo( str(inputDataToDatabase["company_name"]) + "가 다운로드 되고 있습니다")
                url = inputDataToDatabase["pdf_download_link"]

                #PDF를 다운로드 합니다
                savePdfToFileSystem(url, fileName, directoryPath)

                #text를 바꿔서 content를 입력합니다
                toInputContent = pdfToText.pdf2text(fileName, directoryPath)
                inputDataToDatabase['page_number'] = len(toInputContent)

                num = 1;
                for page in toInputContent:
                    temp = {}
                    temp = copy.deepcopy(inputDataToDatabase)
                    temp['fake_id'] = str(temp['file_name']) + "-" + str(num)
                    temp['content'] = page
                    num = num + 1
                    dbManager.Insert(DB_COLLECTION, temp)
    except:
        print (str(inputDataToDatabase['company_name']) + "가 고장났습니다. 다시 한번 봐주시길 바랍니다")
        logManage.writeError(str(inputDataToDatabase['company_name']) + "가 고장났습니다. 다시 한 번 봐주세요")
        if f is not None:
            f.close()
        numOfDownloadedFile = numOfDownloadedFile + 1



"""
    pdf를 다운로드 받아서 FileSystem에 저장시키는 함수입니다
"""
def savePdfToFileSystem(pdfDownloadUrl, fileName, directoryPath):
    try:
        pdfSavePath = str(directoryPath) + str(fileName)

        driver.get(str(pdfDownloadUrl))

        session = requests.Session()
        cookies = driver.get_cookies()

        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        response = session.get(pdfDownloadUrl)

        time.sleep(5)

        with open(pdfSavePath, "wb") as file:
            # write to file
            file.write(response.content)

        logManage.writeInfo(str(pdfDownloadUrl) + "pdf를 정상적으로 받았습니다")
    except:
        logManage.writeError(str(pdfDownloadUrl) + "pdf에서 오류가 났습니다")
        return


