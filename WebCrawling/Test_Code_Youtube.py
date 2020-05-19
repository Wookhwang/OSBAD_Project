from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

# chromedriver의 위치를 지정한다.
path = 'C:\\Users\\hyeon\\chromedriver'
# driver란 변수에 객체를 만들어 준다.
driver = webdriver.Chrome(path)
# 원하는 사이트의 url을 입력하여 사이트를 연다.
driver.get('https://www.youtube.com/results?search_query=%EB%AF%B8%EB%9E%98%ED%86%B5%ED%95%A9%EB%8B%B9+%EB%A7%89%EB%A7%90&sp=CAM%253D')
# 한번 스크롤 하고 멈출 시간 설정
SCROLL_PAUSE_TIME = 0.5
# body태그를 선택하여 body에 넣음
body = driver.find_element_by_tag_name('body')

while True:
    last_height = driver.execute_script('return document.documentElement.scrollHeight')
    # 현재 화면의 길이를 리턴 받아 last_height에 넣음
    for i in range(10):
        body.send_keys(Keys.END)
        # body 본문에 END키를 입력(스크롤내림)
        time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script('return document.documentElement.scrollHeight')
    if (new_height == last_height):
        break

page = driver.page_source
soup = BeautifulSoup(page, 'lxml')

all_videos = soup.find_all(id='dismissable')

title_list = []
for video in all_videos:
    title = video.find(id='video-title')
    if len(title.text.strip())>0:
        title_list.append(title.text)
    # 공백을 제거하고 글자수가 0보다 크면 append    


# 조회수
'''
view_num_list = []
view_num_regexp = re.compile('조회수')
for video in all_videos:
    view_num = video.find('span',{'class':'style-scope ytd-video-meta-block'})
    if view_num_regexp.search(view_num.text):
        # view_num.text 에 '조회수' 문자열이 있으면 True
        view_num_list.append(view_num.text)


def nview(text):
    view = text.replace('조회수','')
    num = float(view[:-2])
    danwee = view[-2:]
    if danwee == '만회':
        return int(num*10000)
    else:
        int(num*1000)
        
        
view_number_type_list = []
for view in view_num_list:
    view_number_type_list.append(nview(view))

'''


for i in range(len(title_list)):
    print(title_list[i])

print(len(title_list))


data = pd.DataFrame(title_list) 
  
data.to_excel('.\\crawling_result\\미래통합당_막말.xlsx')



# webdriver를 종료한다.
driver.close()
