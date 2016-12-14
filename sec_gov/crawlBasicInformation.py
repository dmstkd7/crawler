
import codecs
import xml.etree.ElementTree as ET
import json


from .CIKDATA import CIK
from .CIKDATA import CIKTITLE



# 이것이 Company인지 Investment인지 구분해 내는 함수입니다
def isCompanyOrInvestment(self, num):
    if num not in CIK:
        return "Investment"
    return "Company"


# 타입을 정해주는 함수입니다
def tagging(self, type, formType):
    formType = str(formType[0])

    company_annual_reports = ['10-K', '10-k/A', 'NT 10-K', '11-K', '11-KT', 'NT 11-K', '18-K', '18-K/A', '20-F',
                              '20-F/A', 'ARS']
    company_quarterly_reports = ['10-Q', '10-Q/A', 'NT 10-Q', '10-QT']
    company_current_reports = ['8-K', '8-K/A']
    company_other_reports = ['6-K', '10-D', 'ABS-15G']
    company_registrations = ['S-1', 'S-3', 'S-4', 'S-6', 'S-8', 'S-11', 'S-20']
    company_private_offering = ['D', 'D/A']
    company_ownership = ['SC 13D', 'SC 13-D/A', 'SC 13G', 'SC 13G/A']
    company_prospectus = ['POS AM ', '425']
    company_proxy = ['PRE 14A', 'DEF 14A', 'DEFA 14A']

    investment_company_annual_reports = ['MA-I', 'N-CSR', 'NSAR-A', 'NSAR-B', '24F-2', '24F-2 NT']
    investment_company_quarterly_reports = ['N-Q', 'N-Q/A']
    investment_company_current_reports = ['8-K', '8-K/A']
    investment_company_other_reports = ['40-17G', '40-17F2', 'ABS-15G', '6-K', '10-D']
    investment_company_registrations = ['N-1', 'N-2', 'N-3', 'N-4', 'N-5', 'N-6', 'N-8', 'N-14', '497', '497K',
                                        '485*', '487']
    investment_company_private_offering = ['D', 'D/A']
    investment_company_ownership = ['13F', '13F-HR', '13F-NT', 'SC 13D', 'SC 13-D/A', 'SC 13G', 'SC 13G/A']
    investment_company_prospectus = ['425']
    investment_company_proxy = ['PRE 14A', 'DEF 14A', 'DEFA 14A']

    insiders_ownership = ['3', '4', '5'];

    # 먼저 form이 3,4,5 인지 확인하고 맞다면 바로 return한다
    if (formType in insiders_ownership):
        return "insiders_ownership"

    elif type == "company":
        if (type in company_annual_reports):
            return "company_annual_reports"
        elif (type in company_quarterly_reports):
            return "company_quarterly_reports"
        elif (type in company_current_reports):
            return "company_current_reports"
        elif (type in company_other_reports):
            return "company_other_reports"
        elif (type in company_registrations):
            return "company_registrations"
        elif (type in company_private_offering):
            return "company_private_offering"
        elif (type in company_ownership):
            return "company_ownership"
        elif (type in company_prospectus):
            return "company_prospectus"
        elif (type in company_proxy):
            return "company_proxy"

    elif type == "investment":
        if (type in investment_company_annual_reports):
            return "investment_company_annual_reports"
        elif (type in investment_company_quarterly_reports):
            return "investment_company_quarterly_reports"
        elif (type in investment_company_current_reports):
            return "investment_company_current_reports"
        elif (type in investment_company_other_reports):
            return "investment_company_other_reports"
        elif (type in investment_company_registrations):
            return "investment_company_registrations"
        elif (type in investment_company_private_offering):
            return "investment_company_private_offering"
        elif (type in investment_company_ownership):
            return "investment_company_ownership"
        elif (type in investment_company_prospectus):
            return "investment_company_prospectus"
        elif (type in investment_company_proxy):
            return "investment_company_proxy"

    return "error"



def readFile():





def crawlBasicInformation(list):
    file = codecs.open('current_sec_list.json', 'a', encoding='utf-8')
    crawlingList = ["sitemap.quarterlyindex1.xml", "sitemap.quarterlyindex2.xml"]

    # 주소를 다 가져오기
    siteList = []
    siteDate = []
    doc = ET.parse("sitemap.quarterlyindex1.xml")
    # print doc
    root = doc.getroot()
    for url in root.iter("url"):
        siteList.append(url.findtext("loc"))
        siteDate.append(url.findtext("lastmod"))

    # 2차 크롤링
    numOfDocument = 0
    for site in siteList:
        url = site

        response = requests.get(url, stream=False)
        response = HtmlResponse(url=url, body=(response.content))
        response = Selector(response)

        site = "https://www.sec.gov/" + str(
            response.xpath("//*[@id='formDiv']/div/table/tr[2]/td[3]/a/@href").extract()[0])

        # 태깅 부여하기
        # type1 = str(response.xpath("//*[@id='formDiv']/div/table/tr[2]/td[4]/text()").extract()[0])
        # type1 = self.tagging(type1)

        # 회사 이름 부여하기
        company_name = str(response.xpath("//*[@id='filerDiv']/div[3]/span/text()").extract()[0])

        # 만약 마지막 이름에 "(" 이 있다면 없앤다
        if (company_name.endswith('(')):
            company_name = company_name[:-1]

        # CIK를 부여하는 함수입니다

        # formType 꼭 가져올것
        formType = response.xpath("//*[@id='formDiv']/div/table/tr[2]/td[4]/text()").extract()

        print
        formType
        print
        str(formType[0])

        # CIK를 부여하는 함수입니다. 6-K일 경우 홈페이지가 달라지기 때문에 if ~else 처리를 하였습니다.
        differentType = ['6-K', 'FWP', '424B2', '8-K']
        if (str(formType[0]) in differentType):
            tmpNumOfCIK = (response.xpath("//*[@id='filerDiv']/div[3]/span/a/text()").extract()[0])
            print
            tmpNumOfCIK
            print
            "a"
        else:
            tmpNumOfCIK = response.xpath("//*[@id='filerDiv']/div[3]/span/a[2]/text()").extract()[0]
            print
            tmpNumOfCIK
            print
            "b"

        tmpNumOfCIK = re.findall('\d+', str(tmpNumOfCIK))
        print
        tmpNumOfCIK[0]
        print
        " 이게 분류표 입니다 "
        numOfCIK = self.isCompanyOrInvestment(tmpNumOfCIK)
        print
        numOfCIK
        print
        "위에 문서가 numOfCIK입니다"

        item = {}
        item['company_name'] = company_name
        item['title'] = CIKTITLE[str(formType[0])]
        item['publish_place'] = str(company_name)
        item['report_name'] = item['title']
        item['date'] = siteDate[numOfDocument]
        item['link'] = url
        item['pdf_download_link'] = site
        item['link_directory'] = '/home/data/sec/2016/'
        item['file_name'] = ''.join(str(uuid.uuid1()).split('-'))
        item['content'] = ''
        item['search_on'] = '1'
        item['tag'] = ["미국공시"]
        item['count_query'] = 0
        item['document_type'] = 'pdf'
        item['target_site_name'] = 'sec'

        numOfDocument = numOfDocument + 1

        # tag를 부여하는 작업입니다
        if (self.isCompanyOrInvestment(str(numOfCIK)) == "company"):
            item['tag'].append(self.tagging("company", formType))
            print
            item['tag']
        else:
            item['tag'].append(self.tagging("investment", formType))
            print
            self.tagging("investment", formType)
            print
            item['tag']

        # 임시로 여기서 다운로드까지 한다
        # pdfkit.from_url(site, item['file_name'])


        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        file.write(line)

    file.close()
