import copy
from printing_util import generate_forest_image
import json

def get_all_suffix(arr, leaf_obj):
    all_suffix = []

    for i in range(len(arr)):
        all_suffix.append(get_suffix(arr, i, copy.deepcopy(leaf_obj)))

    return all_suffix


def get_suffix(arr, idx, leaf_obj):
    suffix = []

    while idx < len(arr):
        suffix.append(arr[idx])
        idx += 1

    suffix.append(leaf_obj)
    return suffix


def build_sufix_forest(sfd_list, produce_intermediate_images = False, produce_final_image = False, output_dir = ".", filename = ""):
    h_tree = {}
    count = 1
    image_path = f'{output_dir}/{filename}'

    for type in sfd_list.keys():
        SFD = sfd_list[type]
        for state in SFD.keys():
            suffixes = get_all_suffix(SFD[state], {
                state: [type]
            })

            for suffix in suffixes:
                assert len(suffix) > 1

                if suffix[0] in h_tree.keys():
                    match(h_tree[suffix[0]], suffix)
                else:
                    h_tree[suffix[0]] = build(suffix)
                if(produce_intermediate_images):
                    generate_forest_image(h_tree, f'{image_path}.itermediate{count}.png')
                    count += 1

    if(produce_final_image):               
        generate_forest_image(h_tree, f'{image_path}.final.png')
    return h_tree


def match(h_node, suffix):
    assert h_node["item"] == suffix[0]

    if (len(suffix) == 2):  # suffix[1] is a leaf node
        if h_node["leaf"] == None:
            h_node["leaf"] = copy.deepcopy(suffix[1])
        else:
            # merge the new leaf with the existing leaf
            tree_leaf = h_node["leaf"] #Note: reference (alias) to h_node["leaf"] is used
            state = list(suffix[1].keys())[0]
            type = suffix[1][state][0]

            if (state in tree_leaf.keys()):
                if (type in tree_leaf[state]):
                    print("Warning: Same row already exists in forest for ("+state+", "+type+").")
                else:
                    tree_leaf[state].append(type)
            else:
                tree_leaf[state] = [type]
    else:
        # suffix[1] will not be a leaf

        # matching suffix[1]
        for child in h_node["children"]:
            if child["item"] == suffix[1]:
                match(child, suffix[1:])
                return
        # if no match is found, building h_node
        h_node["children"].append(build(suffix[1:]))


def build(suffix):
    assert len(suffix) >= 2
    h_node = {
        "item": suffix[0],
        "children": [],
        "leaf": None
    }

    if len(suffix) == 2:
        h_node["leaf"] = copy.deepcopy(suffix[1])
    else:
        h_node["children"].append(build(suffix[1:]))
    return h_node


def produce_forest_json(path_to_dir: str, filename: str, h_tree: dict, min_sup_count: int):
    filepath = f'{path_to_dir}/{filename}.ms={min_sup_count}.encoded.json'
    with open(filepath, "w") as file:
        file.write(json.dumps(h_tree, indent=2))
