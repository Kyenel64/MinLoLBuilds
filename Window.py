from tkinter import *
from PIL import ImageTk, Image

import LoL

class Window:
    def __init__(self, config):
        self.root = Tk()
        self.config = config
        self.imageSheets = [ Image.open("Images/item0.webp"), 0, Image.open("Images/item2.webp"), Image.open("Images/item3.webp"), Image.open("Images/item4.webp") ]
        self.starterItemsTkImage = [0] * 3
        self.coreItemsTkImage = [0] * 3
        self.fourthItemOptionsTkImage = [0] * 3
        self.fifthItemOptionsTkImage = [0] * 3
        self.sixthItemOptionsTkImage = [0] * 3

        self.root.overrideredirect(config.OverlayMode)
        self.root.attributes("-alpha", config.Opacity)
        self.root.attributes("-topmost", True)
        screenHeight =  self.root.winfo_screenheight()
        self.root.geometry("+%d+%d"%(0,screenHeight - (config.ItemSize * 3)))
        self.root.configure(background="black")

    def DrawItemSet(self, recBuildJSON, className):
        startingItems = recBuildJSON.find("div", class_=className)
        items = startingItems.find_all("div", {"class": "item-img"})

        for index, item in enumerate(items):
            offset = LoL.RetrieveXYOffset(item)
            spriteSheetIndex = LoL.RetrieveSpriteSheetIndex(item)
            img = self.imageSheets[spriteSheetIndex].crop((offset[0], offset[1], offset[0] + 48, offset[1] + 48)) #48 is size of each sprite
            img = img.resize((self.config.ItemSize, self.config.ItemSize), Image.Resampling.LANCZOS)
            
            if (className == "starting-items"): 
                self.starterItemsTkImage[index] = ImageTk.PhotoImage(img)
                panel = Label(self.root, image = self.starterItemsTkImage[index], borderwidth=0)
                panel.grid(row = index, column = 0)

            elif (className == "core-items"): 
                self.coreItemsTkImage[index] = ImageTk.PhotoImage(img)
                panel = Label(self.root, image = self.coreItemsTkImage[index], borderwidth=0)
                panel.grid(row = index, column = 1, padx=(0, 10))
            elif (className == "item-options-1"): 
                self.fourthItemOptionsTkImage[index] = ImageTk.PhotoImage(img)
                panel = Label(self.root, image = self.fourthItemOptionsTkImage[index], borderwidth=0)
                panel.grid(row = index, column = 2)
            elif (className == "item-options-2"): 
                self.fifthItemOptionsTkImage[index] = ImageTk.PhotoImage(img)
                panel = Label(self.root, image = self.fifthItemOptionsTkImage[index], borderwidth=0)
                panel.grid(row = index, column = 3)
            elif (className == "item-options-3"): 
                self.sixthItemOptionsTkImage[index] = ImageTk.PhotoImage(img)
                panel = Label(self.root, image = self.sixthItemOptionsTkImage[index], borderwidth=0)
                panel.grid(row = index, column = 4)

    def Loop(self):
        self.root.mainloop()