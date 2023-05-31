import itertools
from Pattern import Pattern
from util import get_support_count
import pandas as pd

def get_generators(FCP: list):
    """Returns the list of generators from the FCP list"""
    FCP.sort(key = comparator)
    GEN = []
    
    for i in range(len(FCP)):
        pattern = FCP[i].get_copy()
        found_gen = False
        generator_size = 1

        while found_gen == False and generator_size < pattern.size():
            subsets = get_all_subsets(pattern.get_itemset(), generator_size)

            for subset in subsets:
                not_generator = False
                for generator in GEN:
                    if generator[0].get_itemset() == subset:
                        not_generator = True
                        break
                if not_generator == False:
                    #TODO: Is this what is meant by "for all C ∈ FCP preceding F ∈ FCP" ?
                    for j in range(i):
                        if subset.issubset(FCP[j].get_itemset()):
                            not_generator = True
                            break
                if not_generator == False:
                    #TODO: Is this the correct Object List for the generators ?
                    GEN.append([Pattern(subset, pattern.get_object()), pattern])
                    found_gen = True
                    #TODO: Should we break here and not test other subsets ?
            generator_size += 1

        if found_gen == False:
            GEN.append([pattern, pattern.get_copy()])
    return GEN



def comparator(pattern: Pattern) ->int:
    """Custom key funtion that will be used for used for soring FCPs
    based on the size of the pattern"""
    return pattern.size()

def get_all_subsets(subset: set, n: int) ->list:
    """Returns all possible subsets of size n from the given subset"""
    return [set(tpl) for tpl in itertools.combinations(subset, n)]

def write_generators_to_csv(output_dir: str, filename: str,  GENs: list, min_sup_count, include_object = False):
    data = list()
    for [gen, clos] in GENs:
        generator = str(list(gen.get_itemset()))
        closure = str(list(clos.get_itemset()))
        if include_object:
            support_object = clos.get_object_as_line()
        support_count = get_support_count(clos.get_object())
        if include_object:
            data.append([generator, closure, support_count, support_object])
        else:
            data.append([generator, closure, support_count])
    if include_object:
        df = pd.DataFrame(data, columns = ["Generator", "Closure", "Support Count","Support Object"])
    else:
        df = pd.DataFrame(data, columns = ["Generator", "Closure", "Support Count"])
    filename = f'{output_dir}/{filename}.ms={min_sup_count}.csv'
    df.to_csv(filename, index=False)
    print(f"Created file {filename}")