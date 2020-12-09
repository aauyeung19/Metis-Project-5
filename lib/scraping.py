import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime 

def get_soup(url):
    """
    Scrapes the provided url link using python's requests module and returns a BS object containing returned information text
    Scraping wrapped around try-except blocks along with conditional check if status code is 200.
    Args:
        url ([str]): website to be scrapped.
    Returns:
        soup [Beautiful Soup object]: Returns scraped text in a Beautiful Soup object type.
    """
    try:
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features="html.parser")
            return soup
        else:
            print(f"Did not get status code 200 for url: \n{url}")
            return None
    except Exception as err_msge:
        print(f"Error while scraping: {err_msge}")
        return None

def parse_body_soup(link):
    soup = get_soup(link)
    
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

    
    claps = get_claps(soup)
    n_img, n_codes = count_images(soup)

    page_dict = {
        'title': title,
        'subtitle': subtitle,
        'author': author,
        'date': date,
        'body': body,
        'link': link,
        'claps': claps,
        'images': n_img,
        'codeblocks': n_codes
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

def count_images(soup):
    try:
        n_img = len(soup.find('article').find_all('img', {'src':True, 'sizes':True}))
    except:
        n_img = 0
    try:         
        n_codes = len(soup.find('article').find_all('pre')) + len(soup.find('article').find_all('table'))
    except:
        n_codes = 0
    return n_img, n_codes

def get_claps(soup):
    no_sibling = True
    # Find first clap image and find parents until the number of claps sibling appears
    if soup==None:
        return 0
    try:
        curs = soup.find('svg', {'aria-label':'clap'})
        while no_sibling:
            try:
                claps = curs.find_next_sibling().text.strip()
                no_sibling = False
            except:
                curs = curs.find_parent()
    except:
        return 0
    
    try:
        if claps[-1]=='K':
            claps = claps[:-1]
            claps = float(claps) * 1000
        return int(claps)
    except:
        print("Claps not found for: ", link)
        return 0
    
def update_clap_count():
    """
    Searches existing links from database and updates the number of claps
    """
    links = get_current_links()
    conn=psycopg2.connect(database='DS_Articles', user='postgres', host='127.0.0.1', port= '5432')

    for link in links:
        soup = get_soup(link)
        claps = get_claps(soup)
        query = f"UPDATE towards_ds SET claps={claps} WHERE link='{link}'"
        cursor = conn.cursor()
        cursor.execute("BEGIN;")
        cursor.execute(query)
        cursor.execute("commit;")

def get_current_links():
    """ Returns links of articles already scraped"""
    conn=psycopg2.connect(database='DS_Articles', user='postgres', host='127.0.0.1', port= '5432')
    query = """
    SELECT link FROM towards_ds;
    """
    return pd.read_sql_query(query, conn)

def update_db(link):
    """Only used to update existing database that was created before the claps, images, and codeblocks columns were created"""

    soup = get_soup(link)
    claps = get_claps(soup)
    n_img, n_codes = count_images(soup)
    query = f"UPDATE towards_ds SET claps={claps}, images={n_img}, codeblocks={n_codes} WHERE link='{link}'"
    cursor = conn.cursor()
    cursor.execute("BEGIN;")
    cursor.execute(query)
    cursor.execute("commit;")

def get_2020_dates(conn):
    query = """
    SELECT author, link FROM towards_ds WHERE date is null;
    """
    df = pd.read_sql_query(query, conn)
    for author, link in zip(df.author.values, df.link.values):
        try: # Some authors are nan (makes up 11 of the population)
            # Manually add those authors later
            if len(author)==1: # One Letter Authors. Troubleshoot later
                continue
            else:
                print(link)
                soup = get_soup(str(link))
                if soup==None:
                    continue
                date = None
                for d in re.finditer('[A-Za-z]{3} [0-9]{1,2}', soup.text):
                    date = d[0]
                    try:
                        datetime.datetime.strptime(date, '%b %d')
                        break
                    except ValueError:
                        date = None
                date = date + ', 2020'
                query = f"UPDATE towards_ds SET date='{date}' WHERE link='{link}';"
                cursor = conn.cursor()
                cursor.execute("BEGIN;")
                cursor.execute(query)
                cursor.execute("commit;")
                print(f'Author: {author}, date: {date}')

        except Exception as err_msge2:
            print(f"Error while scraping: {err_msge2}")

if __name__ == "__main__":
    import psycopg2

    # ping sitemap to get all links
    response = requests.get('https://www.towardsdatascience.com/sitemap/sitemap.xml', 'xml')
    soup = BeautifulSoup(response.text, features="html.parser")

    # make list of links but skip links to tag landing pages
    links = [link.text for link in soup.find_all('loc') if re.match("^((?!tagged*).)*$", link.text)]
    conn=psycopg2.connect(database='DS_Articles', user='postgres', host='127.0.0.1', port= '5432')
    old_links = get_current_links()
    option = input('Enter U to Update or N to get New')

    if option == 'U':
        for link in old_links.values:
            update_db(link[0])
            print(link[0])

    if option == 'N':
        for link in links[::-1]:
            if link in old_links:
                update_db(link)
            else:
                to_db(parse_body_soup(link))