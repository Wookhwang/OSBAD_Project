from MyMorpheme import Morpheme
from MySentiment import Sentiment
from MyAnalyzer import Analyzer
from time import sleep
import numpy


class Sentiment_test:
    def __init__(self):
        # 생성 테스트 파일
        self.read_file = 'test_crawling_data.txt'
        self.create_json_file = 'create_test_json.json'
        self.create_model_name = 'create_test_model.h5'

        # 실제 분석 테스트 파일
        self.test_json_file = 'analyze_test_json.json'
        self.test_model_name = 'analyze_test_model.h5'
        self.analyze_data_file = 'analyze_test_data.txt'
        self.analyze_result_file_txt = 'analyze_result.txt'
        self.analyze_result_file_csv = 'analyze_result.csv'

        # 경로
        self.directory_input = 'Data/Test/Input/'
        self.directory_output = 'Data/Test/Output/'

    def make_json_file(self):
        print("********************형태소 분석********************")
        morpheme = Morpheme()
        train_data = morpheme.read_data(self.set_directory_input(self.read_file))
        morpheme.write_data(self.set_directory_output(self.create_json_file), train_data)
        print('********************' +self.create_json_file +' 파일 생성********************')
        print()

    def make_model_file(self):
        print("********************모델 파일 생성********************")
        sleep(0.3)
        model = Sentiment(self.set_directory_output(self.create_json_file))
        model.make_model(self.set_directory_output(self.create_model_name))
        print('********************' +self.create_model_name +' 파일 생성********************')
        print()

    def analyze(self):
        print('********************'+ self.analyze_data_file +" 파일 분석 작업********************")
        print()
        analyzer = Analyzer(self.set_directory_input(self.test_json_file), self.set_directory_input(self.test_model_name))

        f = open(self.set_directory_output(self.analyze_result_file_txt), 'w', encoding='UTF-8')
        with open(self.set_directory_input(self.analyze_data_file), encoding='UTF-8') as file:
            for line in file.readlines():
                print(line)
                result = analyzer.predict_pos_neg(line)
                f.write(line.strip() + "\t" + result + "\n")
        f.close()

    def to_CSV(self):
        r = open(self.set_directory_output(self.analyze_result_file_txt), mode='r', encoding='utf-8')
        f = open(self.set_directory_output(self.analyze_result_file_csv), "w", encoding='utf-8')
        f.write("Text,Tag\n")
        while True:
            line = r.readline()
            if not line: break
            text = line.split('\t')[0].strip()
            tag = line.split('\t')[1].strip()
            f.write(text + "," + tag + '\n')
        print("'********************'분석 종료 : " +self.analyze_result_file_csv +" 결과 파일 생성********************")

    def set_directory_input(self, route):
        return self.directory_input + route

    def set_directory_output(self, route):
        return self.directory_output + route

    def to_do_test(self):
        # 생성 테스트
        self.make_json_file()
        self.make_model_file()
        sleep(0.5)

        # 분석 테스트
        self.analyze()
        sleep(0.5)

        # to CSV
        self.to_CSV()
        sleep(0.5)

