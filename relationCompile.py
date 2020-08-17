#coding=utf-8
import os
import json
import sys

result = []
with open('PersonRelationMaster.json', encoding='utf-8') as relation:
    relation = json.load(relation)
    with open('PersonMaster.json', encoding='utf-8') as unit:
        unit = json.load(unit)
        for relKey in relation.keys():
            newRel = {}
            name = relation[relKey]["description"]
            personID1 =  relation[relKey]["person_id"]
            personID2 =  relation[relKey]["target_person_id"]
            if (name == "仮テキスト"):
                continue
            newRel["关系"] = name
            newRel["人物1"] =  unit[str(personID1)]["name"]
            newRel["人物2"] =  unit[str(personID2)]["name"]
            result.append(newRel)

with open('relationCompiled.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)