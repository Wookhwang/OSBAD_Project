from MyMorpheme import Morpheme
from MySentiment import Sentiment
from MyAnalyzer import Analyzer
import numpy


def make_json_file(read_file, json_file):
    morpheme = Morpheme()
    train_data = morpheme.read_data(read_file)
    morpheme.write_data(json_file, train_data)


def make_model_file(json_file, model_name):
    model = Sentiment(json_file)
    model.make_model(model_name)


def analyze(json_file, model_name, analyze_data_file, analyze_result_file):
    analyzer = Analyzer(json_file, model_name)

    f = open(analyze_result_file, 'w', encoding='UTF-8')
    with open(analyze_data_file, encoding='UTF-8') as file:
        for line in file.readlines():
            print(line)
            result = analyzer.predict_pos_neg(line)
            f.write(line.strip() + "\t" + result + "\n")
    f.close()

def to_CSV(txt_file_name, csv_file_name):
    r = open(txt_file_name, mode='r', encoding='utf-8')
    f = open(csv_file_name, "w", encoding='utf-8')
    f.write("Text,Tag\n")
    while True:
        line = r.readline()
        if not line: break
        text = line.split('\t')[0].strip()
        tag = line.split('\t')[1].strip()
        f.write(text + "," + tag + '\n')


'''def main():
    read_file = 'ratings_test.txt'
    json_file = 'train_docs.json'
    model_name = 'tmp_model.h5'

    analyzer = Analyzer(json_file, model_name)
    analyzer.predict_pos_neg("올해 최고의 영화! 세 번 넘게 봐도 질리지가 않네요.")
    analyzer.predict_pos_neg("배경 음악이 영화의 분위기랑 너무 안 맞았습니다. 몰입에 방해가 됩니다.")
    analyzer.predict_pos_neg("주연 배우가 신인인데 연기를 진짜 잘 하네요. 몰입감 ㅎㄷㄷ")
    analyzer.predict_pos_neg("믿고 보는 감독이지만 이번에는 아니네요")
    analyzer.predict_pos_neg("주연배우 때문에 봤어요")'''


if __name__ == "__main__":
    #생성 테스트 파일
    read_file = 'Data/Test/Input/test_crawling_data.txt'
    create_json_file = 'Data/Test/Output/create_test_json.json'
    create_model_name = 'Data/Test/Output/create_test_model.h5'

    #실제 분석 테스트 파일
    test_json_file = 'Data/Test/Input/analyze_test_json.json'
    test_model_name = 'Data/Test/Input/analyze_test_model.h5'
    analyze_data_file = 'Data/Test/Input/analyze_test_data.txt'
    analyze_result_file_txt = 'Data/Test/Output/analyze_result.txt'
    analyze_result_file_csv = 'Data/Test/Output/analyze_result.csv'

    #생성 테스트
    make_json_file(read_file, create_json_file)
    make_model_file(create_json_file, create_model_name)

    #분석 테스트
    analyze(test_json_file, test_model_name, analyze_data_file, analyze_result_file_txt)

    #to CSV
    to_CSV(analyze_result_file_txt, analyze_result_file_csv)



