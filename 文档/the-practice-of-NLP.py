import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from jieba import analyse

#定义解析网页文本函数，获取新闻的标题与正文
def get_text(url):
    headers = {'User-Agent':
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'}
    response = requests.get(url = url, headers = headers)
    response.encoding = 'utf-8'
    html_data = response.text
    soup = BeautifulSoup(html_data, 'lxml')
    parse_url(soup)

#定义解析bs对象函数，提取新闻标题与正文，并保存为txt文件
def parse_url(soup):
    title = soup.select('.post-title h1')[0].string
    print(title)
    p_list = soup.select('.post-content p')
    for p in p_list:
        if p.string:
            with open(f'/home/wiki/git-remote-test/news/{title}.txt', 'a', encoding = 'utf-8') as fp:
                fp.write(p.string)

#开始获取新闻标题与正文
headers = {'User-Agent':
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'}
url = 'http://www.centrechina.com/news/jiaodian'
response = requests.get(url = url, headers = headers)
html_data = response.text
soup = BeautifulSoup(html_data, 'lxml')
hotnews_url_list = []
a_list = soup.select('.ajax-load-con h2 a')
for a in a_list:
    hotnews_url_list.append(a['herf'])
for url in hotnews_url_list:
    get_text(url)

#读取每个txt文件中的新闻正文，从中提取关键词
keywords_dict = {'新闻标题':[], '新闻检索关键词':[]}
txt_name = os.listdir('/home/wiki/git-remote-test/news')#获取news文件夹下的所有文件名
for txt_file in txt_name:
    with open('/home/wiki/git-remote-test/news/'+txt_file, 'r+', encoding = 'utf-8') as fp1:
        txt_content = fp1.read()
    keywords = analyse.textrank(txt_content, topK = 10, withWeight = False)
    print(keywords)
    keywords_dict['新闻标题'].append(txt_file)
    keywords_dict['新闻检索关键词'].append(keywords)

#将得到的数据转化为dataframe类型，并存储为csv文件
news_keywords_info = pd.DataFrame(keywords_dict, columns = ['新闻标题', '新闻检索关键词'])
news_keywords_info.to_csv('/home/wiki/git-remote-test/news/newskeywords.csv', index = False, encoding = 'utf-8')