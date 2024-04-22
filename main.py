import os
import json

import LoL
import Window

class Configuration:
    RiotName: str
    RiotTag: str
    OverlayMode: bool
    Opacity: int
    ItemSize: int

# Populate config data
def ParseConfigFile():
    config = Configuration()
    f = open(".config")
    configJson = json.load(f)
    config.RiotName = configJson["RiotName"]
    config.RiotTag = configJson["RiotTag"]
    config.OverlayMode = configJson["OverlayMode"]
    config.Opacity = configJson["Opacity"]
    config.ItemSize = configJson["ItemSize"]
    return config


def main():
    config = ParseConfigFile()

    url = LoL.RetrieveBuildURL(config)
    recBuildJSON = LoL.RetrieveRecommendedBuild(url)

    window = Window.Window(config)

    window.DrawItemSet(recBuildJSON, "starting-items")
    window.DrawItemSet(recBuildJSON, "core-items")
    window.DrawItemSet(recBuildJSON, "item-options-1")
    window.DrawItemSet(recBuildJSON, "item-options-2")
    window.DrawItemSet(recBuildJSON, "item-options-3")

    window.Loop()

if __name__ == "__main__":
    main()