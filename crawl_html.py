import requests
from bs4 import BeautifulSoup
import pdfkit
import os


HOMEPAGE = 'https://pymotw.com/3/'

OPTIONS = {
    'page-size': 'Letter',
    'margin-top': '0.05in',
    'margin-right': '0.00in',
    'margin-bottom': '0.05in',
    'margin-left': '0.00in',
    'encoding': "UTF-8",
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
    'no-outline': None
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
}


def get_html(url: str) -> str:
    '''爬取网页内容'''

    try:
        r = requests.get(url, headers=HEADERS)
        r.encoding = 'UTF-8'
        return r.text
    except Exception as e:
        return ''


def collect_urls(current_url: str):
    '''收集链接, 将链接写入到txt文件中'''

    # 现将当前的URL写入到txt文件中
    with open('urls.txt', 'a', encoding='utf-8') as f:
        f.write(current_url + '\n')

    # 解析当前页面的HTML内容, 寻找指向下一页面的a标签
    html = get_html(current_url)
    soup = BeautifulSoup(html, 'html.parser')
    next_link = soup.find('a', {'id': 'next-link'})

    if next_link is not None:
        # 找到指向下一页的a标签, 根据该标签的href值构造下一页面的URL
        next_href : str = next_link['href']
        next_url = ''
        if next_href.startswith('../'):
            next_url = HOMEPAGE + next_href.replace('../', '')
        else:
            url_parts = current_url.split('/')
            url_parts[-1] = next_href
            next_url = '/'.join(url_parts)

        # 递归调用自身, 像处理当前的URL那样处理下一个URL
        collect_urls(next_url)
    else:
        # 找不到指向下一页的a标签, 表名当前页面是最后一页, 爬取完成
        print('Completed crawling.')
        return


def generate_pdf():
    '''根据爬取得来的链接, 生成PDF文件'''

    with open('urls.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()
        for index, url in enumerate(urls):
            try:
                order = str(index+1).zfill(3) + '-'
                file_name = url.strip().replace(HOMEPAGE, '').replace('/', '-').replace('.html', '') + '.pdf'
                file_path = os.path.join('pdfs', order + file_name)
                pdfkit.from_url(url, file_path, options=OPTIONS)
                print('Finished converting HTML ({0}) to PDF ({1})'.format(url, file_path))
            except:
                break

    
def main():
    collect_urls('https://pymotw.com/3/index.html')
    generate_pdf()


if __name__ == '__main__':
    main()