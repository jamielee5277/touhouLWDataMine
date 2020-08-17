#coding=utf-8
import os
import json
import sys

result = {}
with open('UnitRankPromoteMaster.json', encoding='utf-8') as unitRank:
    unitRank = json.load(unitRank)
    with open('UnitMaster.json', encoding='utf-8') as unit:
        unit = json.load(unit)
        with open('ItemMaster.json', encoding='utf-8') as item:
            item = json.load(item)
            for rel in unitRank.keys():
                unitId = unitRank[rel]["unit_id"]
                rank = unitRank[rel]["rank"]
                item1 = item[str(unitRank[rel]["slot1_object_id"])]["name"] + str(unitRank[rel]["slot1_object_value"])
                item2 = item[str(unitRank[rel]["slot2_object_id"])]["name"] + str(unitRank[rel]["slot2_object_value"])
                item3 = item[str(unitRank[rel]["slot3_object_id"])]["name"] + str(unitRank[rel]["slot3_object_value"])
                item4 = item[str(unitRank[rel]["slot4_object_id"])]["name"] + str(unitRank[rel]["slot4_object_value"])
                item5 = item[str(unitRank[rel]["slot5_object_id"])]["name"] + str(unitRank[rel]["slot5_object_value"])
                item6 = item[str(unitRank[rel]["slot6_object_id"])]["name"] + str(unitRank[rel]["slot6_object_value"])
                itemList = []
                itemList.append(item1)
                itemList.append(item2)
                itemList.append(item3)
                itemList.append(item4)
                itemList.append(item5)
                itemList.append(item6)
                if unit.get(str(unitId), None) == None:
                    continue
                if result.get(unitId, None) != None:
                    result[unitId][str(rank)] = itemList
                else:
                    result[unitId] = {
                        "name": unit[str(unitId)]["name"],
                    }
                    result[unitId][str(rank)] = itemList

with open('rankCompiled.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)