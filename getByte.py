import urllib.request
import json
import sys

manifest = "manifest.json"

if len(sys.argv) < 2:
    print("Please provide base url as program argument")
    exit()
uri = sys.argv[1]

with urllib.request.urlopen(uri + manifest) as f:
    info = json.load(f)["AssetInfos"]
    for item in info:
        urllib.request.urlretrieve(uri + item["Name"], "./" + item['AssetPaths'][0].split("/")[-1])