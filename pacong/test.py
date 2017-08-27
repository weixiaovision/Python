import requests
from bs4 import BeautifulSoup


r = requests.get('https://tieba.baidu.com/f?ie=utf-8&kw=%E5%BC%B9%E5%BC%B9%E5%A0%82%E6%89%8B%E6%B8%B8')
soup = BeautifulSoup(r.text, "lxml")
text = soup.select('span[title="回复"]')
for item in text:
    print(item)
    print(item.string)
    print('========')
