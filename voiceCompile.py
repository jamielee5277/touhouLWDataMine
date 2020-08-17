#coding=utf-8
import os
import json
import sys

result = {}
with open('VoiceMaster.json', encoding='utf-8') as voice:
    voice = json.load(voice)
    with open('UnitMaster.json', encoding='utf-8') as unit:
        unit = json.load(unit)
        with open('voiceTypeMaster.json', encoding='utf-8') as voiceType:
            voiceType = json.load(voiceType)
            for voiceKey in voice.keys():
                unitUnit = unit.get(str(voice[voiceKey]["unit_id"]))
                vt = voiceType.get(str(voice[voiceKey]["voice_type_id"]))["name"]
                if unitUnit != None:
                    unitName = unitUnit["name"]
                    if result.get(unitName) != None:
                        result[unitName][vt] = voice[voiceKey]["voice_text"]
                    else:
                        result[unitName] = {}
                        result[unitName][vt] = voice[voiceKey]["voice_text"]

with open('voiceCompiled.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)