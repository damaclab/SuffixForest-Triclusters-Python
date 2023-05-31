
import pandas as pd
import json

def get_clusters(FCP: list, min_support_count = 1) ->list:
    """Returns a list of tri-clusters from the given list of FCPs"""
    
    return [fcp.toJSON(include_object=True)
     for fcp in FCP if fcp.support_count() >= min_support_count]


def write_triclusters_to_csv(path_to_output_dir: str, filename: str, FCP: list, item_name_map: dict,  dataset_size: int, min_support_count = 1):

    data = list()
    data_decoded = list()
    for fcp in FCP:
        if fcp.support_count() >= min_support_count:
            itemset_decoded = str([item_name_map[number] for number in fcp.get_itemset()])
            itemset = str(fcp.get_itemset())
            support_count = fcp.support_count()
            support_percentage = 100*support_count/dataset_size
            support_obj = fcp.get_object_as_line()
            data.append([itemset, support_count, support_percentage, support_obj])
            data_decoded.append([itemset_decoded, support_count, support_percentage, support_obj])
            
    df = pd.DataFrame(data, columns=["Itemset", "Support(count)", "Support(%)", "Support Object"])
    filepath = f"{path_to_output_dir}/{filename}.ms={min_support_count}"
    df.to_csv(f'{filepath}.encoded.csv')
    print(f"Created file {filepath}.encoded.csv")

    df = pd.DataFrame(data_decoded, columns=["Itemset", "Support(count)", "Support(%)", "Support Object"])
    df.to_csv(f'{filepath}.decoded.csv')
    print(f"Created file {filepath}.decoded.csv")


def write_triclusters_to_json(path_to_output_dir: str, filename: str, FCP: list, min_support_count = 1):
    filepath = f'{path_to_output_dir}/{filename}.ms={min_support_count}.encoded.json'
    with open(filepath, "w") as file:
        file.write(json.dumps(get_clusters(FCP, min_support_count), indent=2))
    print(f"Created file {filepath}")
