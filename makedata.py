from bs4 import BeautifulSoup
import pandas as pd
import csv
import json

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

# change column name from Chinese to English
data = pd.read_csv('output/courses.csv')
data.drop(data.columns[17:20], axis=1, inplace=True)
data.columns = ['department','id','alter_id','name','credit','teacher','capacity',\
		'capacity_graduate','time','restrict','character','grade',\
		'second_choose','exprement','retry','choose_or_not','group']
data.to_csv('output/courses.csv', index=False)

# csv to json: http://blog.topspeedsnail.com/archives/3923
csv_rows = []
with open('output/courses.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    title = reader.fieldnames
    for row in reader:
        csv_rows.extend([{title[i]:row[title[i]] \
                        for i in range(len(title))}])

with open('output/courses.json','w') as f:
    f.write(json.dumps(csv_rows, sort_keys=False, indent=4, \
            separators=(',', ': '),ensure_ascii=False))
