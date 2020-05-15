import pandas as pd
import numpy as np
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm

'''
if __name__ == '__main__':
    # 각 형태소별로 분류(Tagging)해주는 Okt 객체를 불러온다.
    tagger = Okt()

    # nouns 함수를 통해 명사에 해당하는 부분만 리스트 형태로 반환한다.
    noun_list = tagger.nouns('KoNLPy에 오신 것을 환영합니다.')

    print(noun_list)

'''
# DTM을 편리하게 만들어주기 위해 Scikit-Learn에서 제공하는 CountVectorizer를 import 한다.


if __name__ == '__main__':
    # 타이틀 리스트를 불러와서 title_list 변수에 저장한다.
    t_file_name = open('Title_List.txt', 'r', encoding='utf-8')

    title_list = []
    for line in t_file_name.readlines():
        # txt파일을 readlines로 불러오면 개행 문자도 함께 읽어오기 때문에 인덱싱으로 처리해준다.
        title_list.append(line[:-1])

    t_file_name.close()

    s_file_name = open('Stop_Words.txt', 'r', encoding='utf-8')

    stop_words_list = []
    for line in s_file_name.readlines():
        # 위에서는 인덱싱으로 처리했지만 rstrip 함수를 사용하여 공백을 제거할 수도 있다.
        stop_words_list.append(line.rstrip())

    s_file_name.close()
   # print(stop_words_list)

    # pandas의 read_csv 함수를 이용하여 csv 파일을 불러온다.
    dataset = pd.read_csv('Naver_0408_0414_DM_UTF8_2.csv', encoding='utf-8')


    # 각 형태소별로 분류(Tagging)해주는 Okt 객체를 불러온다.
    tagger = Okt()

    for title in tqdm(title_list, desc='타이틀 리스트 진행도'):  # title_list에 대해 반복문을 실행
        # 각 타이틀에 대한 6770개 문서의 DTM을 표현하기 위해
        # CountVectorizer 객체를 선언
        cv = CountVectorizer()

        # 각 문서들의 말뭉치(corpus)를 저장할 리스트 선언
        corpus = []

        # 각 타이틀에 대한 문서들의 말 뭉치를 저장한다. (데이터가 많으면 이 부분에서 장시간이 소요될 수 있다.)
        for doc_num in tqdm(range(1000), desc='문서 진행도'):
            # 각 말뭉치에서 명사 리스트를 만든다.
            noun_list = tagger.nouns(dataset[title].loc[doc_num])

            # 이를 문자열로 저장해야하기 때문에 join함수로 공백으로 구분해 corpus에 append한다.
            corpus.append(' '.join(noun_list))

        # CountVectorizer의 fit_transform 함수를 통해 DTM을 한번에 생성할 수 있다.
        DTM_Array = cv.fit_transform(corpus).toarray()

        # feature_names 함수를 사용하면 DTM의 각 열(column)이 어떤 단어에 해당하는지 알 수 있다.
        feature_names = cv.get_feature_names()

        # 추출해낸 데이터를 DataFrame 형식으로 변환한다.
        DTM_DataFrmae = pd.DataFrame(DTM_Array, columns=feature_names)

        # 열 제거는 drop 함수를 사용하며 axis 속성을 columns로 준 후 inplace를 True로 한다.
        DTM_DataFrmae.drop(stop_words_list, axis='columns', inplace=True)

        # 최종적으로 DTM을 csv 파일로 저장한다.
        DTM_DataFrmae.to_csv('DTM_3.csv', encoding='utf-8-sig')

