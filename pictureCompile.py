#coding=utf-8
import os
import json
import sys

result = {}
with open('PictureMaster.json', encoding='utf-8') as picture:
    picture = json.load(picture)
    for key in picture.keys():
        entry = {}
        entry["1"] = picture[key]["flavor_text1"]
        entry["2"] = picture[key]["flavor_text2"]
        entry["3"] = picture[key]["flavor_text3"]
        entry["4"] = picture[key]["flavor_text4"]
        entry["5"] = picture[key]["flavor_text5"]
        entry["画师"] = picture[key]["illustrator_name"]
        result[picture[key]["name"]] = entry

with open('pictureCompiled.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)