

'''
    author : eunsang jang
    date : 2016/12/08
    e-mail : eeunsang7@naver.com

    python 과 mongodb를 연결하는 크롤링입니다

'''

import pymongo
import json



class DBManager:
    def __init__(self, database):
        self.connection = pymongo.MongoClient("223.194.70.86", 27017)
        self.db = self.connection[database]  # test db create

    #이 부분은 장현수분이 만드셨습니다 참고하시기 바랍니다
    #현수씨와 상담해주세요
    def Search(self, collectionName, pdfUrl):  # collection, dic
        collection = self.db[collectionName]
        t = collection.find({"pdf_download_link": pdfUrl})
        if t.count() == 0:
            return True
        else:
            return False

    def Insert(self, collectionName, Data):
        collection = self.db[collectionName]  # collectionName으로  collection 지정
        val = collection.insert(Data)


    '''
    update를 하는 부분입니다 아직 구현이 덜 되어 있어서
    나중에 꼭 완성 시키겠습니다
    def Update(self, collectionName, oldData):
    collection = self.db[collectionName]  # collectionName으로  collection 지정
    val = collection.insert(Data)

    '''
