

import codecs
import requests
import time
import uuid

INFINITE_NUM = 987654321

def crawlBasicInformation(url, startDay, endDay):

    currentUrl = url + "&strt_dt=" + str(startDay) + "&end_dt=" + str(endDay)
    countOfCrawlingItem = 0
    saveUrlList = []

    file = codecs.open('fsc_list.json', 'a', encoding='utf-8')

    for page in range(1, INFINITE_NUM):
        # 현재 페이지를 갈 수 있게 합니다
        currentUrl = url + "&page=" + str(page)

        response = requests.get(currentUrl)
        time.sleep(10)

        for info in range(1, 16):
            # 파일 네임 무조건 할것 !!!!

            print
            "path"
            print
            response.xpath('tr[' + str(info) + ']/' + 'td[1]/text()').extract()

            item = {}
            item['title'] = response.xpath('tr[' + str(info) + ']/' + 'td[2]/a/text()').extract()[0]
            item['publish_place'] = response.xpath('tr[' + str(info) + ']/' + 'td[3]/text()').extract()[0]
            item['date'] = response.xpath('tr[' + str(info) + ']/' + 'td[4]/text()').extract()[0]
            item['search_on'] = search_on
            item['link_directory'] = link_directory
            item['tag'] = "경제금융"
            item['content'] = ""
            item['count_query'] = 0
            item['link'] = url
            item['company_name'] = ""
            item['report_name'] = ""
            item['target_site_name'] = "fsc"

        for sel in response.xpath('tr[' + str(info) + ']/' + 'td[6]/a'):
            isPdf = "PDF 문서" == sel.xpath('img/@alt').extract()[0]
            if isPdf:
                item['pdf_download_link'] = 'http://www.fsc.go.kr' + str(sel.xpath('@href').extract()[0])
                item['file_name'] = ''.join(str(uuid.uuid1()).split('-'))
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                file.write(line)

        if int(response.xpath('tr[' + str(info) + ']/' + 'td[1]/text()').extract()[0]) == 1:
            file.close()
            return