import re
from collections import defaultdict
import json

obj = []

sleeveTypes = {}
skus = {}
with open('skus.csv', 'r') as sizes:
    for line in sizes:
        name, sku, premSku, width, height, price, link, premiumLink = line.split(',')[:8]
        skus[sku] = {"name": name, "sku": sku, "premSku": premSku, "width": width, "height": height, "link": link, "premiumLink": premiumLink.strip()}
arr = []
for key in skus:
    arr.append(skus[key])

arr.sort(key=lambda x: len(x["premiumLink"]), reverse=True)
with open("skus.json", 'w') as skuFile:
        skuFile.write(json.dumps(arr))


def recognize(size):
    for sku in skus:
        if sku in size:
            return sku
    return "UNKNOWN"
regex = r"\([^)]*(card|sheets)[^)]*\)|\(\s*(Large|Small)[^)]*\)|large cards*|small cards|(\s*Square\s*)|Square cards|(Square Tiles)"

def findRealName(name):
    return re.sub(regex, "", name, flags=re.IGNORECASE).strip().replace("©", ",")
    
matchedSleeves = defaultdict(list)
priority = defaultdict(lambda: float('-inf'))

with open('sleeves.csv', 'r', encoding="utf8") as ifile:
    lines = ifile.read().splitlines()
    for index, line in enumerate(lines[::-1]):
        name, count, width, length, sleeveType, = line.split(',')[:5]
        cName = findRealName(name)
        sku = recognize(sleeveType)
        sleeve = {"name": cName, "count": count, "width": width, "height": length, "sku":sku, "nameLower": cName.lower(), "priority": index}
        # print(cName)
        if not cName:
            continue
        if len(cName) == 1:
            continue
        toAddTo = matchedSleeves[cName]
        hasMatch = False
        for existing in toAddTo:
            if existing['sku'] != "UNKNOWN" and existing['sku'] == sku:
                hasMatch = True
                break
        if hasMatch:
            continue 
        toAddTo.append(sleeve)

matchedSleeves
with open('output.json', 'w') as output:
    output.write(json.dumps(matchedSleeves))

msf = 0
bssf = ""
for name in matchedSleeves:
    val = matchedSleeves[name]
    num = len(list(filter(lambda x : x['sku'] != "UNKNOWN", val)))
    if num > msf:
        msf = num
        bssf = name

print(bssf)

for x in sleeveTypes:
    print(x)