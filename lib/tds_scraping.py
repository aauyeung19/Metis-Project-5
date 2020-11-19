import requests
from bs4 import BeautifulSoup
import re

def get_soup_info(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, features="html.parser")

    # title
    try:
        header = soup.find_all('section')[1]
    
        if header.find('h1'):
            title = header.find('h1').text
        else:
            title = None

        # subtitle
        if header.find('h2'):
            subtitle = header.find('h2').text
        else:
            subtitle = None

        # Look at Author information
        user_info = header.find_all('span')
        try:
            author = user_info[0].text
        except:
            try:
                author = header.find('h4').text
            except:
                author = None
    except:
        try:
            title = soup.find('article').find('h1').text
            subtitle = soup.find('article').find('h2').text
            author = soup.find('article').find('h4').text
        except:
            title = None
            subtitle = None
            author = None
    
    # get date
    try:
        date = re.search('[A-Za-z]{3} [0-9]{1,2}[,] [0-9]{4}', user_info[1].text)[0]
    except:
        date = None
    
    # paragraphs = soup.find_all('p')

    try:
        body = [paragraph.text for paragraph in soup.find_all('p')][:-2]
    except:
        body = None
        
    page_dict = {
        'title': title,
        'subtitle': subtitle,
        'author': author,
        'date': date,
        'body': body,
        'link': link
    }
    return page_dict

def to_db(page):
    """
    Puts Article Information into database
    """
    conn=psycopg2.connect(database='DS_Articles', user='postgres', host='127.0.0.1', port= '5432')

    columns_ = ','.join(page)
    val = ', '.join(["%s"]*len(page))
    query = f"INSERT INTO towards_ds ({columns_}) values ({val});"
    
    cursor = conn.cursor()
    cursor.execute("BEGIN;")
    cursor.execute(query, list(page.values()))
    cursor.execute("commit;")


if __name__ == "__main__":
    from sqlalchemy import create_engine
    import psycopg2

    # ping sitemap to get all links
    response = requests.get('https://www.towardsdatascience.com/sitemap/sitemap.xml', 'xml')
    soup = BeautifulSoup(response.text, features="html.parser")

    # make list of links but skip links to tag landing pages
    links = [link.text for link in soup.find_all('loc') if re.match("^((?!tagged*).)*$", link.text)]
    
    conn=psycopg2.connect(database='DS_Articles', user='postgres', host='127.0.0.1', port= '5432')

    for link in links:
        to_db(get_soup_info(link))