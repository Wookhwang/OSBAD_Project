import konlpy
from konlpy.tag import Okt
import csv

#print('morp : sample_twitter_data_{}_to_{}.csv'.format(my_crawler.days_range[0], my_crawler.days_range[-1]))
#df_tweet = pd.read_csv('sample_twitter_data_{}_to_{}.csv'.format(my_crawler.days_range[0], my_crawler.days_range[-1]))
#df_tweet = pd.read_csv('sample_twitter_data_2019-04-20_to_2019-04-20.csv')

f = open('sample_twitter_data_2019-04-20_to_2019-04-20.csv','r',encoding='UTF8')
rdr = csv.reader(f)

x_data = [[0]*60 ]*60

for i, document in enumerate(rdr):
    print("index:{}, document:{}".format(i,document[3]))
    okt = Okt()
    for word in okt.pos(document[3]):
        #if word[1] in ['Noun', 'Verb', 'Adjective']:  # 명사, 동사, 형용사
        if word[1] in ['Verb']:  # 명사, 동사, 형용사
            print("동사:{}".format(word[0]))
        if word[1] in ['Noun']:  # 명사, 동사, 형용사
            print("명사:{}".format(word[0]))
        if word[1] in ['Adjective']:  # 명사, 동사, 형용사
            print("형용사:{}".format(word[0]))
f.close