import pandas as pd

# change this
def filter_func(x):
    return x['credit'] >= 5

data = pd.read_csv('output/courses.csv')

df = data[data.apply(filter_func, axis=1)]
#data.iloc[0,:].to_csv('output/query.csv', header=False, index=False)
df.to_csv('output/query.csv', index=False)