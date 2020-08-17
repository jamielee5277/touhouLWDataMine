# touhouLWDataMine
touhou lostword datamining scripts

Usage: unpack the eastreg.ini, get the manifest url and pass it in as parameter (without manifest.json part) to getBytes.py. It will download the bytes to the local directory. Then use touhoulw_bytestojson.py to decode to json files (credit to ThTsOd from QQ group). Use informationCompile after to group it to aggregate to a big json file (note that this script is not optimized, so it can take a while to complete). To convert to csv format, use writeWiki.py (pre req: have ran informationCompile and rankCompile). To calculate damage, use damageCalculation.py (this file have bunch of hard coded values for Picture, not yet automated).
