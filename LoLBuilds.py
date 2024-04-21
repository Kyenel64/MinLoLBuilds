import requests
from tkinter import *
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
import cssutils
import selenium

overlayMode = False
opacity = 1
imgSize = 20
xPadding = imgSize / 3

root = Tk()
root.overrideredirect(overlayMode)
root.attributes('-alpha', opacity)
root.update()

req = requests.get("https://u.gg/lol/champions/gragas/build")
soup = BeautifulSoup(req.content, 'html.parser')

spriteSheets = [ Image.open("item0.webp"), 0, Image.open("item2.webp"), Image.open("item3.webp"), Image.open("item4.webp") ]
starterItemsTkImage = [0] * 3
coreItemsTkImage = [0] * 3
fourthItemOptionsTkImage = [0] * 3
fifthItemOptionsTkImage = [0] * 3
sixthItemOptionsTkImage = [0] * 3

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


def DrawItemSet(className):
    startingItems = soup.find('div', class_=className)
    items = startingItems.find_all('div', {'class': 'item-img'})

    for index, item in enumerate(items):
        offset = RetrieveXYOffset(item)
        spriteSheetIndex = RetrieveSpriteSheetIndex(item)
        img = spriteSheets[spriteSheetIndex].crop((offset[0], offset[1], offset[0] + 48, offset[1] + 48)) #48 is size of each sprite
        img = img.resize((imgSize, imgSize), Image.Resampling.LANCZOS)
        
        if (className == 'content-section_content starting-items'): 
            starterItemsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = starterItemsTkImage[index])
            panel.grid(row = 0, column = index)

        elif (className == 'core-items'): 
            coreItemsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = coreItemsTkImage[index])
            pad = 0
            if (index == 2):
                pad = xPadding
            panel.grid(row = 1, column = index, padx=(0, pad))
        elif (className == 'content-section_content item-options item-options-1'): 
            fourthItemOptionsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = fourthItemOptionsTkImage[index])
            panel.grid(row = index, column = 4)
        elif (className == 'content-section_content item-options item-options-2'): 
            fifthItemOptionsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = fifthItemOptionsTkImage[index])
            panel.grid(row = index, column = 5)
        elif (className == 'content-section_content item-options item-options-3'): 
            sixthItemOptionsTkImage[index] = ImageTk.PhotoImage(img)
            panel = Label(root, image = sixthItemOptionsTkImage[index])
            panel.grid(row = index, column = 6)
        #panel.pack(side = LEFT)


def main():
    DrawItemSet('content-section_content starting-items')
    DrawItemSet('core-items')
    DrawItemSet('content-section_content item-options item-options-1')
    DrawItemSet('content-section_content item-options item-options-2')
    DrawItemSet('content-section_content item-options item-options-3')

    root.mainloop()

if __name__ == "__main__":
    main()