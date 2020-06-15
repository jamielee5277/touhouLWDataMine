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
def sortByLwP2(item):
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
            level = levelType * 5
        if level > 10:
            level = 10
        if effects == None:
            return buffAmount
        if effects["subtype"] == 1 and  (effects["range"] == 1 or effects["range"] == 2):
            buffAmount["yang_buff"] = effects["level" + str(level) + "_add_value"]
        elif effects["subtype"] == 2 and (effects["range"] == 3 or effects["range"] == 4):
            buffAmount["yang_debuff"] = effects["level" + str(level) + "_add_value"]
        elif effects["subtype"] == 3 and (effects["range"] == 1 or effects["range"] == 2):
            buffAmount["yin_buff"] = effects["level" + str(level) + "_add_value"]
        elif effects["subtype"] == 4 and (effects["range"] == 3 or effects["range"] == 4):
            buffAmount["yin_debuff"] = effects["level" + str(level) + "_add_value"]
    return buffAmount

def getSpellCardDamage(key, yin_buff, yang_buff, yin_debuff, yang_debuff, unit, yin_boost, yang_boost):
    yin_attack = unit["yin_attack"]
    yang_attack = unit["yang_attack"]
    yin_buff_current = yin_buff
    yang_buff_current = yang_buff
    yin_debuff_current = yin_debuff
    yang_debuff_current = yang_debuff
    spellCard1 = unit["spellCard" + str(key)]
    if (spellCard1 == "Missing"):
        return "Missing"
    if (spellCard1["Special"] != "-"):
        for i in range(1, 4):
            spellEffectId = spellCard1["spellcard_skill" + str(i) + "_effect_id"]
            levelType = spellCard1["spellcard_skill" + str(i) + "_level_type"]
            levelValue = spellCard1["spellcard_skill" + str(i) + "_level_value"]
            timing = spellCard1["spellcard_skill" + str(i) + "_timing"]
            buff = getSpellBuffAmount(spellEffectId, levelType, levelValue, timing)
            yin_buff_current += buff["yin_buff"]
            yang_buff_current += buff["yang_buff"]
            yin_debuff_current += buff["yin_debuff"]
            yang_debuff_current += buff["yang_debuff"]
    
    damageMap = {}
    damageMap["P0"] = 0
    damageMap["P1"] = 0
    damageMap["P2"] = 0
    damageMap["P3"] = 0
    for i in range(0, 4):
        rawTotalDamage = 0
        yin_multiplier = (1.0 + 0.3 * min(yin_buff_current + yin_boost * i, 10)) * (1 + 0.3 * yin_debuff_current)
        yang_multiplier = (1.0 + 0.3 * min(yang_buff_current + yang_boost * i, 10)) * (1 + 0.3 * yang_debuff_current)
        for j in range(1, 7):
            bullet = spellCard1.get(str(j), None)
            if bullet == None:
                continue
            if bullet["boost"] <= i:
                rawDamage =  bullet["power"] * bullet["count"] * spellCard1["shot_level5_power_rate"]
                # not reliable, changing later
                if (bullet["description"][0] == "陽"):
                    rawDamage *= yang_multiplier * yang_attack
                else:
                    rawDamage *= yin_multiplier * yang_attack
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
    for i in range(1, 4):
        skill = unit["skill" + str(i)]
        if skill == "Missing":
            continue
        for j in range(1, 4):
            effects = skill.get("effect" + str(i), "Missing")
            if effects == "Missing":
                continue
            if effects["subtype"] == 1 and  (effects["range"] == 1 or effects["range"] == 2):
                buffAmount["yang_buff"] = effects["level" + str(level) + "_value"]
            elif effects["subtype"] == 2 and (effects["range"] == 3 or effects["range"] == 4):
                buffAmount["yang_debuff"] = effects["level" + str(level) + "_value"]
            elif effects["subtype"] == 3 and (effects["range"] == 1 or effects["range"] == 2):
                buffAmount["yin_buff"] = effects["level" + str(level) + "_value"]
            elif effects["subtype"] == 4 and (effects["range"] == 3 or effects["range"] == 4):
                buffAmount["yin_debuff"] = effects["level" + str(level) + "_value"]
    return buffAmount

def getPassiveBuff(ability):
    buffAmount = {}
    buffAmount["yin_buff"] = 0
    buffAmount["yang_buff"] = 0
    buffAmount["yin_debuff"] = 0
    buffAmount["yang_debuff"] = 0
    buffAmount["yang_boost"] = 0
    buffAmount["yin_boost"] = 0
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
        if effects["purge_barrier_diffusion_range"] == 0 or effects["purge_barrier_diffusion_range"] == 1:
            if effects["purge_barrier_diffusion_type"] == 1:
                buffAmount["yang_buff"] = 3
            elif effects["purge_barrier_diffusion_type"] == 3:
                buffAmount["yin_buff"] = 3
    return buffAmount

finalResult = {}
finalList = []
# 命中加成
# done by hardcoding now, need to automate later
specialIdYin = ["1003"]
specialIdYang = ["1010"]
with open('infoCompiled.json', encoding='utf-8') as json_file:
    units = json.load(json_file)
    for key in units.keys():
        unitResult = {}
        unit = units[key]
        buffAmount = getSkillBuff(unit)
        yin_buff = buffAmount["yin_buff"]
        yang_buff = buffAmount["yang_buff"]
        yin_debuff = buffAmount["yin_debuff"]
        yang_debuff = buffAmount["yang_debuff"]
        buffAmount = getPassiveBuff(unit["ability"])
        yin_buff += buffAmount["yin_buff"]
        yang_buff += buffAmount["yang_buff"]
        yin_debuff += buffAmount["yin_debuff"]
        yang_debuff += buffAmount["yang_debuff"]
        yin_boost = buffAmount["yin_boost"]
        yang_boost = buffAmount["yang_boost"]
        unitResult["name"] = unit["name"]
        if (key in specialIdYang):
            yang_buff += 3
        if (key in specialIdYin):
            yin_buff += 3
        unitResult["yin_buff"] = yin_buff
        unitResult["yang_buff"] = yang_buff
        unitResult["yin_debuff"] = yin_debuff
        unitResult["yang_debuff"] = yin_debuff
        unitResult["yin_boost"] = yin_boost
        unitResult["yang_boost"] = yang_boost
        unitResult["SpellCard1Damge"] = getSpellCardDamage(1, yin_buff, yang_buff, yin_debuff, yang_debuff, unit, yin_boost, yang_boost)
        unitResult["SpellCard2Damge"] = getSpellCardDamage(2, yin_buff, yang_buff, yin_debuff, yang_debuff, unit, yin_boost, yang_boost)
        unitResult["LastWordDamage"] = getSpellCardDamage(5, yin_buff, yang_buff, yin_debuff, yang_debuff, unit, yin_boost, yang_boost)
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
    with open('damageP2.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortByLwP2)
        json.dump(finalList, json_file, ensure_ascii=False, indent=2)
    with open('damageP3.json', 'w', encoding='utf-8') as json_file:
        finalList.sort(reverse=True, key=sortByLwP3)
        json.dump(finalList, json_file, ensure_ascii=False, indent=2)