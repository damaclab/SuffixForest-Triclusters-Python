import pandas as pd
import math
from suffix_forest import build_sufix_forest, produce_forest_json
from frequent_patterns import get_FCPs
from generators import get_generators, write_generators_to_csv
from association_rules import Rule
from tricluster import write_triclusters_to_csv, write_triclusters_to_json
import os

class Processor:
    def __init__(self):
        self.h_tree = None
        self.df = None
        self.OID_ATTR = 'OID'
        self.ITEM_LIST_ATTR = 'ITEM_LIST'
        self.SPLIT_ATTR = 'SPLIT'
        self.min_sup_count = 1
        self.min_sup_count_number_table = 1
        self.min_confidence = 0.0
        self.number_table = None
        self.item_name_table = None
        self.sfd_list = None
        self.output_directory_path = '.'
        self.h_tree = None
        self.fcp_list = None
        self.genarator_closure_pairs = None
        self.filename = None
    
    def set_input_dataset(self, input_file_dir: str,
                           input_file_name: str,
                             oid_attribute: str,
                               item_list_attribute: str,
                                 split_attribute: str):
        self.df = pd.read_csv(os.path.join(input_file_dir, input_file_name))
        self.df = self.df[[oid_attribute, item_list_attribute, split_attribute]]
        self.df = self.df.rename(columns={oid_attribute: self.OID_ATTR})
        self.df = self.df.rename(columns={item_list_attribute: self.ITEM_LIST_ATTR})
        self.df = self.df.rename(columns={split_attribute: self.SPLIT_ATTR})

        self.filename = input_file_name.split('.')[0]
        self.output_directory_path = os.path.join(input_file_dir, 'output')

        try:
            os.mkdir(self.output_directory_path)
        except FileExistsError:
            print(f'Directory {self.output_directory_path} already exists.')

        print(f'Output directory is set to {self.output_directory_path}')

    def process(self,
                min_support_percentage_number_table = 0.0,
                 min_support_count = 1,
                   min_confidence = 0.0,
                     produce_intermediate_imgs = False,
                       produce_final_img = False,
                         custom_name_mapping = None,
                           dtype_key = None):
        assert not self.df.empty
        
        if min_support_count > 1:
                self.set_minmum_support_count(min_support_count)
                self.min_sup_count_number_table = min_support_count

        if min_confidence > 0.0:
            self.set_minimum_conidence(min_confidence)
        
        if min_support_percentage_number_table > 0.0:
            self.min_sup_count_number_table = math.ceil(len(self.df)*min_support_percentage_number_table*0.01)


        self._form_number_table()

        if(custom_name_mapping != None):
                for (key, value) in self.item_name_table.items():
                    self.item_name_table[key] = custom_name_mapping[dtype_key(value)]

        self.get_sfd_list()
        self.build_forest(produce_intermediate_imgs,
                           produce_final_img,
                             f'{self.filename}.forest')
        self.extract_fcp_list()
        self.find_generator_closure_pairs()
        self.generate_files()
        print('process completed')  

    def generate_files(self):
        self.produce_number_table_csv(f'{self.filename}.number_table')
        produce_forest_json(self.output_directory_path,
                            f'{self.filename}.forest',
                              self.h_tree,
                                self.min_sup_count)
        self.produce_triclusters_csv(f'{self.filename}.triclusters')
        self.produce_triclusters_json(f'{self.filename}.triclusters')
        self.generate_rules(f'{self.filename}.rule',
                            self.min_sup_count,
                            self.min_confidence,
                            produce_csv = True,
                            produce_json = True)
        self.produce_generators_csv(f'{self.filename}.generators',
                                     include_object = True)

    def set_output_directory_path(self, output_dir_path):
        self.output_directory_path = output_dir_path

    def set_minmum_support_count(self, count: int):
        self.min_sup_count = count

    def set_minimum_conidence(self, min_conidence: float):
        self.min_confidence = min_conidence

    def set_min_suuport_percent(self, percent: int):
        self.min_sup_count =  math.ceil((len(self.df)*percent)/100)
        return self.min_sup_count
    
    def _form_number_table(self, print_item_tbl = False, print_number_tbl = False):
        support = dict()
        for i in range(len(self.df)):
            for item in set(self.df.loc[i, self.ITEM_LIST_ATTR].split(',')):
                if item not in support:
                    support[item] = 1
                else:
                    support[item] += 1

        items = [ (item, count) for (item, count) in support.items() if count >= self.min_sup_count_number_table]
        items = sorted(items, key = lambda x: x[1])

        number_table = dict()
        item_name_table = dict()

        for i, (item, count) in enumerate(items):
            number_table[item] = (i+1)
            item_name_table[i+1] = item

        self.number_table = number_table
        self.item_name_table = item_name_table

        if(print_item_tbl):
            print("item table: \n", str(support))

        if(print_number_tbl):
            print("number table: \n", str(number_table))

    def produce_number_table_csv(self, filename: str):
        data = []
        for (item_name, item_number) in self.number_table.items():
            data.append([item_name, item_number])
        df = pd.DataFrame(data, columns = ['Item Name', "Item Number"])
        df.to_csv(f'{self.output_directory_path}/{filename}.ms={self.min_sup_count}.csv', index=False)
        print(f'Created file {self.output_directory_path}/{filename}.ms={self.min_sup_count}.csv')

    def get_sfd_list(self, create_datesets = False):
        self.sfd_list = dict()
        grouped_df = self.df.groupby(by=self.SPLIT_ATTR)
        for split_val, data in grouped_df:
            if(create_datesets):
                filepath = f'{self.output_directory_path}/SFD_{str(split_val)}.csv'
                data.to_csv(filepath)
            SFD = dict()
            for i in data.index:
                itemset = list()
                item_list = set(data[self.ITEM_LIST_ATTR][i].split(','))
                for (item, item_number) in self.number_table.items():
                    if item in item_list:
                        itemset.append(item_number)
                SFD['O'+str(data[self.OID_ATTR][i])] = itemset
            self.sfd_list[str(split_val)] = SFD
        return self.sfd_list
    
    def build_forest(self, produce_intermediate_images = False, produce_final_image = False, filename = ""):
        self.h_tree = build_sufix_forest(self.sfd_list,
                                          produce_intermediate_images,
                                            produce_final_image,
                                              self.output_directory_path,
                                                filename)
        return self.h_tree

    def extract_fcp_list(self, min_support_count = 1):
        self.fcp_list = get_FCPs(self.h_tree, min_support_count)
        return self.fcp_list
    
    def find_generator_closure_pairs(self, produce_csv = False):
        self.genarator_closure_pairs = get_generators(self.fcp_list)
        if(produce_csv):
            write_generators_to_csv(self.output_directory_path, self.genarator_closure_pairs)

    def set_item_name_table(self, custom_name_table: dict):
        self.item_name_table = custom_name_table
    
    def generate_rules(self, filename,
                        support_count_filter = 0,
                          min_confidence_filter = 0.0,
                            produce_csv = True,
                              produce_json = True): 
        Rule.generate(self.genarator_closure_pairs,
                       self.fcp_list,
                       self.item_name_table,
                       len(self.df),
                       self.output_directory_path,
                       filename,
                       support_count_filter,
                       min_confidence_filter,
                       produce_csv,
                       produce_json)
    
    def produce_triclusters_csv(self, filename: str, support_count_filter = 0):
        min_sup_count_cluster = self.min_sup_count
        if(support_count_filter > 0):
            min_sup_count_cluster = support_count_filter

        write_triclusters_to_csv(self.output_directory_path,
                                 filename,
                                 self.fcp_list,
                                 self.item_name_table,
                                 len(self.df),
                                min_sup_count_cluster)
        
    def produce_triclusters_json(self, filename: str, support_count_filter = 0):
        min_sup_count_cluster = self.min_sup_count
        if(support_count_filter > 0):
            min_sup_count_cluster = support_count_filter

        write_triclusters_to_json(self.output_directory_path,
                                  filename,
                                  self.fcp_list,
                                  min_sup_count_cluster)

    def produce_generators_csv(self, filename: str, include_object: bool):
        write_generators_to_csv(self.output_directory_path,
                                 filename,
                                   self.genarator_closure_pairs,
                                     self.min_sup_count,
                                       include_object)
    