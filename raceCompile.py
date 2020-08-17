#coding=utf-8
import os
import json
import sys

result = {}
with open('UnitRaceMaster.json', encoding='utf-8') as unitToRace:
    unitToRace = json.load(unitToRace)
    with open('UnitMaster.json', encoding='utf-8') as unit:
        unit = json.load(unit)
        with open('RaceMaster.json', encoding='utf-8') as race:
            race = json.load(race)
            for rel in unitToRace.keys():
                unitId = unitToRace[rel]["unit_id"]
                raceId = unitToRace[rel]["race_id"]
                if unit.get(str(unitId), None) == None:
                    continue
                if result.get(unitId, None) != None:
                    result[unitId]["race"].append(race[str(raceId)]["name"])
                else:
                    raceArray = []
                    raceArray.append(race[str(raceId)]["name"])
                    result[unitId] = {
                        "name": unit[str(unitId)]["name"],
                        "race": raceArray
                    }

with open('raceCompiled.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)