from util import get_support_count
import pandas as pd
import copy
import json


def find_support_count(itemset: set, FCPs: list) -> int:
    max_count = 0
    for pattern in FCPs:
        sup_count = pattern.support_count()
        if sup_count > max_count and itemset.issubset(pattern.get_itemset()):
            max_count = sup_count
    return max_count


class Rule:
    def __init__(self, antecedent_set=set(), consequent_set=set(), support_object=dict(), confidence=0.0, lift=1.0):
        self._antecedent = set(antecedent_set)
        self._consequent = set(consequent_set)
        self._support_object = copy.deepcopy(support_object)
        self._support = get_support_count(support_object)
        self._confidence = confidence
        self._lift = lift

    def support(self) -> int:
        return self._support

    def confidence(self) -> float:
        return self._confidence

    def lift(self) -> float:
        return self._lift

    def antecedent(self) -> set:
        return self._antecedent

    def consequent(self) -> set:
        return self._consequent

    def is_valid(self, min_confidence: float) -> bool:
        return self._confidence >= min_confidence

    def is_exact(self) -> bool:
        return self._confidence == 1.0

    def generate(GEN: list, FCP: list,
                  item_name_map: dict,
                    dataset_size: int,
                      path_to_output_dir: str,
                        filename: str,
                          min_support: int,
                            min_confidence: float,
                              produce_csv,
                                produce_json):
        
        rules = Rule.generate_rules(GEN, FCP, dataset_size, min_confidence)
        for key in list(rules.keys()):
            data = list()
            data_org = list()

            filepath = f'{path_to_output_dir}/{filename}.{key}.ms={min_support}.mc={min_confidence}'
            if produce_csv:
                for rule in rules[key]:
                    confidence = rule.confidence()
                    if confidence < min_confidence:
                        continue
                    support_count = rule.support()
                    antecedent_org = str([item_name_map[item_number]
                                        for item_number in rule.antecedent()])
                    consequent_org = str([item_name_map[item_number]
                                        for item_number in rule.consequent()])
                    support_percentage = 100*support_count/dataset_size
                    lift = rule.lift()
                    data_org.append([antecedent_org, consequent_org,
                                    confidence, lift, support_count, support_percentage])
                    data.append([rule.antecedent(), rule.consequent(),
                                confidence, lift, support_count, support_percentage])

                rule_df = pd.DataFrame(data, columns=[
                                    "Antecedent", "Consequent", "Confidence", "Lift", "Support(count)", "Support(%)"])
                rule_df_org = pd.DataFrame(data_org, columns=[
                                        "Antecedent", "Consequent", "Confidence", "Lift", "Support(count)", "Support(%)"])
                rule_df.to_csv(f'{filepath}.encoded.csv')
                rule_df_org.to_csv(f'{filepath}.decoded.csv')
                print(f"Created file {filepath}.encoded.csv")
                print(f"Created file {filepath}.decoded.csv")

            if produce_json:
                rules_json_arr = [rule.toJSON(
                    include_object=True) for rule in rules[key] if rule.confidence() >= min_confidence]
                with open(f'{filepath}.encoded.json', 'w') as file:
                    file.write(json.dumps(rules_json_arr, indent=2))
                    print(f'Created file {filepath}.encoded.json')

    def get_exact_and_approximate_rules(GEN: list, FCP: list, dataset_size: int, min_confidence=0.0):
        exact_rules = list()
        approximate_rules = list()
        for g in GEN:
            antecedent = g[0].get_itemset()
            closure = g[1].get_itemset()
            for pattern in FCP:
                consequent = (pattern.get_itemset() - antecedent)
                if closure == pattern.get_itemset():
                    if (antecedent != pattern.get_itemset()):
                        lift = (pattern.support_count()*dataset_size)/(g[0].support_count() * find_support_count(consequent, FCP))
                        rule = Rule(antecedent, consequent,
                                    pattern.get_object(), 1.0, lift)
                        exact_rules.append(rule)
                else:
                    if closure.issubset(pattern.get_itemset()):
                        confidence = pattern.support_count() / g[0].support_count()
                        if confidence >= min_confidence:
                            lift = (pattern.support_count()*dataset_size) /(g[0].support_count() * find_support_count(consequent, FCP))
                            rule = Rule(antecedent, consequent,
                                        pattern.get_object(), confidence, lift)
                            approximate_rules.append(rule)
        return (exact_rules, approximate_rules)

    def get_proper_base_rules(FCP: list, dataset_size: int, min_confidence: float):
        proper_base_rules = list()
        for Fi in FCP:
            antecedent = Fi.get_itemset()
            for Fj in FCP:
                consequent = Fj.get_itemset() - antecedent
                if (Fi.size() < Fj.size() and Fi.get_itemset().issubset(Fj.get_itemset())):
                    confidence = Fj.support_count()/Fi.support_count()
                    if confidence >= min_confidence:
                        lift = (Fj.support_count()*dataset_size)/(Fi.support_count()*find_support_count(consequent, FCP))
                        rule = Rule(antecedent, consequent,
                                    Fj.get_object(), confidence, lift)
                        proper_base_rules.append(rule)
        return proper_base_rules

    # TODO: Why AR_PB and AR_SB same ?
    def generate_rules(GEN: list, FCP: list, dataset_size: int, min_confidence=0.0) -> list:
        """Generates and returns a list of Association Rules from the
         given generator list GEN and frequent closed pattern list FCP"""

        AR_E, AR_SB = Rule.get_exact_and_approximate_rules(
            GEN, FCP, dataset_size, min_confidence)
        AR_PB = Rule.get_proper_base_rules(FCP, dataset_size, min_confidence)

        return {
            "E": AR_E,
            "SB": AR_SB,
            "PB": AR_PB
        }

    def __str__(self):
        return "Rule(\n\t"+str(self._antecedent)+" => "+str(self._consequent)+"\n\tSupport: "+str(self.support())+"\n\tConfidence: "+str(self.confidence())+"\n\Lift: "+str(self.lift())+"\n)\n"

    def toJSON(self, include_object=False) -> dict:
        JSON = {
            "antecedent": list(self.antecedent()),
            "consequent": list(self.consequent()),
            "support": self.support(),
            "confidence": self.confidence(),
            "lift": self.lift()
        }

        if (include_object):
            JSON["object"] = self._support_object

        return JSON
