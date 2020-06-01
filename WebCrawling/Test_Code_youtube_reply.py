
from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import re


def get_urls_from_youtube_with_keyword(keyword):
    titles = []
    urls = []

    search_keyword_encode = requests.utils.quote(keyword)

    url = "https://www.youtube.com/results?search_query=" + search_keyword_encode + "&sp=CAM%253D"

    driver = wd.Chrome(executable_path="C:\\Users\\hyeon\\chromedriver.exe")

    driver.get(url)

    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        time.sleep(3.0)

        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_page_height == last_page_height:
            break

        last_page_height = new_page_height

    html_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html_source, 'lxml')

    datas = soup.select("a#video-title")

    for data in datas:
        title = data.text.replace('\n', '')
        url = "https://www.youtube.com/" + data.get('href')

        titles.append(title)
        urls.append(url)

    return titles, urls


def crawl_youtube_page_html_sources(urls):
    html_sources = []

    for i in range(0, 5):
        driver = wd.Chrome(executable_path="C:\\Users\\hyeon\\chromedriver.exe")
        driver.get(urls[i])

        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2.0)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

            if new_page_height == last_page_height:
                break
            last_page_height = new_page_height

        html_source = driver.page_source
        html_sources.append(html_source)
        print("OK")

        driver.quit()
    return html_sources


def get_user_IDs_and_comments(html_sources):
    my_dataframes = []
    for html in html_sources:

        soup = BeautifulSoup(html, 'lxml')

        youtube_user_IDs = soup.select('div#header-author > a > span')

        youtube_comments = soup.select('yt-formatted-string#content-text')

        str_youtube_userIDs = []
        str_youtube_comments = []

        for i in range(len(youtube_user_IDs)):
            str_tmp = str(youtube_user_IDs[i].text)
            #     print(str_tmp)
            str_tmp = str_tmp.replace('\n', '')
            str_tmp = str_tmp.replace('\t', '')
            str_tmp = str_tmp.replace('                ', '')
            str_youtube_userIDs.append(str_tmp)

            str_tmp = str(youtube_comments[i].text)
            str_tmp = str_tmp.replace('\n', '')
            str_tmp = str_tmp.replace('\t', '')
            str_tmp = str_tmp.replace('               ', '')

            str_youtube_comments.append(str_tmp)

        pd_data = {"ID": str_youtube_userIDs, "Comment": str_youtube_comments}

        youtube_pd = pd.DataFrame(pd_data)

        my_dataframes.append(youtube_pd)

    return my_dataframes


def convert_csv_from_dataframe(titles, my_dataframes):
    for i in range(len(my_dataframes)):
        title = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…《\》]', '', titles[i])
        my_dataframes[i].to_csv("C:\\Users\\hyeon\\study\\오픈소스\\reply_crawling_result\\train\\미래통합당\\{}.csv".format("미래통합당 막말_"+title))


titles, url = get_urls_from_youtube_with_keyword("미래통합당 막말")

html_sorces = crawl_youtube_page_html_sources(url)

my_dataframes = get_user_IDs_and_comments(html_sorces)

convert_csv_from_dataframe(titles, my_dataframes)



