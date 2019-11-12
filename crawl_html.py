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


def get_html(url: str) -> str:
    try:
        r = requests.get(url)
        r.encoding = 'UTF-8'
        return r.text
    except Exception as e:
        return ''


def collect_urls(previous_url: str, current_href: str):
    current_url = ''
    if current_href.startswith('../'):
        current_url = HOMEPAGE + current_href.replace('../', '')
    else:
        url_parts = previous_url.split('/')
        url_parts[-1] = current_href
        current_url = '/'.join(url_parts)

    with open('urls.txt', 'a', encoding='utf-8') as f:
        f.write(current_url+'\n')

    html = get_html(current_url)
    soup = BeautifulSoup(html, 'html.parser')
    next_link = soup.find('a', {'id': 'next-link'})

    if next_link is not None:
        next_href = next_link['href']
        collect_urls(current_url, next_href)
    else:
        return



def generate_pdf():
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
    # collect_urls('https://pymotw.com/3/index.html', 'index.html')
    generate_pdf()


main()