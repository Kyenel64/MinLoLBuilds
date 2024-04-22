import requests
from tkinter import *
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
import os
import json

import LoL

# Create .config file if it does not exist
if not os.path.isfile(".config"):
    jsonData = { "RiotName": "", "RiotTag": "", "RiotAPIKey": "", "OverlayMode": True, "Opacity": 0.5, "ItemSize": 30 }
    jsonData["RiotName"] = input("Riot name: ")
    jsonData["RiotTag"] = input("Riot tag: ")
    jsonData["RiotAPIKey"] = input("Riot API Key: ")
    with open(".config", "w") as out:
        json.dump(jsonData, out, indent=4)

# Set Configurations
f = open(".config")
config = json.load(f)
overlayMode = config["OverlayMode"]
opacity = config["Opacity"]
imgSize = config["ItemSize"]

url = LoL.RetrieveBuildURL(config)
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")

# Initialize Tkinter
root = Tk()
root.overrideredirect(overlayMode)
root.attributes("-alpha", opacity)
root.attributes("-topmost", True)
screenHeight = root.winfo_screenheight()
root.geometry("+%d+%d"%(0,screenHeight - (imgSize * 3)))
root.configure(background="black")

imageSheets = [ Image.open("Images/item0.webp"), 0, Image.open("Images/item2.webp"), Image.open("Images/item3.webp"), Image.open("Images/item4.webp") ]
starterItemsTkImage = [0] * 3
coreItemsTkImage = [0] * 3
fourthItemOptionsTkImage = [0] * 3
fifthItemOptionsTkImage = [0] * 3
sixthItemOptionsTkImage = [0] * 3


def DrawItemSet(className):
    startingItems = soup.find("div", class_=className)
    items = startingItems.find_all("div", {"class": "item-img"})

    for index, item in enumerate(items):
        offset = LoL.RetrieveXYOffset(item)
        spriteSheetIndex = LoL.RetrieveSpriteSheetIndex(item)
        img = imageSheets[spriteSheetIndex].crop((offset[0], offset[1], offset[0] + 48, offset[1] + 48)) #48 is size of each sprite
        img = img.resize((imgSize, imgSize), Image.Resampling.LANCZOS)
        
        if (className == "content-section_content starting-items"): 
            starterItemsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = starterItemsTkImage[index], borderwidth=0)
            panel.grid(row = index, column = 0)

        elif (className == "core-items"): 
            coreItemsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = coreItemsTkImage[index], borderwidth=0)
            panel.grid(row = index, column = 1, padx=(0, 10))
        elif (className == "content-section_content item-options item-options-1"): 
            fourthItemOptionsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = fourthItemOptionsTkImage[index], borderwidth=0)
            panel.grid(row = index, column = 2)
        elif (className == "content-section_content item-options item-options-2"): 
            fifthItemOptionsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = fifthItemOptionsTkImage[index], borderwidth=0)
            panel.grid(row = index, column = 3)
        elif (className == "content-section_content item-options item-options-3"): 
            sixthItemOptionsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = sixthItemOptionsTkImage[index], borderwidth=0)
            panel.grid(row = index, column = 4)



def main():
    DrawItemSet("content-section_content starting-items")
    DrawItemSet("core-items")
    DrawItemSet("content-section_content item-options item-options-1")
    DrawItemSet("content-section_content item-options item-options-2")
    DrawItemSet("content-section_content item-options item-options-3")

    root.mainloop()

if __name__ == "__main__":
    main()