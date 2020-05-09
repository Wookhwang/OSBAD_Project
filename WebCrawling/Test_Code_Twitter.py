import GetOldTweets3 as got
from bs4 import BeautifulSoup
import datetime
import time
from random import uniform
from tqdm.notebook import tqdm
import pandas as pd
import matplotlib.pyplot as plt

days_range = []

start = datetime.datetime.strptime("2019-04-21", "%Y-%m-%d")
end = datetime.datetime.strptime("2019-04-22", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    days_range.append(date.strftime("%Y-%m-%d"))

print("=== 설정된 트윗 수집 기간은 {} 에서 {} 까지 입니다 ===".format(days_range[0], days_range[-1]))
print("=== 총 {}일 간의 데이터 수집 ===".format(len(days_range)))

# 수집 기간 맞추기
start_date = days_range[0]
end_date = (datetime.datetime.strptime(days_range[-1], "%Y-%m-%d")
            + datetime.timedelta(days=1)).strftime("%Y-%m-%d") # setUntil이 끝을 포함하지 않으므로, day + 1

# 트윗 수집 기준 정의
tweetCriteria = got.manager.TweetCriteria().setQuerySearch('더불어민주당')\
                                           .setSince(start_date)\
                                           .setUntil(end_date)\
                                           .setMaxTweets(-1)

# 수집 with GetOldTweet3
print("Collecting data start.. from {} to {}".format(days_range[0], days_range[-1]))
start_time = time.time()

tweet = got.manager.TweetManager.getTweets(tweetCriteria)

print("Collecting data end.. {0:0.2f} Minutes".format((time.time() - start_time)/60))
print("=== Total num of tweets is {} ===".format(len(tweet)))

# initialize
tweet_list = []

for index in tqdm(tweet):
    # 메타데이터 목록
    username = index.username
    link = index.permalink
    content = index.text
    tweet_date = index.date.strftime("%Y-%m-%d")
    tweet_time = index.date.strftime("%H:%M:%S")
    retweets = index.retweets
    favorites = index.favorites

    # 결과 합치기
    info_list = [tweet_date, tweet_time, username, content, link, retweets, favorites]
    tweet_list.append(info_list)

    # 휴식
    time.sleep(uniform(1, 2))

twitter_df = pd.DataFrame(tweet_list,
                          columns = ["date", "time", "user_name", "text", "link", "retweet_counts", "favorite_counts"])

# csv 파일 만들기
twitter_df.to_csv("sample_twitter_data_{}_to_{}.csv".format(days_range[0], days_range[-1]), index=False)
print("=== {} tweets are successfully saved ===".format(len(tweet_list)))

# 파일 확인하기
df_tweet = pd.read_csv('sample_twitter_data_{}_to_{}.csv'.format(days_range[0], days_range[-1]))
print(df_tweet['text'].head(20))

# 키워드 빈도 분석하기
def get_keywords(dataframe):
    keywords = []
    text = dataframe["text"].lower()
    if "더불어민주당" in text:
        keywords.append("더불어민주당")
    if "막말" in text:
        keywords.append("막말")
    return ",".join(keywords)

df_tweet["keyword"] = df_tweet.apply(get_keywords,axis=1)

# barplot 그리기
counts = df_tweet["keyword"].value_counts()
plt.bar(range(len(counts)), counts)
plt.title("Tweets mentioning keywords")
plt.ylabel("# of tweets")
plt.show()
print(counts)


