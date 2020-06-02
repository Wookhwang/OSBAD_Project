from MyMorpheme import Morpheme
from MySentiment import Sentiment
from MyAnalyzer import Analyzer
import numpy
import pandas as pd
'''
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
'''
'''
if __name__ == "__main__":
    #main()

    #file_name = 'Naver_0408_0414.csv'

    file_name = 'C:\\Users\\hyeon\\study\\오픈소스\\crawling_result\\train\\미래통합당\\0\\미래통합당 최악 패배 부른 3가지 장면  YTN.csv'
    #file_name = 'test.csv'
    
    with open(file_name, encoding='UTF8') as file:
        csv_data = []
        i = 0
        for line in file.readlines():
            line = line.split(",")
            csv_data.append(line[-1])
            #print(csv_data[i][3])
            i += 1

    read_file = 'ratings_test.txt'
    json_file = 'train_docs.json'
    model_name = 'tmp_model.h5'

    analyzer = Analyzer(json_file, model_name)



    for index, value in enumerate(csv_data):


        analyzer.predict_pos_neg(value)





    #data = pd.DataFrame(new_data)

    #data.to_excel('C:\\Users\\hyeon\\study\\오픈소스\\crawling_result\\train\\미래통합당\\테스트.xlsx')
'''
if __name__ == "__main__":
    #main()
    read_file = 'ratings_test.txt'
    #read_file = 'C:\\Users\\hyeon\\study\\오픈소스\\reply_crawling_result\\train\\미래통합당\\tagging_train.txt'
    json_file = 'train_docs.json'
    model_name = 'tmp_model.h5'
    analyzer = Analyzer(json_file, model_name)

    f = open("C:\\Users\\hyeon\\study\\오픈소스\\reply_crawling_result\\train\\미래통합당\\새누리당_tagging_total.txt", 'a', encoding='UTF-8')

    file_name = "C:\\Users\\hyeon\\study\\오픈소스\\reply_crawling_result\\train\\미래통합당\\새누리당_total.csv"
    with open(file_name, encoding='UTF-8') as file:
        for line in file.readlines():
            line = line.split(",")
            result = analyzer.predict_pos_neg(line[2])

            print(line[0].rstrip('\n')+"\t" +line[2].rstrip('\n')+"\t" +result)

            f.write(line[0].rstrip('\n')+"\t" +line[2].rstrip('\n')+"\t" +result+"\n")
    f.close()