


from module import DBManager
from module import pdf2text
from module import LogManager


"""define 부분입니다"""
URL_JSON_FILE_PATH = 'sec_list.json'
DB_NAME = "Test"
DB_COLLECTION = "sec"

logManage = LogManage()
dbManager = DBManager.DBManager(DB_NAME)
pdfToText = pdf2text.Pdf2Text()

# pdf다운로드 하는 함수
def download(self, url, file_name):
    # open in binary mode

    pdfkit.from_url(url, file_name)
    tt.sleep(1)
    with open(file_name, "wb") as file:
        # get request
        responfse = get(url)
        # write to file
        file.write(response.content)


def downloadHtml(self, url, file_name, file_path):
    print
    "html 다운로드 중입니다"
    u = urllib2.urlopen(url)
    html_file_name = file_path + file_name + ".html"
    f = open(html_file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        # status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        # status = status + chr(8)*(len(status)+1)
        # print status,
    print
    "html comeplete"
    f.close()


def downloadPdf(self):
    # json에 몇개의 파일이 있는지 정해주는 변수
    listFilePath = 'current_sec_list.json'
    numOfFileCount = 0
    with codecs.open(listFilePath, 'rU', 'utf-8') as f:
        for line in f:
            numOfFileCount = numOfFileCount + 1
            tt.sleep(1)
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
                path = "/home/data/sec/2016/" + file_name
                print
                url
                # pdfkit을 통해 download를 하는 대신 from_url을 사용한다
                pdfkit.from_url(str(url), str(path))
                toInputContent = pdfToText.pdf2text(file_name, "/home/data/sec/2016/")
                toInputMongodbData['page_number'] = len(toInputContent)

                lineWithoutTab = list()
                for line in toInputContent:
                    lineWithoutTab.append(line.replace('\t', ' '))

                toInputMongodbData['content'] = lineWithoutTab
                toInputMongodbData['target_site_name'] = 'sec'
                file_path = "/home/data/sec/2016/"
                print
                str(url)
                print
                str(file_name)
                print
                str(file_path)
                self.downloadHtml(str(url), str(file_name), str(file_path))
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
                now = datetime.datetime.now()
                nowdate = now.strftime("%Y-%m-%d")
                pdf_url = url;
                dbManager.Insert('crawl_except', {"date": nowdate, "url": pdf_url})
                sys.exit()

                # 첫번째 변수는 어떤 id로 넣을건지, 두번째는 어떤 데이터가 들어갈지 정해주는 것
            dbManager.Insert('sec', toInputMongodbData)
            # dbManager.mysqlInsert(toInputMongodbData)



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

        logManager.writeInfo(str(pdfDownloadUrl) + "pdf를 정상적으로 받았습니다")
    except:
        logManager.writeError(str(pdfDownloadUrl) + "pdf에서 오류가 났습니다")
        return