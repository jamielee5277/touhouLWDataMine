#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import json

def cleanText(text):
    return text.replace("<color=#CCAA00>", "").replace("</color>", "").replace("<color=#0066FF>", "").replace("<color=#FF6600>", "").replace("<color=#00CC66>", "")

def getEffect(text, levelValue, addon, addonChance):
    text = cleanText(text)
    if addonChance == 0 or addon == 0:
        text = text[0:-18]
        text = text.format(str(levelValue))
    else:
        text = text.format(levelValue, addonChance, addon)
    return text

with open('wiki.csv', 'w', newline='', encoding='utf-8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow('\ufeff')
    with open('infoCompiled.json', encoding='utf-8') as json_file:
        units = json.load(json_file)
        for key in units.keys():
            unit = units[key]
            spamwriter.writerow([key])
            spamwriter.writerow([unit['name'],unit['role'],unit['total_power']])
            spamwriter.writerow(['体力', '阳攻', '阴攻'])
            spamwriter.writerow([unit['life_point'],unit['yang_attack'],unit['yin_attack']])
            spamwriter.writerow(['速力', '阳防', '阴防'])
            spamwriter.writerow([unit['speed'],unit['yang_defense'],unit['yin_defense']])
            spamwriter.writerow("")
            spamwriter.writerow(['气质', unit["resist"]["name"]])
            spamwriter.writerow([unit["resist"]["description"].replace("\n", "/")])
            spamwriter.writerow(["抵抗"])
            spamwriter.writerow(unit["resist"]["Good"])
            spamwriter.writerow(["弱点"])
            spamwriter.writerow(unit["resist"]["Weak"])
            spamwriter.writerow("")
            ability = unit["ability"]
            spamwriter.writerow(["能力",ability["name"]])
            spamwriter.writerow([ability["description"].replace("\n", "/")])
            if ability["barrier_ability_description"] != "":
                spamwriter.writerow([cleanText(ability["barrier_ability_description"])])
            if ability["boost_ability_description"] != "":
                spamwriter.writerow([cleanText(ability["boost_ability_description"])])
            if ability["element_ability_description"] != "":
                spamwriter.writerow([cleanText(ability["element_ability_description"])])
            if ability["purge_ability_description"] != "":
                spamwriter.writerow([cleanText(ability["purge_ability_description"])])
            if ability["resist_ability_description"] != "":
                spamwriter.writerow([cleanText(ability["resist_ability_description"])])
            spamwriter.writerow("")
            characteristic = unit["characteristic"]
            spamwriter.writerow(["特性"])
            for i in range(1, 4):
                spamwriter.writerow([characteristic["characteristic" + str(i) + "_name"], cleanText(characteristic["characteristic" + str(i) + "_description"])])
            spamwriter.writerow(["连携", characteristic["trust_characteristic_name"], cleanText(characteristic["trust_characteristic_description"].replace("\n", "/"))])
            spamwriter.writerow("")
            spamwriter.writerow(["技能"])
            spamwriter.writerow(["技名", "Lv1", "Lv10"])
            for i in range(1, 4):
                skill = unit["skill" + str(i)]
                if skill == "Missing":
                    continue
                skillEffect1 = ""
                skillEffect10 = ""
                for j in range(1, 4):
                    effect = skill["effect" + str(j)]
                    if effect == "Missing":
                        continue
                    level1Effect = getEffect(effect["description"], effect["level1_value"], effect["level1_add_value"], effect["level1_success_rate"])
                    skillEffect1 += level1Effect + "/"
                    level10Effect = getEffect(effect["description"], effect["level10_value"], effect["level10_add_value"], effect["level10_success_rate"])
                    skillEffect10 += level10Effect + "/"
                spamwriter.writerow([skill["name"], skillEffect1[:-1], skillEffect10[:-1]])
            spamwriter.writerow("")
            spamwriter.writerow(["Shot"])
            for i in range(1, 3):
                shot = unit["shot" + str(i)]
                if shot == "Missing":
                    continue
                spamwriter.writerow([shot["name"], shot["description"].replace("\n", "/")])
                spamwriter.writerow([shot["Special"].replace("\n", "/")])
                spamwriter.writerow(["弹幕", "弹种", "威力x弹数", "命中", "暴击", "范围", "boost"])
                for j in range(1, 7):
                    line = shot[str(j)]
                    ranges = ""
                    if (line["range"] == 1):
                        ranges = "单体"
                    else:
                        ranges = "群体"

                    row = [line["name"], line["description"], "%.2f" % line["power"] + "x" + str(line["count"]), line["hit_rate"], line["critical"], ranges, line["boost"]]
                    for k in range(1, 7):
                        extra = line.get("bullet" + str(k) + "_addon_id", None)
                        if extra != None:
                            with open('BulletAddonMaster.json', encoding='utf-8') as bulletaddon:
                                 bulletaddon = json.load(bulletaddon)
                                 name = bulletaddon[str(extra)]["name"] + "(" + str(line["bullet" + str(k) + "_addon_value"]) + ")"
                                 row.append(name)
                        extra = line.get("bullet" + str(k) + "_extraeffect_id", None)
                        if extra != None:
                            with open('BulletExtraEffectMaster.json', encoding='utf-8') as bulletaddon:
                                 bulletaddon = json.load(bulletaddon)
                                 name = bulletaddon[str(extra)]["name"] + "(" + str(line["bullet" + str(k) + "_extraeffect_success_rate"]) + ")"
                                 row.append(name)
                    spamwriter.writerow(row)
                spamwriter.writerow("")
            spamwriter.writerow("")
            spamwriter.writerow(["SpellCard"])
            for i in [1, 2, 5]:
                shot = unit["spellCard" + str(i)]
                if shot == "Missing":
                    continue
                if i == 1:
                    spamwriter.writerow(["符卡1"])
                if i == 2:
                    spamwriter.writerow(["符卡2"])
                if i == 5:
                    spamwriter.writerow(["Lastword"])
                spamwriter.writerow([shot["name"], shot["description"].replace("\n", "/")])
                spamwriter.writerow([shot["Special"].replace("\n", "/")])
                for j in range(1, 6):
                    spellSkill = shot.get("spellcard_skill" + str(j), None)
                    if spellSkill != None:
                        levelType = spellSkill["spellcard_skill" + str(j) + "_level_type"]
                        timing  = spellSkill["spellcard_skill" + str(j) + "_timing"]
                        value  = spellSkill["spellcard_skill" + str(j) + "_level_value"]
                        effect = spellSkill.get("effect", None)
                        if effect != None:
                            spamwriter.writerow(["符卡技能" + str(j)])
                            if levelType == 1:
                                level1Effect = getEffect(effect["description"], effect["level" + str(value) + "_value"], effect["level" + str(value) + "_add_value"], effect["level" + str(value) + "_success_rate"])
                                if timing == 1:
                                    spamwriter.writerow(["前置(固定)", level1Effect])
                                elif timing == 2:
                                    spamwriter.writerow(["后置(固定)", level1Effect])
                            if levelType == 2:
                                for k in [2, 4, 6, 8, 10]:
                                    level1Effect = getEffect(effect["description"], effect["level" + str(k) + "_value"], effect["level" + str(k) + "_add_value"], effect["level" + str(k) + "_success_rate"])
                                    if timing == 1:
                                        spamwriter.writerow(["前置(星" + str(round(k/2,0))[:-2] + ")", level1Effect])
                                    elif timing == 2:
                                        spamwriter.writerow(["前置(星" + str(round(k/2,0))[:-2] + ")", level1Effect])
                            if levelType == 3:
                                for k in [1, 4, 7, 10]:
                                    level1Effect = getEffect(effect["description"], effect["level" + str(k) + "_value"], effect["level" + str(k) + "_add_value"], effect["level" + str(k) + "_success_rate"])
                                    if timing == 1:
                                        spamwriter.writerow(["前置(Boost" + str(round((k-1)/3,0))[:-2] + ")", level1Effect])
                                    elif timing == 2:
                                        spamwriter.writerow(["前置(Boost" + str(round((k-1)/3,0))[:-2] + ")", level1Effect])
                spamwriter.writerow("")
                spamwriter.writerow(["弹幕", "弹种", "威力x弹数", "命中", "暴击", "范围", "boost", "其他"])
                for j in range(1, 7):
                    line = shot.get(str(j), None)
                    if line == None:
                        continue
                    ranges = ""
                    if (line["range"] == 1):
                        ranges = "单体"
                    else:
                        ranges = "群体"

                    row = [line["name"], line["description"], "%.2f" % line["power"] + "x" + str(line["count"]), line["hit_rate"], line["critical"], ranges, line["boost"]]
                    for k in range(1, 7):
                        extra = line.get("bullet" + str(k) + "_addon_id", None)
                        if extra != None:
                            with open('BulletAddonMaster.json', encoding='utf-8') as bulletaddon:
                                 bulletaddon = json.load(bulletaddon)
                                 name = bulletaddon[str(extra)]["name"] + "(" + str(line["bullet" + str(k) + "_addon_value"]) + ")"
                                 row.append(name)
                        extra = line.get("bullet" + str(k) + "_extraeffect_id", None)
                        if extra != None:
                            with open('BulletExtraEffectMaster.json', encoding='utf-8') as bulletaddon:
                                 bulletaddon = json.load(bulletaddon)
                                 name = bulletaddon[str(extra)]["name"] + "(" + str(line["bullet" + str(k) + "_extraeffect_success_rate"]) + ")"
                                 row.append(name)
                    spamwriter.writerow(row)
                spamwriter.writerow("")
            with open('rankCompiled.json', encoding='utf-8') as rank:
                rank = json.load(rank)
                ranked = rank.get(key, None)
                if ranked != None:
                    spamwriter.writerow(["Rank材料"])
                    for j in range(0, 5):
                        spamwriter.writerow(ranked[str(j)])
            spamwriter.writerow(["========================================================================================"])
            spamwriter.writerow([""])
