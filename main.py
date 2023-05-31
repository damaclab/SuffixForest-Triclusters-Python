from triclustering import Processor
import pandas as pd

processor = Processor()
processor.set_input_dataset('../input/netflix/',
                            'netflix_dataset_sample.csv',
                            oid_attribute = 'uid',
                            item_list_attribute = 'movie_ids',
                            split_attribute = 'year')

df = pd.read_csv('../input/netflix/Netflix_Dataset_Movie.csv', dtype=str)
mid_to_name = {}
for i in range(len(df)):
    mid_to_name[int(df.iloc[i]['Movie_ID'])] = df.iloc[i]['Name']


processor.process(min_support_count=2,
                  produce_intermediate_imgs=True,
                    produce_final_img=True,
                     custom_name_mapping=mid_to_name,
                      dtype_key=int)