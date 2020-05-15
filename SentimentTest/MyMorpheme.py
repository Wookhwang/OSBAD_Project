from konlpy.tag import Okt
import json

class Morpheme:
    def read_data(self, filename):
        with open(filename, 'r', encoding='UTF8') as f:
            data = [line.split('\t') for line in f.read().splitlines()]
            # txt 파일의 헤더(id document label)는 제외하기
            data = data[1:]
        return data

    def tokenize(doc):
        # norm은 정규화, stem은 근어로 표시하기를 나타냄
        okt = Okt()
        print(doc)
        return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

    def write_data(self, filename, train_data):
        train_docs = [(self.tokenize(row[1]), row[2]) for row in train_data]
        with open(filename, 'w', encoding="utf-8") as make_file:
            json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")






    '''
    train_data = read_data('ratings_test.txt')
    okt = Okt()
    train_docs = [(tokenize(row[1]), row[2]) for row in train_data]
    with open('train_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")
    '''


