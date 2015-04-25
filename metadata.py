from xml.dom import minidom
from pymongo import MongoClient


def metadata(filename):
    dom = minidom.parse(filename)
    record_id = -1
    for record in dom.getElementsByTagName('record'):
        title = record.getElementsByTagName('lom:title')[0]
        keywords = record.getElementsByTagName('lom:keyword')
        description = record.getElementsByTagName('lom:description')[0]
        record_id += 1
        yield {
            'title': title.firstChild.nodeValue,
            'keywords': [
                keyword.firstChild.nodeValue
                for keyword in keywords],
            'description': description.firstChild.nodeValue,
            # 'raw': record.toxml(),
            'id': record_id,
        }


def main():
    client = MongoClient('localhost', 27017)
    database = client['lsa-froac']
    records = database['records']
    records.delete_many({})
    records.insert_many(list(metadata('data/roapManizales1.xml')))

if __name__ == '__main__':
    main()
