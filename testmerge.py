import pandas as pd

df1 = pd.read_csv('courses.csv')
df2 = pd.read_csv('courses2.csv')
#df1[['id','alter_id']] = df1[['id','alter_id']].astype(str)
#df2[['id','alter_id']] = df2[['id','alter_id']].astype(str)
print(df1.columns)
print(df2.iloc[:,0:3].columns)

df = pd.merge(df1, df2, how='inner', sort=False)
# df = df.drop_duplicates(['id','alter_id'])
df.to_csv('courses3.csv', index=False)
