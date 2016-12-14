

from selenium import webdriver
import codecs
import uuid
import json
import datetime

from module import LogManage

logManage = LogManage()
INFINITE_NUM = 987654321

driver = webdriver.PhantomJS(executable_path="/usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")


def crawlBasicInformation(url, startDay, endDay, directoryPath):

    try:
        file = codecs.open('fsc_list.json', 'a', encoding='utf-8')

        urlIncludeDay = url + "&strt_dt=" + str(startDay) + "&end_dt=" + str(endDay)

        for page in range(1, INFINITE_NUM):
            currentUrl = urlIncludeDay + "&page=" + str(page)
            driver.get(currentUrl)

            #단순히 제목을 가져오는 부분이지만 제목이 몇 개 인지 파악하여 page당 몇 개의 리스트를 크롤링 해야 하는지
            #알려주는 지표가 된다.
            numOftitles = len(driver.find_elements_by_class_name("description"))

            if (numOftitles == 0):
                logManage.writeInfo(str(currentUrl)) + "부분이 끝났습니다 다음으로 이동하겠습니다"
                print (str(currentUrl) + "부분이 끝이 났습니다 다음으로 이동하겠습니다")
                return

            num = 0
            for i in range(1, numOftitles):

                currentElementTitle = driver.find_element_by_xpath(
                    "//*[@id='contents']/div[2]/table/tbody/tr[" + str(i) + "]/td[2]")
                currentElementDate = driver.find_element_by_xpath(
                    "//*[@id='contents']/div[2]/table/tbody/tr[" + str(i) + "]/td[4]")
                currentElementAttach = driver.find_elements_by_xpath(
                    "//*[@id='contents']/div[2]/table/tbody/tr[" + str(i) + "]/td[6]/a")
                currentElementAttachCheck = driver.find_elements_by_xpath(
                    "//*[@id='contents']/div[2]/table/tbody/tr[" + str(i) + "]/td[6]/a/img")
                item = {}
                item['title'] = currentElementTitle.text
                item['publish_place'] = "금융위원회"
                item['document_type'] = "pdf"
                item['search_on'] = "1"
                item['file_name'] = ''.join(str(uuid.uuid1()).split('-'))
                item['count_query'] = 0
                item['report_name'] = currentElementTitle.text
                item['content'] = ''
                item['tag'] = ["금융정책"]
                item['link'] = currentUrl
                item['company_name'] = ""
                item['pdf_download_link'] = ''
                item['target_site_name'] = "fsc"
                item['link_directory'] = directoryPath
                item['page_number'] = ''
                item['date'] = currentElementDate.text

                time_temp = item['date'].split('-')
                time = datetime.datetime(int(time_temp[0]), int(time_temp[1]), int(time_temp[2]))
                item['date'] = time


                #첨부파일이 몇 개 인지 표시하기 위한 변수
                numOfAttach = 0

                # pdf파일을 여기서 새로 받아야 합니다
                for it in currentElementAttach:
                    isPdf = u'PDF 문서' == currentElementAttachCheck[numOfAttach].get_attribute("alt")

                    numOfAttach = numOfAttach + 1
                    if (isPdf == True):
                        # item['pdf_download_link'].append(it.get_attribute("href"))
                        item['pdf_download_link'] = it.get_attribute("href")
                        item['file_name'] = ''.join(str(uuid.uuid1()).split('-'))
                        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                        file.write(line)

        file.close()

    except:
        logManage.writeError(" fsc, crawlBasicInformation.py,  error")
        return