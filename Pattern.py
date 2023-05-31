import copy
from util import get_support_count

class Pattern:
    def __init__(self, itemset: set, object: dict):
        self.itemset = set(itemset)
        self.object = copy.deepcopy(object)
    
    def __eq__(self, __o) -> bool:
        if len(__o.itemset) != len(self.itemset):
            return False
        if self.itemset != __o.itemset:
            return False
        return self.has_same_object(__o)

    def add_item(self, item):
        self.itemset.add(item)
    
    def get_object(self) -> dict:
        return copy.deepcopy(self.object)

    def get_object_ref(self) ->dict:
        return self.object
    
    def get_itemset(self) -> set:
        return self.itemset
    
    def get_copy(self):
        return Pattern(self.itemset, self.object)
    
    def size(self) -> int:
        return len(self.itemset)
    
    def is_closed(self, pattern_list) -> bool:
        """Checks whether the pattern is closed within pattern_list"""
        search_space = [pat for pat in pattern_list if pat.size() > self.size() and self.has_same_object(pat)]
    
        for pat in search_space:
            if self.get_itemset().issubset(pat.get_itemset()):
                return False
                
        return True
    
    def intersection(self, other):
        """Returns the interesction with the given pattern"""
        itemset = self.get_itemset().intersection(other.get_itemset())
        new_object = self.get_object()
        other_object = other.get_object()
        for key in other_object:
            if key in new_object:
                for e in other_object[key]:
                    if e not in new_object[key]:
                        new_object[key].append(e)
            else:
                new_object[key] = other_object[key]

        return Pattern(itemset, new_object)

    def merge_leaf(self, leaf: dict):
        for state in list(leaf.keys()):
            if state not in self.object.keys():
                self.object[state] = copy.deepcopy(leaf[state])
            else:
                for type in leaf[state]:
                    if type not in self.object[state]:
                        self.object[state].append(type)
    
    def is_object_subset(self, object1, object2):
        """Returns whether object1 is a subset of object2"""

        for state in list(object1.keys()):
            if state not in object2.keys():
                return False
            else:
                for type in object1[state]:
                    if type not in object2[state]:
                        False
        return True

    def get_object_as_line(self):
        return str(self.object)
        
    def has_same_object(self, other):
        return self.is_object_subset(self.object, other.get_object()) and self.is_object_subset(other.get_object(), self.object)

    def __str__(self): 
        return "Pattern(\n\titemset: "+str(self.itemset)+"\n\tobject: "+str(self.object)+"\n)"
    
    def support_count(self) ->int:
        return get_support_count(self.object)
        
    def toJSON(self, include_object = False) ->dict:
        JSON = {
            "itemset": list(self.itemset),
            "support": get_support_count(self.object)
        }

        if(include_object):
            JSON["object"] = self.object
        
        return JSON


if __name__ == "__main__":
    p1 = Pattern({}, {"AP" : []})
    p2 = copy.deepcopy(p1)

    p2.object["AP"] = [1]

    print(p1.get_itemset())