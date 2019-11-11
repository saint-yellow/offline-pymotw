import requests
from bs4 import BeautifulSoup
import pdfkit


ENGLISH_HOMEPAGE = 'https://pymotw.com/3/'


def get_html(url: str) -> str:
    try:
        r = requests.get(url)
        r.encoding = 'UTF-8'
        return r.text
    except Exception as e:
        print('Failed while crawling {0}'.format(url))
        print(e)
        return ''


def generate_pdf(html: str, output_path: str):
    pdfkit.from_string(html, output_path)



if __name__ == '__main__':
    html = get_html(ENGLISH_HOMEPAGE+'index.html')
    generate_pdf(html, 'index.pdf')
