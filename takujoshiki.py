import urllib.request
import re
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime, date, timedelta, timezone

JST = timezone(timedelta(hours=+9))


trans_table = str.maketrans(
    {
        "　": " ", 
#        "▼": "。", 
        "０": "0", 
        "１": "1", 
        "２": "2", 
        "３": "3", 
        "４": "4", 
        "５": "5", 
        "６": "6", 
        "７": "7", 
        "８": "8", 
        "９": "9",  
    }
)


class Takujoshiki():
    def __init__(self):
        self.content_text = ''
        self.title = ''
        self.ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
            'AppleWebKit/537.36 (KHTML, like Gecko) '\
            'Chrome/55.0.2883.95 Safari/537.36 '

    def text_getter(self, inner_url):
        r = urllib.request.Request(inner_url, headers={'User-Agent': self.ua})
        html = urllib.request.urlopen(r)
        soup = BeautifulSoup(html, "html.parser")
    
        self.title = soup.find('h1', class_='newsTitle').text
        sentence = soup.find("p").text
        sentence = sentence.translate(trans_table)
        sentence = re.sub(r"（.*?）", "", sentence)
        sentence = re.sub(r"([0-9]{4})・([0-9]{1,2})・([0-9]{1,2})", r"\1-\2-\3", sentence)
        self.content_text = sentence
    
    
    def url_getter(self):
        r = urllib.request.Request(
            url = "https://www.hokkaido-np.co.jp/column/c_column/c_season",
            headers = {'User-Agent': self.ua}
        )

        html = urllib.request.urlopen(r)
        soup = BeautifulSoup(html, "html.parser")
    
        sentence = soup.find("ul", attrs={'class': 'categoryArchiveList'})
        sentence = sentence.find_all("li")
    
        url = ["https://www.hokkaido-np.co.jp" + i.find("a").get('href') for i in sentence][0]
    
        sleep(1)
    
        self.text_getter(url)

    def is_today(self):
        r = re.search(r"([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", self.content_text)
        if datetime.now(JST).date() == date(int(r.group(1)), int(r.group(2)), int(r.group(3))):
            return
        else:
            self.content_text = None
    
    def run(self):
        self.url_getter()
        self.is_today()
        return self.content_text, self.title