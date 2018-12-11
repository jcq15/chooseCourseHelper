from bs4 import BeautifulSoup
import pandas as pd

def getDFFromFile(fname):
    with open(fname,'r') as f:
        txt = f.read()
    soup = BeautifulSoup(txt, 'html.parser')
    tables = soup.select('table')
    df_list = []
    for table in tables:
        df_list.append(pd.concat(pd.read_html(table.prettify())))
    df = pd.concat(df_list)
    return df

# first page
getDFFromFile('pages/page1.html').iloc[:-1,:]\
.to_csv('courses.csv', header=False, index=False)

# other pages
pages = 2
try:
    while True:
        getDFFromFile('pages/page%s.html'%pages).iloc[2:-1,:]\
        .to_csv('output/courses.csv', header=False, index=False, mode='a')
        print('%ssucceed!'%pages)
        pages = pages + 1
except FileNotFoundError as e:
    print('stop at %s'%pages)

