from MyMorpheme import Morpheme
from MySentiment import Sentiment
from MyAnalyzer import Analyzer
import numpy

def main():
    read_file = 'ratings_test.txt'
    json_file = 'train_docs.json'
    model_name = 'tmp_model.h5'

    morpheme = Morpheme()
    train_data = morpheme.read_data(read_file)
    morpheme.write_data(json_file, train_data)

    model = Sentiment(json_file)
    model.make_model(model_name)

    analyzer = Analyzer(json_file, model_name)
    analyzer.predict_pos_neg("올해 최고의 영화! 세 번 넘게 봐도 질리지가 않네요.")
    analyzer.predict_pos_neg("배경 음악이 영화의 분위기랑 너무 안 맞았습니다. 몰입에 방해가 됩니다.")
    analyzer.predict_pos_neg("주연 배우가 신인인데 연기를 진짜 잘 하네요. 몰입감 ㅎㄷㄷ")
    analyzer.predict_pos_neg("믿고 보는 감독이지만 이번에는 아니네요")
    analyzer.predict_pos_neg("주연배우 때문에 봤어요")

if __name__ == "__main__":
    main()

    #file_name = 'Naver_0408_0414.csv'
    '''file_name = 'sample_twitter_data_2019-04-21_to_2019-04-21.csv'
    #file_name = 'test.csv'
    with open(file_name, encoding='UTF8') as file:
        csv_data = []
        i = 0
        for line in file.readlines():
            line = line.split(",")
            csv_data.append(line[3])
            #print(csv_data[i][3])
            i += 1

    for index, value in enumerate(csv_data):
        #print(value)
        analyzer.predict_pos_neg(analyzer, value)'''


