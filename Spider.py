import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)<.*?title="(.*?)".*?-src="(.*?)".*?star">(.*?)<.*?releasetime">(.*?)</p>.*?"integer">(.*?)</.*?fraction">(.*?)</i>', re.S)
    items = pattern.findall(html)
    for item in items:
        yield {
            'index': item[0],
            'title': item[1],
            'img': item[2],
            'star': item[3].strip()[3:],
            'time': item[4][5:],
            'score': item[5] + item[6]
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])