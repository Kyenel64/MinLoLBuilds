import requests
import logging
import cssutils

import ChampionList

cssutils.log.setLevel(logging.CRITICAL)

def RetrieveBuildURL():
    return "https://u.gg/lol/champions/blitzcrank/build" #Debug

    # Retrieve riot API information
    f = open(".config", "r")
    riotName = f.readline().replace('\n', '').replace(' ', '%20')
    tagline = f.readline().replace('\n', '')
    riotAPIKey = f.readline()
    f.close()

    accountData = requests.get("https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + riotName + "/" + tagline + "?api_key=" + riotAPIKey).json()
    riotPUUID = accountData['puuid']
    currentGameData = requests.get("https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/" + riotPUUID + "?api_key=" + riotAPIKey).json()
    if 'status' in currentGameData:
        assert currentGameData['status']['status_code'] != 404, "No running game found!"

    for participant in currentGameData['participants']:
        if (participant['puuid'] == riotPUUID):
            currentChampionID = participant['championId']
    currentChampionName = ChampionList.ChampionIDToName(currentChampionID)
    currentGameMode = currentGameData['gameMode']

    if (currentGameMode == "CLASSIC"):
        buildURL = "https://u.gg/lol/champions/" + currentChampionName + "/build"
    elif (currentGameMode == "ARAM"):
        buildURL = "https://u.gg/lol/champions/aram/" + currentChampionName + "-aram"

    return buildURL

# DEPENDS ON U.GG. Retrieves offset from spritesheet
def RetrieveXYOffset(divElement):
    i = divElement.find_all('div')[-1]['style']
    posStr = cssutils.parseStyle(i)['background-position']
    posStr = posStr.replace('px', '')
    posStr = posStr.replace('-', '')
    posStr = posStr.split(' ')
    posX = posStr[0]
    posY = posStr[1]
    return [int(posX), int(posY)]

# DEPENDS ON U.GG. Retrieves the spritesheet image index
def RetrieveSpriteSheetIndex(divElement):
    i = divElement.find_all('div')[-1]['style']
    posStr = cssutils.parseStyle(i)['background-image']
    fileName = posStr.split('/')[-1]
    fileName = fileName.replace(')', '')

    if (fileName == 'item0.webp'): return 0
    if (fileName == 'item1.webp'): return 1
    if (fileName == 'item2.webp'): return 2
    if (fileName == 'item3.webp'): return 3
    if (fileName == 'item4.webp'): return 4