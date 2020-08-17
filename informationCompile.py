#coding=utf-8
import os
import json
import sys

masterResult = {}

elementMap = {
    0: "属性なし",
    1: "日属性",
    2: "月属性",
    3: "火属性",
    4: "水属性",
    5: "木属性",
    6: "金属性",
    7: "土属性",
    8: "星属性",
}

def getCharacteristic(id):
    with open('CharacteristicMaster.json', encoding='utf-8') as characteristic_json:
        characteristics = json.load(characteristic_json)
        characteristic = characteristics[str(id)]
        # Assuming the description is correct, all the remaining is not needed
        del characteristic["characteristic1_icon_filename"]
        del characteristic["characteristic2_icon_filename"]
        del characteristic["characteristic3_icon_filename"]
        del characteristic["characteristic1_effect_subtype"]
        del characteristic["characteristic2_effect_subtype"]
        del characteristic["characteristic3_effect_subtype"]
        del characteristic["characteristic1_effect_type"]
        del characteristic["characteristic2_effect_type"]
        del characteristic["characteristic3_effect_type"]
        del characteristic["characteristic1_effect_value"]
        del characteristic["characteristic2_effect_value"]
        del characteristic["characteristic3_effect_value"]
        del characteristic["characteristic1_rate"]
        del characteristic["characteristic2_rate"]
        del characteristic["characteristic3_rate"]
        del characteristic["characteristic1_type"]
        del characteristic["characteristic2_type"]
        del characteristic["characteristic3_type"]
        del characteristic["trust_characteristic_avent_effect_subtype"]
        del characteristic["trust_characteristic_avent_effect_type"]
        del characteristic["trust_characteristic_rear_effect_subtype"]
        del characteristic["trust_characteristic_rear_effect_type"]
        return characteristic

def getAbility(id):
    with open('AbilityMaster.json', encoding='utf-8') as ability_json:
        abilities = json.load(ability_json)
        ability = abilities[str(id)]
        # Assuming the description is correct, all the remaining is not needed
        del ability["blackout_barrier_type"]
        del ability["boost_power_divergence_range"]
        del ability["boost_power_divergence_type"]
        del ability["burning_barrier_type"]
        del ability["electrified_barrier_type"]
        del ability["frozen_barrier_type"]
        del ability["good_element_give_damage_rate"]
        del ability["good_element_give_damage_ratef"]
        del ability["good_element_take_damage_rate"]
        del ability["good_element_take_damage_ratef"]
        # del ability["id"]
        del ability["poisoning_barrier_type"]
        del ability["purge_barrier_diffusion_range"]
        del ability["purge_barrier_diffusion_type"]
        del ability["weak_element_give_damage_rate"]
        del ability["weak_element_give_damage_ratef"]
        del ability["weak_element_take_damage_rate"]
        del ability["weak_element_take_damage_ratef"]
        return ability

def getResist(id):
    with open('ResistMaster.json', encoding='utf-8') as resist_json:
        weakElement = []
        goodElement = []
        # Too lazy to use map, hard coding here
        resist = json.load(resist_json)[str(id)]
        if (resist["element1_resistance"] == 0):
            weakElement.append("日")
        if (resist["element1_resistance"] == 2):
            goodElement.append("日")
        if (resist["element2_resistance"] == 0):
            weakElement.append("月")
        if (resist["element2_resistance"] == 2):
            goodElement.append("月")
        if (resist["element3_resistance"] == 0):
            weakElement.append("火")
        if (resist["element3_resistance"] == 2):
            goodElement.append("火")
        if (resist["element4_resistance"] == 0):
            weakElement.append("水")
        if (resist["element4_resistance"] == 2):
            goodElement.append("水")
        if (resist["element5_resistance"] == 0):
            weakElement.append("木")
        if (resist["element5_resistance"] == 2):
            goodElement.append("木")
        if (resist["element6_resistance"] == 0):
            weakElement.append("金")
        if (resist["element6_resistance"] == 2):
            goodElement.append("金")
        if (resist["element7_resistance"] == 0):
            weakElement.append("土")
        if (resist["element7_resistance"] == 2):
            goodElement.append("土")
        if (resist["element8_resistance"] == 0):
            weakElement.append("星")
        if (resist["element8_resistance"] == 2):
            goodElement.append("星")
        resist["Good"] = goodElement
        resist["Weak"] = weakElement
        del resist["element1_resistance"]
        del resist["element2_resistance"]
        del resist["element3_resistance"]
        del resist["element4_resistance"]
        del resist["element5_resistance"]
        del resist["element6_resistance"]
        del resist["element7_resistance"]
        del resist["element8_resistance"]
        del resist["id"]
        return resist
def getRole(id):
    roleMap = {
        1:"防御式",
        2:"支援式",
        3:"回復式",
        4:"妨害式",
        5:"攻撃式",
        6:"技巧式",
        7:"速攻式",
        8:"破壊式",
    }
    return roleMap[id]

def getBullet(id):
    with open('BulletMaster.json', encoding='utf-8') as bullet_json:
        bullet = json.load(bullet_json).get(str(id), "Missing")
        if bullet == "Missing":
            return bullet
        for i in range(1, 4):
            if bullet["bullet" + str(i) + "_addon_id"] == 0:
                del bullet["bullet" + str(i) + "_addon_id"]
                del bullet["bullet" + str(i) + "_addon_value"]
            if bullet["bullet" + str(i) + "_extraeffect_id"] == 0:
                del bullet["bullet" + str(i) + "_extraeffect_id"]
                del bullet["bullet" + str(i) + "_extraeffect_success_rate"]
        # Assuming the description is correct
        # del bullet["bullet1_addon_id"]
        # del bullet["bullet1_addon_value"]
        # del bullet["bullet1_extraeffect_id"]
        # del bullet["bullet1_extraeffect_success_rate"]
        # del bullet["bullet2_addon_id"]
        # del bullet["bullet2_addon_value"]
        # del bullet["bullet2_extraeffect_id"]
        # del bullet["bullet2_extraeffect_success_rate"]
        # del bullet["bullet3_addon_id"]
        # del bullet["bullet3_addon_value"]
        # del bullet["bullet3_extraeffect_id"]
        # del bullet["bullet3_extraeffect_success_rate"]
        # del bullet["category"]
        # del bullet["element"]
        # del bullet["type"]
        # del bullet["power"]
        # del bullet["id"]
        return bullet

def getShot(id):
    with open('ShotMaster.json', encoding='utf-8') as shot_json:
        finalShot = {}
        shot = json.load(shot_json).get(str(id), None)
        if shot == None:
            return "Missing"
        finalShot["description"] = shot["description"]
        finalShot["name"] = shot["name"]
        finalShot["id"] = shot["id"]
        finalShot["Special"] = shot["specification"]
        finalShot["phantasm_power_up_rate"] = shot["phantasm_power_up_rate"]
        finalShot["shot_level0_power_rate"] = shot["shot_level0_power_rate"]
        finalShot["shot_level1_power_rate"] = shot["shot_level1_power_rate"]
        finalShot["shot_level2_power_rate"] = shot["shot_level2_power_rate"]
        finalShot["shot_level3_power_rate"] = shot["shot_level3_power_rate"]
        finalShot["shot_level4_power_rate"] = shot["shot_level4_power_rate"]
        finalShot["shot_level5_power_rate"] = shot["shot_level5_power_rate"]
        for i in range(6):
            bullet = getBullet(shot["magazine" + str(i)+ "_bullet_id"])
            shotLine = bullet
            shotLine["description"] = bullet["description"]
            shotLine["range"] = shot["magazine" + str(i) +"_bullet_range"]
            shotLine["name"] = bullet["name"]
            shotLine["hit_rate"] = bullet["hit"]
            shotLine["power"] = shot.get("magazine" + str(i) + "_bullet_power_ratef", shot.get("magazine" + str(i) + "_bullet_power_rate")/100)
            shotLine["count"] = shot["magazine" + str(i) + "_bullet_value"]
            shotLine["boost"] = shot.get("magazine" + str(i) + "_boost_count", 0)
            finalShot[str(i + 1)] = shotLine
        return finalShot

def getSpellCard(id):
    with open('SpellcardMaster.json', encoding='utf-8') as shot_json:
        finalShot = {}
        shot = json.load(shot_json).get(str(id), None)
        if shot == None:
            return "Missing"
        finalShot["description"] = shot["description"]
        finalShot["id"] = shot["id"]
        finalShot["name"] = shot["name"]
        finalShot["Special"] = shot["specification"]
        finalShot["phantasm_power_up_rate"] = shot["phantasm_power_up_rate"]
        finalShot["shot_level0_power_rate"] = shot["shot_level0_power_rate"]
        finalShot["shot_level1_power_rate"] = shot["shot_level1_power_rate"]
        finalShot["shot_level2_power_rate"] = shot["shot_level2_power_rate"]
        finalShot["shot_level3_power_rate"] = shot["shot_level3_power_rate"]
        finalShot["shot_level4_power_rate"] = shot["shot_level4_power_rate"]
        finalShot["shot_level5_power_rate"] = shot["shot_level5_power_rate"]
        for x in range(1, 6):
            if shot["spellcard_skill" + str(x) +"_effect_id"] != 0:
                skill = {}
                skill["spellcard_skill" + str(x) +"_effect_id"] = shot["spellcard_skill" + str(x) +"_effect_id"]
                skill["spellcard_skill" + str(x) +"_level_type"] = shot["spellcard_skill" + str(x) +"_level_type"]
                skill["spellcard_skill" + str(x) +"_timing"] = shot["spellcard_skill" + str(x) +"_timing"]
                skill["spellcard_skill" + str(x) +"_level_value"] = shot["spellcard_skill" + str(x) +"_level_value"]
                skill["effect"] = getSkillEffect(shot["spellcard_skill" + str(x) +"_effect_id"])
                finalShot["spellcard_skill" + str(x)] = skill
        for i in range(6):
            bullet = getBullet(shot["magazine" + str(i)+ "_bullet_id"])
            if bullet =="Missing":
                continue
            shotLine = bullet
            shotLine["range"] = shot["magazine" + str(i) +"_bullet_range"]
            shotLine["hit_rate"] = bullet["hit"]
            del shotLine["hit"]
            shotLine["power"] = shot.get("magazine" + str(i) + "_bullet_power_ratef", shot.get("magazine" + str(i) + "_bullet_power_rate")/100)
            shotLine["count"] = shot["magazine" + str(i) + "_bullet_value"]
            shotLine["boost"] = shot.get("magazine" + str(i) + "_boost_count", 0)
            finalShot[str(i + 1)] = shotLine
        return finalShot

def getSkillEffect(id):
    with open('SkillEffectMaster.json', encoding='utf-8') as skill_json:
        skill = json.load(skill_json).get(str(id), "Missing")
        if skill == "Missing":
            return skill
        return skill

def getSkill(id):
    with open('SkillMaster.json', encoding='utf-8') as skill_json:
        skill = json.load(skill_json).get(str(id), "Missing")
        if skill == "Missing":
            return skill
        skill.pop("icon_filename", None)
        del skill["exp_id"]
        skill["effect1"] = getSkillEffect(skill["effect1_id"])
        skill["effect2"] = getSkillEffect(skill["effect2_id"])
        skill["effect3"] = getSkillEffect(skill["effect3_id"])
        return skill

with open('unitMaster.json', encoding='utf-8') as json_file:
    unit = json.load(json_file)
    for key in unit.keys():
        person = unit[key]
        masterResult[key] = person
        # Power calculation
        person["total_power"] = person["life_point"]*0.2 + person["speed"] + person["yang_attack"] + person["yin_attack"] + person["yang_defense"] + person["yin_defense"]
        # Process ability
        person["ability"] = getAbility(person["ability_id"])
        del person["ability_id"]
        del person["album_id"]
        # Process characteristic
        person["characteristic"] = getCharacteristic(person["characteristic_id"])
        del person["characteristic_id"]
        del person["default_costume_id"]
        del person["exp_id"]
        del person["id"]
        del person["person_id"]
        del person["recycle_id"]
        # Process resistance
        person["resist"] = getResist(person["resist_id"])
        del person["resist_id"]
        # Process role
        person["role"] = getRole(person["role"])
        masterResult[key] = person
        person["shot1"] = getShot(person["shot1_id"])
        person["shot2"] = getShot(person["shot2_id"])
        del person["shot1_id"]
        del person["shot2_id"]
        person["spellCard1"] = getSpellCard(person["spellcard1_id"])
        person["spellCard2"] = getSpellCard(person["spellcard2_id"])
        # person["spellCard3"] = getSpellCard(person["spellcard3_id"])
        # person["spellCard4"] = getSpellCard(person["spellcard4_id"])
        person["spellCard5"] = getSpellCard(person["spellcard5_id"])
        del person["spellcard1_id"]
        del person["spellcard2_id"]
        del person["spellcard3_id"]
        del person["spellcard4_id"]
        del person["spellcard5_id"]
        person["skill1"] = getSkill(person["skill1_id"])
        person["skill2"] = getSkill(person["skill2_id"])
        person["skill3"] = getSkill(person["skill3_id"])
        del person["skill1_id"]
        del person["skill2_id"]
        del person["skill3_id"]

    print(masterResult)
    with open('infoCompiled.json', 'w', encoding='utf-8') as json_file:
        json.dump(masterResult, json_file, ensure_ascii=False, indent=2)