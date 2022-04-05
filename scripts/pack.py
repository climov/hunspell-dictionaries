#!/usr/bin/env python3

import argparse
import csv
import json
import os.path

# Reads the variants.csv file and outputs a tuple of 3 dictionaries: (variants, languages, packs)
def readVariants(varCsv):
    with open(varCsv, newline='', encoding='utf-8') as csvVariants:
        variantsReader = csv.reader(csvVariants)
        header = []
        variants = {}
        variantNameSet = set()
        languages = {}
        packs = {}
        rowNum = 0
        for row in variantsReader:
            if (rowNum == 0):
                pass
            elif (rowNum == 1):
                header = row
            else:
                colNum = 0
                variant = {}
                for val in row:
                    variant[header[colNum]] = val
                    colNum += 1
                if variant['variantID'] in variants:
                    raise "Duplicate language variant: " + variant['variantID']
                if variant['stems'] != '':
                    variant['dictType'] = 'hs'
                else:
                    variant['dictType'] = ''
                variant['isDefault'] = (variant['isDefault'] == "y")
                variants[variant['variantID']] = variant
                # variantName should be unique
                if variant['variantFullName'] in variantNameSet:
                    raise "Duplicate language variant name: " + variant['variantFullName']
                variantNameSet.add(variant['variantFullName'])
                language = {}
                language['name'] = variant['languageName']
                language['id'] = variant['languageID']
                language['qlanguage'] = variant['qlanguage']
                language['defaultVariant'] = ""
                language['variants'] = [variant['variantID']]
                if language['id'] in languages:
                    languages[language['id']]['variants'] += [variant['variantID']]
                else:
                    languages[language['id']] = language
                if variant['isDefault']:
                    if languages[language['id']]['defaultVariant'] != "":
                        raise "Language has two variants: " + variant['variantID'] + " and: " + languages[language['id']]['defaultVariant']
                    languages[language['id']]['defaultVariant'] = variant['variantID']
                languages[language['id']]
                if variant['pack'] not in packs:
                    packs[variant['pack']] = []
                packs[variant['pack']] += [variant['variantID']]
                #print(json.dumps(variant, indent=4))
            rowNum += 1
        #print(json.dumps(variants, indent=4))
        for langId, lang in languages.items():
            if lang['defaultVariant'] == "":
                raise Exception("Language is missing a default variant:" + lang['name'])
        return (variants, languages, packs)

# Reads the presets.csv file and outputs a tuple of 2 dictionaries: (presets, presetsByScript)
def readPresets(presCsv):
    with open(presCsv, newline='', encoding='utf-8') as csvPresets:
        presetsReader = csv.reader(csvPresets)
        header = []
        presets = {}
        presetsByScript = {}
        rowNum = 0
        for row in presetsReader:
            if (rowNum == 0):
                pass
            elif (rowNum == 1):
                header = row
            else:
                colNum = 0
                preset = {}
                for val in row:
                    preset[header[colNum]] = val
                    colNum += 1
                if preset['id'] in presets:
                    raise "Duplicate preset: " + preset['id']
                presets[preset['id']] = preset
                if preset['qscript'] not in presetsByScript:
                    presetsByScript[preset['qscript']] = []
                presetsByScript[preset['qscript']] += [preset['id']]
                #print(json.dumps(preset, indent=4))
            rowNum += 1
        return (presets, presetsByScript)

# For each variant, check if it has a dictionary and create the .meta.json file for it
def createMetaForDictionaries(variants, dictsDir):
    for k, v in variants.items():
        if v["description"] == "":
            del v["description"]
        dirPath = dictsDir + "/" + k
        if os.path.isdir(dirPath):
            path = dirPath + "/" + k + ".meta.json"
            with open(path, 'w', encoding='utf-8') as vout:
                json.dump(v, vout, indent=4, ensure_ascii=False)

def createMetaForPacks(variants, languages, packs, presets, presetsByScript, packsDir):
    basicPresets = set()
    basicFonts = set()
    for variantId in packs['basic']:
        basicScript = variants[variantId]['qscript']
        for basicPreset in presetsByScript[basicScript]:
            basicPresets.add(basicPreset)
            preset = presets[basicPreset]
            basicFonts.add(preset['typewriterFont'])
            basicFonts.add(preset['serifFont'])
            basicFonts.add(preset['sansFont'])
            basicFonts.add(preset['titleFont'])
            if preset['additionalFonts'] != '':
                for font in preset['additionalFonts'].split(','):
                    basicFonts.add(font.strip())
    #print(basicPresets)
    #print(basicFonts)
    for pack, packVariants in packs.items():
        #print(pack)
        packDir = packsDir + "/" + pack
        manifest = packDir + "/packmanifest.json"
        #print(manifest)
        packJson = {}
        packJson['active'] = True
        isBasic = (pack == 'basic')
        packJson['preinstalled'] = isBasic
        packJson['languages'] = []
        variantsByLang = {}
        for variantId in packVariants:
            langId = variants[variantId]['languageID']
            if langId not in variantsByLang:
                variantsByLang[langId] = []
            variantsByLang[langId] += [variantId]
        packScripts = set()
        for langId, variantIds in variantsByLang.items():
            lang = {}
            lang['name'] = languages[langId]['name']
            lang['id'] =langId
            lang['qlanguage'] = languages[langId]['qlanguage']
            lang['defaultVariant'] = languages[langId]['defaultVariant']
            lang['variants'] = []
            for variantId in variantIds:
                variant = {}
                variant['name'] = variants[variantId]['variantName']
                variant['id'] = variantId
                #variant['fullName'] = variants[variantId]['variantFullName']
                variant['defaultPreset'] = variants[variantId]['defaultPreset']
                variant['qscript'] = variants[variantId]['qscript']
                variant['qcountry'] = variants[variantId]['qcountry']
                variant['dictType'] = variants[variantId]['dictType']
                if 'description' in variants[variantId]:
                    variant['description'] = variants[variantId]['description']
                lang['variants'] += [variant]
                packScripts.add(variant['qscript'])
            lang['variants'].sort(key = lambda variant: variant['name'])
            if lang['name'] != '':
                packJson['languages'] += [lang]
        packJson['languages'].sort(key = lambda lang: lang['name'])
        packJson['presets'] = []
        packJson['fonts'] = set()
        for packScript in packScripts:
            for packPreset in presetsByScript[packScript]:
                preset = presets[packPreset].copy()
                if preset['description'] == '':
                    del preset['description']
                packJson['fonts'].add(preset['typewriterFont'])
                packJson['fonts'].add(preset['serifFont'])
                packJson['fonts'].add(preset['sansFont'])
                packJson['fonts'].add(preset['titleFont'])
                if preset['additionalFonts'] != '':
                    for font in preset['additionalFonts'].split(','):
                        packJson['fonts'].add(font.strip())
                del preset['additionalFonts']
                if preset['name'] != '' and (isBasic or preset['id'] not in basicPresets):
                    packJson['presets'] += [preset]
        if not isBasic:
            packJson['fonts'] -= basicFonts
        packJson['fonts'] = sorted(list(packJson['fonts']))
        packJson['presets'] = sorted(list(packJson['presets']), key = lambda preset: preset['id'])
        #print(json.dumps(packJson, indent=4))
        with open(manifest, 'w', encoding='utf-8') as pout:
            json.dump(packJson, pout, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--variants", type=str, required=True, help="The variants csv table")
    parser.add_argument("--presets",  type=str, required=True, help="The presets csv table")
    parser.add_argument("--dicts",    type=str, required=True, help="The folder containing the dictionaries")
    parser.add_argument("--packs",    type=str, required=True, help="The folder containing the packs")
    args = parser.parse_args()

    (variants, languages, packs) = readVariants(args.variants)
    #print(json.dumps(variants, indent=4))
    #print(json.dumps(languages, indent=4))
    #print(json.dumps(packs, indent=4))
    
    (presets, presetsByScript) = readPresets(args.presets)
    #print(json.dumps(presets, indent=4))
    #print(json.dumps(presetsByScript, indent=4))
    
    createMetaForDictionaries(variants, args.dicts)
    #print(json.dumps(packs, indent=4))
    createMetaForPacks(variants, languages, packs, presets, presetsByScript, args.packs)
