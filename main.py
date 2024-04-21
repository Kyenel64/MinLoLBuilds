import requests
from tkinter import *
from PIL import ImageTk, Image
from bs4 import BeautifulSoup

import LoL

# GUI Configurations
overlayMode = True
opacity = 0.5
imgSize = 30
xPadding = imgSize / 3


url = LoL.RetrieveBuildURL()
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

# Initialize Tkinter
root = Tk()
root.overrideredirect(overlayMode)
root.attributes('-alpha', opacity)
root.attributes('-topmost', True)
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.geometry('+%d+%d'%(0,screenHeight - (imgSize * 3) - 10))
root.update()

imageSheets = [ Image.open("Images/item0.webp"), 0, Image.open("Images/item2.webp"), Image.open("Images/item3.webp"), Image.open("Images/item4.webp") ]
starterItemsTkImage = [0] * 3
coreItemsTkImage = [0] * 3
fourthItemOptionsTkImage = [0] * 3
fifthItemOptionsTkImage = [0] * 3
sixthItemOptionsTkImage = [0] * 3


def DrawItemSet(className):
    startingItems = soup.find('div', class_=className)
    items = startingItems.find_all('div', {'class': 'item-img'})

    for index, item in enumerate(items):
        offset = LoL.RetrieveXYOffset(item)
        spriteSheetIndex = LoL.RetrieveSpriteSheetIndex(item)
        img = imageSheets[spriteSheetIndex].crop((offset[0], offset[1], offset[0] + 48, offset[1] + 48)) #48 is size of each sprite
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


def main():
    DrawItemSet('content-section_content starting-items')
    DrawItemSet('core-items')
    DrawItemSet('content-section_content item-options item-options-1')
    DrawItemSet('content-section_content item-options item-options-2')
    DrawItemSet('content-section_content item-options item-options-3')

    root.mainloop()

if __name__ == "__main__":
    main()