
# User_ID,Rating,Movie_ID
# 712664,5,3
# 1331154,4,3
# 2632461,3,3
# 44937,5,3
# 656399,4,3
# 439011,1,3
# 1644750,3,3

# Movie_ID,Year,Name
# 1,2003,Dinosaur Planet
# 2,2004,Isle of Man TT 2004 Review
# 3,1997,Character
# 4,1994,Paula Abdul's Get Up & Dance
# 5,2004,The Rise and Fall of ECW

import pandas as pd

df = pd.read_csv('Netflix_Dataset_Movie.csv', dtype=str)
movie = {}
for i in range(len(df)):
    movie[df.iloc[i]['Movie_ID']] = (df.iloc[i]['Name'], df.iloc[i]['Year'])

df = pd.read_csv('Netflix_Dataset_Rating.csv', dtype=str)
df = df.rename(columns={'User_ID': 'uid'})

df = df.head(250000) # Only take the first 0.25 Million rows 
df = df.loc[df['Rating'] == "5"] # Only take ratings of 5

# Adding the year column
df['year'] = [movie[mid][1] for mid in df['Movie_ID']]

df = df.groupby(['uid', 'year']).agg({"Movie_ID": lambda x: ",".join(x)})
df = df.rename(columns={'Movie_ID': 'movie_ids'})

percent = 50 # Deleting this percentage of rows randomly
n = int(percent/100 * len(df))
rows_to_delete = df.sample(n=n, random_state=42)
df = df.drop(rows_to_delete.index)
df.to_csv("netflix_dataset.csv")

data = df['movie_ids']
data_org = []
for item_list in data:
    element = ','.join([movie[mid][0] for mid in item_list.split(',')])
    data_org.append(element)
df = pd.DataFrame(data_org, columns = ['item_list'])
df.to_csv('netflix_dataset_item_names.csv', index=False)