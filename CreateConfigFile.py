import os
import json

if not os.path.isfile(os.getcwd() + "/.config"):
    jsonData = { "RiotName": "", "RiotTag": "", "OverlayMode": True, "Opacity": 0.5, "ItemSize": 30 }
    jsonData["RiotName"] = input("Riot name: ")
    jsonData["RiotTag"] = input("Riot tag: ")
    with open(os.getcwd() + "/.config", "w") as out:
        json.dump(jsonData, out, indent=4)
    input("Completed setup. Press any key to exit.")
    