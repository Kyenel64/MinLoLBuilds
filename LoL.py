### This file depends on u.gg and must be updated if there are changes to the website which breaks the program.
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging
import cssutils
import time

cssutils.log.setLevel(logging.CRITICAL)

MAX_URL_LOAD_ATTEMPTS = 10

def RetrieveBuildURL(config):
    userURL = config.RiotName.replace(" ", "%20") + "-" + config.RiotTag.replace("#", "")
    url = "https://u.gg/lol/profile/na1/" + userURL + "/live-game"
    return url

# Retrieves offset within spritesheet
def RetrieveXYOffset(divElement):
    i = divElement.find_all("div")[-1]["style"]
    posStr = cssutils.parseStyle(i)["background-position"]
    posStr = posStr.replace("px", "")
    posStr = posStr.replace("-", "")
    posStr = posStr.split(" ")
    posX = posStr[0]
    posY = posStr[1]
    return [int(posX), int(posY)]

# Retrieves the spritesheet image index
def RetrieveSpriteSheetIndex(divElement):
    i = divElement.find_all("div")[-1]["style"]
    posStr = cssutils.parseStyle(i)["background-image"]
    fileName = posStr.split("/")[-1]
    fileName = fileName.replace(")", "")

    if (fileName == "item0.webp"): return 0
    if (fileName == "item1.webp"): return 1
    if (fileName == "item2.webp"): return 2
    if (fileName == "item3.webp"): return 3
    if (fileName == "item4.webp"): return 4

# Returns the recommended build json data from u.gg
def RetrieveRecommendedBuild(url):
    chromeOptions = Options()  
    chromeOptions.add_argument("--headless") # Opens the browser up in background
    with Chrome(options=chromeOptions) as browser:
        browser.get(url)
        for i in range(MAX_URL_LOAD_ATTEMPTS):
            time.sleep(2)
            html = browser.page_source
            soup = BeautifulSoup(html, "html.parser")
            if soup.find_all("div", { "class":"champion-recommended-build" }):
                print("Found live game!")
                return soup.find_all("div", { "class":"champion-recommended-build" })[0]