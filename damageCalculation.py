#coding=utf-8
import os
import json
import sys

# this can be optimized
def sortByLwP0(item):
    if (item == "Missing"):
        return -1
    if (item["LastWordDamage"] == "Missing"):
        return -1
    return item["LastWordDamage"]["P0"]
def sortByLwP1(item):
    if (item == "Missing"):
        return -1
    if (item["LastWordDamage"] == "Missing"):
        return -1
    return item["LastWordDamage"]["P1"]
def sortBySC1P1(item):
    if (item == "Missing"):
        return -1
    if (item["LastWordDamage"] == "Missing"):
        return -1
    return item["SpellCard1Damge"]["P1"]
def sortBySC2P1(item):
    if (item == "Missing"):
        return -1
    if (item["LastWordDamage"] == "Missing"):
        return -1
    return item["SpellCard2Damge"]["P1"]
def sortBySC1P1(item):
    if (item == "Missing"):
        return -1
    if (item["LastWordDamage"] == "Missing"):
        return -1
    return item["SpellCard1Damge"]["P3"]
def sortBySC2P3(item):
    if (item == "Missing"):
        return -1
    if (item["LastWordDamage"] == "Missing"):
        return -1
    return item["SpellCard2Damge"]["P3"]
def sortByLwP3(item):
    if (item == "Missing"):
        return -1
    if (item["LastWordDamage"] == "Missing"):
        return -1
    return item["LastWordDamage"]["P2"]
def sortByLwP3(item):
    if (item == "Missing"):
        return -1
    if (item["LastWordDamage"] == "Missing"):
        return -1
    return item["LastWordDamage"]["P3"]

def sortBySCP1(item):
    if (item == "Missing"):
        return -1
    if (item["LastWordDamage"] == "Missing"):
        return -1
    return max(item["SpellCard2Damge"]["P1"], item["SpellCard1Damge"]["P1"])


def sortAllCard(item):
    return item[2]

def getSpellBuffAmount(spellEffectId, levelType, levelValue, timing):
    buffAmount = {}
    buffAmount["yin_buff"] = 0
    buffAmount["yang_buff"] = 0
    buffAmount["yin_debuff"] = 0
    buffAmount["yang_debuff"] = 0
    if timing != 1:
        return buffAmount
    with open('SkillEffectMaster.json', encoding='utf-8') as json_file:
        effects = json.load(json_file).get(str(spellEffectId), None)
        level = 0
        if levelValue != 0:
            level = levelValue
        else:
            level = 10
        if effects == None:
            return buffAmount
        if effects["subtype"] == 1 and effects["type"] == 1 and (effects["range"] == 1 or effects["range"] == 2):
            buffAmount["yang_buff"] = effects["level" + str(level) + "_value"]
        elif effects["subtype"] == 2 and effects["type"] == 2 and (effects["range"] == 3 or effects["range"] == 4):
            buffAmount["yang_debuff"] = effects["level" + str(level) + "_value"]
        elif effects["subtype"] == 3 and effects["type"] == 1 and (effects["range"] == 1 or effects["range"] == 2):
            buffAmount["yin_buff"] = effects["level" + str(level) + "_value"]
        elif effects["subtype"] == 4 and effects["type"] == 2 and (effects["range"] == 3 or effects["range"] == 4):
            buffAmount["yin_debuff"] = effects["level" + str(level) + "_value"]
    return buffAmount

def getSpellCardDamage(key, buff, unit):
    yin_attack = unit["yin_attack"]
    yang_attack = unit["yang_attack"]
    speed = unit["speed"]
    yin_buff_current = buff["yin_buff"]
    yang_buff_current = buff["yang_buff"]
    yin_debuff_current = buff["yin_debuff"]
    yang_debuff_current = buff["yang_debuff"]
    yin_boost = buff["yin_boost"]
    yang_boost = buff["yang_boost"]
    speed_buff = buff["speed_buff"]
    speed_boost = buff["speed_boost"]
    spellCard1 = unit["spellCard" + str(key)]
    if (spellCard1 == "Missing"):
        return "Missing"
    for i in range(1, 6):
        skill = spellCard1.get("spellcard_skill" + str(i), None)
        if skill == None:
            continue
        spellEffectId = skill["spellcard_skill" + str(i) + "_effect_id"]
        levelType = skill["spellcard_skill" + str(i) + "_level_type"]
        levelValue = skill["spellcard_skill" + str(i) + "_level_value"]
        timing = skill["spellcard_skill" + str(i) + "_timing"]
        buff2 = getSpellBuffAmount(spellEffectId, levelType, levelValue, timing)
        yin_buff_current += buff2["yin_buff"]
        yang_buff_current += buff2["yang_buff"]
        yin_debuff_current += buff2["yin_debuff"]
        yang_debuff_current += buff2["yang_debuff"]
    
    damageMap = {}
    damageMap["P0"] = 0
    damageMap["P1"] = 0
    damageMap["P2"] = 0
    damageMap["P3"] = 0
    damageMap["buff"] = buff
    yang_neg = 0
    if yang_buff_current < 0:
        yang_neg = -yang_buff_current
        yang_buff_current = 0
    for i in range(0, 4):
        rawTotalDamage = 0
        yin_att_multiplier = (1.0 + 0.3 * min(yin_buff_current + yin_boost * i, 10))
        yin_extra_multiplier =  (1 + 0.3 * yin_debuff_current)
        if (unit["id"] in sheildYin):
            yin_extra_multiplier *= 1.15*1.15
        yang_att_multiplier = (1.0 + 0.3 * min(yang_buff_current + yang_boost * i, 10)) 
        yang_extra_multiplier = (1 + 0.3 * yang_debuff_current) / (1 + 0.3*yang_neg)
        for j in range(1, 7):
            extra = 0
            bullet = spellCard1.get(str(j), None)
            if bullet == None:
                continue
            for k in range(1, 4):
                addOnId = bullet.get("bullet" + str(k) +"_addon_id", None)
                if addOnId == None:
                    continue
                addOnValue = bullet.get("bullet" + str(k) +"_addon_value")
                if addOnId == 5:
                    extra += speed * (1 + speed_buff * 0.3 + speed_boost * i) * addOnValue/100
                if addOnId == 4:
                    extra += unit["yin_defense"] * addOnValue/100
            if bullet["boost"] <= i:
                rawDamage =  bullet["power"] * bullet["count"] * spellCard1["shot_level5_power_rate"] / 100
                # not reliable, changing later
                if (bullet["description"][0] == "陽"):
                    rawDamage *= yang_extra_multiplier * (yang_attack * yang_att_multiplier + extra)
                    if unit["id"] == "1010":
                        if j == 1 or j == 5:
                            rawDamage = rawDamage * 1.3
                        if j == 2 or j == 4 or j == 2:
                            rawDamage = rawDamage * 1.25
                else:
                    rawDamage *= yin_extra_multiplier * (yin_attack * yin_att_multiplier + extra)
                    if unit["id"] == "1016":
                        if bullet["boost"] == 0:
                            rawDamage = rawDamage * 1.3
                rawTotalDamage += rawDamage
        damageMap["P" + str(i)] = rawTotalDamage
    return damageMap
 
def getSkillBuff(unit):
    level = 10
    buffAmount = {}
    buffAmount["yin_buff"] = 0
    buffAmount["yang_buff"] = 0
    buffAmount["yin_debuff"] = 0
    buffAmount["yang_debuff"] = 0
    buffAmount["speed_buff"] = 0
    p = 0
    for i in range(1, 4):
        skill = unit["skill" + str(i)]
        if skill == "Missing":
            continue
        for j in range(1, 4):
            effects = skill.get("effect" + str(j), "Missing")
            if effects == "Missing":
                continue
            if effects["subtype"] == 1 and effects["type"] == 1 and (effects["range"] == 1 or effects["range"] == 2):
                buffAmount["yang_buff"] += effects["level" + str(level) + "_value"]
            elif effects["subtype"] == 2 and effects["type"] == 2 and (effects["range"] == 3 or effects["range"] == 4):
                buffAmount["yang_debuff"] += effects["level" + str(level) + "_value"]
            elif effects["subtype"] == 3 and effects["type"] == 1 and (effects["range"] == 1 or effects["range"] == 2):
                buffAmount["yin_buff"] += effects["level" + str(level) + "_value"]
            elif effects["subtype"] == 4 and effects["type"] == 2 and (effects["range"] == 3 or effects["range"] == 4):
                buffAmount["yin_debuff"] += effects["level" + str(level) + "_value"]
            elif effects["subtype"] == 1 and effects["type"] == 2 and (effects["range"] == 1 or effects["range"] == 2):
                buffAmount["yang_buff"] -= effects["level" + str(level) + "_value"]
            elif effects["subtype"] == 5 and effects["type"] == 1 and (effects["range"] == 1 or effects["range"] == 2):
                buffAmount["speed_buff"] += effects["level" + str(level) + "_value"] 
    # if p == 1:
    #     buffAmount["yin_buff"] = 0
    #     buffAmount["yang_buff"] = 0
    return buffAmount

def getPassiveBuff(ability):
    buffAmount = {}
    buffAmount["yin_buff"] = 0
    buffAmount["yang_buff"] = 0
    buffAmount["yin_debuff"] = 0
    buffAmount["yang_debuff"] = 0
    buffAmount["yang_boost"] = 0
    buffAmount["yin_boost"] = 0
    buffAmount["speed_boost"] = 0
    buffAmount["speed_buff"] = 0
    if ability == None:
        return buffAmount
    abilityId = ability.get("id", None)
    if abilityId == None:
        return buffAmount
    with open('AbilityMaster.json', encoding='utf-8') as json_file:
        effects = json.load(json_file).get(str(abilityId), None)
        # self or all buff
        if (effects["boost_power_divergence_range"] == 0 or effects["boost_power_divergence_range"] == 1):
            if effects["boost_power_divergence_type"] == 1:
                buffAmount["yang_boost"] = 1
            elif effects["boost_power_divergence_type"] == 3:
                buffAmount["yin_boost"] = 1
            elif effects["boost_power_divergence_type"] == 5:
                buffAmount["speed_boost"] = 1
        if effects["purge_barrier_diffusion_range"] == 0 or effects["purge_barrier_diffusion_range"] == 1:
            if effects["purge_barrier_diffusion_type"] == 1:
                buffAmount["yang_buff"] = 3
            elif effects["purge_barrier_diffusion_type"] == 3:
                buffAmount["yin_buff"] = 3
            elif effects["purge_barrier_diffusion_type"] == 5:
                buffAmount["speed_buff"] = 3
    return buffAmount

finalResult = {}
finalList = []
allCardList = []
# 命中加成
# done by hardcoding now, need to automate later
specialIdYin = ["1003", "1032", "1016", "1017", "1039"]
specialIdYang = ["1035", "1040", "1015"]
sheildYin = ["1006"]
with open('infoCompiled.json', encoding='utf-8') as json_file:
    units = json.load(json_file)
    for key in units.keys():
        unitResult = {}
        unit = units[key]
        buffAmount = getSkillBuff(unit)
        #print(unit["name"])
        yin_buff = buffAmount["yin_buff"]
        yang_buff = buffAmount["yang_buff"]
        yin_debuff = buffAmount["yin_debuff"]
        yang_debuff = buffAmount["yang_debuff"]
        speed_buff = buffAmount["speed_buff"]
        buffAmount = getPassiveBuff(unit["ability"])
        #print(buffAmount)
        yin_buff += buffAmount["yin_buff"]
        yang_buff += buffAmount["yang_buff"]
        yin_debuff += buffAmount["yin_debuff"]
        yang_debuff += buffAmount["yang_debuff"]
        yin_boost = buffAmount["yin_boost"]
        yang_boost = buffAmount["yang_boost"]
        speed_buff += buffAmount["speed_buff"]
        speed_boost = buffAmount["speed_boost"]
        unitResult["name"] = unit["name"]
        unit["id"] = key
        if (key in specialIdYang):
            yang_buff += 3
        if (key in specialIdYin):
            yin_buff += 3
        buff = {
            "yin_buff": yin_buff,
            "yang_buff": yang_buff,
            "yin_debuff": yin_debuff,
            "yang_debuff": yang_debuff,
            "yin_boost": yin_boost,
            "yang_boost": yang_boost,
            "speed_buff": speed_buff,
            "speed_boost": speed_boost,
        }
        card1Damage = getSpellCardDamage(1, buff, unit)
        card2Damage = getSpellCardDamage(2, buff, unit)
        lastwordDamage = getSpellCardDamage(5, buff, unit)
        for i in range (0, 4):
            if (card1Damage == "Missing"):
                continue
            cardEntry1 = (unit["name"] + " SC1", "P" + str(i) ,card1Damage["P" + str(i)])
            cardEntry2 = (unit["name"] + " SC2", "P" + str(i) ,card2Damage["P" + str(i)])
            cardEntry3 = (unit["name"] + " LW", "P" + str(i) ,lastwordDamage["P" + str(i)])
            allCardList.append(cardEntry1)
            allCardList.append(cardEntry2)
            allCardList.append(cardEntry3)
        unitResult["SpellCard1Damge"] = card1Damage
        unitResult["SpellCard2Damge"] = card2Damage
        unitResult["LastWordDamage"] = lastwordDamage
        finalResult[key] = unitResult
        finalList.append(unitResult)
    with open('damage.json', 'w', encoding='utf-8') as json_file:
        json.dump(finalResult, json_file, ensure_ascii=False, indent=2)
    with open('damageP0.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortByLwP0)
        json.dump(finalList, json_file, ensure_ascii=False, indent=2)
    with open('damageP1.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortByLwP1)
        json.dump(finalList, json_file, ensure_ascii=False, indent=2)
    # with open('damageP2.json', 'w', encoding='utf-8') as json_file:
    #     finalList.sort(reverse=True, key=sortByLwP2)
    #     json.dump(finalList, json_file, ensure_ascii=False, indent=2)
    with open('damageP3.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortByLwP3)
        json.dump(finalList, json_file, ensure_ascii=False, indent=2)
    with open('allCardDamage.json', 'w', encoding='utf-8') as json_file:
        allCardList.sort(reverse=True, key=sortAllCard)
        json.dump(allCardList, json_file, ensure_ascii=False, indent=2)
    with open('allCardRank.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortByLwP1)
        simpleList = []
        count = 1
        for i in finalList:
            simpleList.append(str(count) + ": " + i["name"])
            count =  count+1
        json.dump(simpleList, json_file, ensure_ascii=False, indent=2)
    with open('allCardRankP3.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortByLwP3)
        simpleList = []
        count = 1
        for i in finalList:
            simpleList.append(str(count) + ": " + i["name"])
            count =  count+1
        json.dump(simpleList, json_file, ensure_ascii=False, indent=2)
    with open('allCardRankP1SC1.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortBySC1P1)
        simpleList = []
        count = 1
        for i in finalList:
            simpleList.append(str(count) + ": " + i["name"])
            count =  count+1
        json.dump(simpleList, json_file, ensure_ascii=False, indent=2)
    with open('allCardRankP1SC2.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortBySC2P1)
        simpleList = []
        count = 1
        for i in finalList:
            simpleList.append(str(count) + ": " + i["name"])
            count =  count+1
        json.dump(simpleList, json_file, ensure_ascii=False, indent=2)
    with open('allCardRankP1SCAll.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortBySCP1)
        simpleList = []
        count = 1
        for i in finalList:
            simpleList.append(str(count) + ": " + i["name"])
            count =  count+1
        json.dump(simpleList, json_file, ensure_ascii=False, indent=2)