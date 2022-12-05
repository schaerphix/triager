# *********************************************************************
#
#                           Triage
#
# **********************************************************************
#
#  Autor:    schaerphix
#  Date:     06.10.2021
#  Revision: V1.2
#
#  LICENSE:  GNU General Public License v3.0  
#


#   ********************************************************************
#                           Import
#   ********************************************************************

from tkinter import *
import shutil
from tkinter import filedialog as fd
import os
from PIL import ImageTk, Image


#   ********************************************************************
#                           Classes
#   ********************************************************************

class GUI:
    """
    Erstellt die GUI Klasse
    """

    def __init__(self):
        self.version = 'V1.1'
        self.wid = Tk()
        self.selectFiles = None
        self.actPicNo = 0
        self.confWin = None
        self.newFoldWin = None
        self.folderPath = None
        self.folderList = []
        self.button_list = []
        self.img = None
        self.tempPic = None

        self.deltaY = 40
        self.butHeight = 10

        self.white = "#ffffff"
        self.blue = "#c3e7eb"
        self.green = "#cbdeb6"  # 00AC69
        self.greenDark = "#98d19a"
        self.grayA = "#eeeeee"
        self.gray = "#99b5c9"
        self.grayDark = "#8695b0"
        self.red = "#bd8c97"
        self.rosa = "#ba7591"
        self.black = "#000000"
        self.yellow = "#e0da8d"
        self.violett = "#a35f91"
        self.orange = "#cca693"

        self.tiFon = "arial nova light"
        self.tiFonSiz = 30
        self.tiFonSty = "normal"

        self.teFon = "arial nova light"
        self.teFonSiz = 12
        self.teFonSty = "normal"

        self.buttonWidth = 15

        self.reliefEnt = "groove"

        self.fullScreen = True
        self.screen_w_fix = 1500
        self.screen_h_fix = 900
        self.screen_w = self.GetScreenResolution()[0] - 75
        self.screen_h = self.GetScreenResolution()[1] - 80
        
        self.width_A = self.screen_w - 10
        self.width_B = ((self.screen_w / 5) * 4) - 10
        self.width_C = ((self.screen_w / 5) * 1) - 10

        self.height_A = 100
        self.height_B = 50
        self.height_C = self.screen_h - (2 * self.height_B) - 5

    def CreatWin(self, tit):
        self.wid.geometry(str(self.screen_w)+'x'+str(self.screen_h))
        self.wid.title(tit)
        self.wid.tk_setPalette(self.grayA)
        self.wid.configure(background=self.grayA)
        self.wid.iconphoto(False, PhotoImage(file='triager.png'))

        self.setupFrame = Frame(self.wid, background=self.white, width=self.width_A, height=self.height_B)
        self.setupFrame.place(x=5, y=5)

        self.pictureFrame = Frame(self.wid, background=self.white, width=self.width_B, height=self.height_C)
        self.pictureFrame.place(x=5, y=self.height_B + 10)

        self.selectFrame = Frame(self.wid, background=self.white, width=self.width_C + 5, height=self.height_C)
        self.selectFrame.place(x=self.width_B + 10, y=self.height_B + 10)
        
        self.actualFrame = Frame(self.wid, background=self.white, width=self.width_A, height=self.height_B)
        self.actualFrame.place(x=5, y=self.height_B + self.height_C + 15)

        self.labPathFix = Label(self.setupFrame, background=self.white, foreground=self.grayDark, text="open: ",
                                font=(self.teFon, self.teFonSiz, self.teFonSty))
        self.labPathFix.place(x=250, y=15)

        self.labPath = Label(self.setupFrame, background=self.white, foreground=self.black, text="",
                             font=(self.teFon, self.teFonSiz, self.teFonSty))
        self.labPath.place(x=400, y=15)
        
        self.labActulaPicTit = Label(self.actualFrame, background=self.white, foreground=self.grayDark, text="Picture: ",
                                font=(self.teFon, self.teFonSiz, self.teFonSty))
        self.labActulaPicTit.place(x=50, y=15)
        
        self.labActulaPic = Label(self.actualFrame, background=self.white, foreground=self.black, text="",
                                font=(self.teFon, self.teFonSiz, self.teFonSty))
        self.labActulaPic.place(x=150, y=15)
        
        
        self.panel = Label(self.pictureFrame, image=self.img,background=self.white)
        self.panel.place(x=0, y=0)

        self.openBut = Button(self.setupFrame, background=self.gray, relief = "flat", width=self.buttonWidth, text="Pictures")
        self.openBut["command"] = self.OpenFile
        self.openBut.place(x=50, y=10)

        self.NewFolBUT = Button(self.setupFrame, background=self.gray, relief = "flat", width=self.buttonWidth, text="new folder")
        self.NewFolBUT["command"] = self.CreatNewFolder
        self.NewFolBUT.place(x=self.width_B + 20, y=10)

        self.setupBUT = Button(self.setupFrame, background=self.gray, relief = "flat", width=self.buttonWidth, text="select folder")
        self.setupBUT["command"] = self.OpenFolderPath
        self.setupBUT.place(x=self.width_B + (self.width_C/2) + 20, y=10)

        self.mirorBUT = Button(self.selectFrame, background=self.yellow, relief = "flat", width=self.buttonWidth, text="180°")
        self.mirorBUT["command"] = self.Miror
        self.mirorBUT.place(x=(self.width_C/3.3) , y=self.height_C - 150)

        self.rotLeftBUT = Button(self.selectFrame, background=self.yellow, relief = "flat", width=self.buttonWidth, text="turn left")
        self.rotLeftBUT["command"] = self.RotationLeft
        self.rotLeftBUT.place(x=20, y=self.height_C - 100)

        self.rotRightBUT = Button(self.selectFrame, background=self.yellow, relief = "flat", width=self.buttonWidth, text="turn right")
        self.rotRightBUT["command"] = self.RotationRight
        self.rotRightBUT.place(x=(self.width_C/2) + 20, y=self.height_C - 100)

        self.picBackBUT = Button(self.selectFrame, background=self.yellow, relief = "flat", width=self.buttonWidth, text="<")
        self.picBackBUT["command"] = self.PrePic
        self.picBackBUT.place(x=20, y=self.height_C - 50)

        self.picNextBUT = Button(self.selectFrame, background=self.yellow, relief = "flat", width=self.buttonWidth, text=">")
        self.picNextBUT["command"] = self.NextPic
        self.picNextBUT.place(x=(self.width_C/2) + 20, y=self.height_C - 50)

        return self.wid

    def CreatNewFolder(self):

        def NewFoOK():
            newFoldPath = fd.askdirectory(title="Select Folder")
            newFoldPath = newFoldPath + "/" + self.namEntry.get()
            os.mkdir(newFoldPath)
            self.folderList.append(newFoldPath)
            self.newFoldWin.destroy()
            self.CreatButtons()

        self.widN = Tk()
        self.widN.geometry("500x200")
        self.widN.title("Neuer Ordner")
        self.widN.tk_setPalette(self.white)

        newFoldNam = Label(self.widN, background=self.white, foreground=self.black, text="Name new folder",
                           font=(self.teFon, self.teFonSiz, self.teFonSty))
        newFoldNam.place(x=5, y=20)

        self.namEntry = Entry(self.widN, background=self.white, relief=self.reliefEnt, bd=2, width=20)
        self.namEntry.place(x=250, y=20)

        newFoOKBut = Button(self.widN, background=self.grayDark, width=self.buttonWidth, text="OK")
        newFoOKBut["command"] = NewFoOK
        newFoOKBut.place(x=180, y=150)

        self.newFoldWin = self.widN


    def OpenFile(self):
        self.selectFiles = fd.askopenfilenames(title="open files")
        self.actPicNo = 0
        self.GetFilePath()
        self.OpenPic()

    def OpenPic(self):
        picAuto = Image.open(self.selectFiles[self.actPicNo])
        self.tempPic = picAuto
        self.ShowPic(picAuto)
        self.labActulaPic['text'] = self.selectFiles[self.actPicNo].split('/')[len(self.selectFiles[self.actPicNo].split('/'))-1]
        self.inFolderCheck(self.selectFiles[self.actPicNo].split('/')[len(self.selectFiles[self.actPicNo].split('/'))-1])

    def ShowPic(self,picAuto):
        pic = self.AutoSize(picAuto)
        self.img = ImageTk.PhotoImage(pic)
        self.panel ["image"] = self.img

    def AutoSize(self,pic):
        sizeOrig = pic.size
        picVerh = sizeOrig[1] / sizeOrig[0]
        if sizeOrig[0] > sizeOrig[1]:
            picAuto = pic.resize((int(self.width_B), int(self.width_B * picVerh)))
        else:
            picAuto = pic.resize((int(self.height_C / picVerh),self.height_C))
        return picAuto

    def GetFilePath(self):
        folder = self.selectFiles[0].split('/')
        a = 0
        self.folderPath = ""
        while a < (len(folder) - 1):
            self.folderPath = self.folderPath + folder[a] + "/"
            a += 1
        self.labPath["text"] = self.folderPath

    def OpenFolderPath(self):
        folderPathX = fd.askdirectory(title="Ordner Auswählen")
        self.folderList.append(folderPathX)
        self.CreatButtons()
        self.inFolderCheck(self.selectFiles[self.actPicNo].split('/')[len(self.selectFiles[self.actPicNo].split('/'))-1])


    def NextPic(self):
        if not self.selectFiles == None:
            self.actPicNo += 1
            if self.actPicNo > len(self.selectFiles) - 1:
                self.img = None
                self.panel ["image"] = self.img
                self.actPicNo = len(self.selectFiles)
            else:
                self.OpenPic()


    def PrePic(self):
        if not self.selectFiles == None:
            self.actPicNo -= 1
            if self.actPicNo < 0 :
                self.img = None
                self.panel ["image"] = self.img
                self.actPicNo = -1
            else:
                self.OpenPic()


    def RotationLeft(self):
        if self.img:
            rotPic = self.tempPic.rotate(90)
            self.ShowPic(rotPic)


    def RotationRight(self):
        if self.img:
            rotPic = self.tempPic.rotate(270)
            self.ShowPic(rotPic)


    def Miror(self):
        if self.img:
            rotPic = self.tempPic.rotate(180)
            self.ShowPic(rotPic)


    def CopyToFolder(self, path):
        shutil.copy(self.selectFiles[self.actPicNo],path)
        self.inFolderCheck(self.selectFiles[self.actPicNo].split('/')[len(self.selectFiles[self.actPicNo].split('/'))-1])

    def CreatButtons(self):
        self.actYpos = 20
        for n in self.button_list:
            n.destroy()
        self.button_list = []
        for n in self.folderList:
            text = self.GetFolderName(n)
            self.button_list.append(self.CreatFolderButton(self.selectFrame, n, text, (self.width_C/3.3), self.actYpos))
            self.actYpos = self.actYpos + self.deltaY + self.butHeight


    def CreatFolderButton(self, rot, path, tex, px, py):
        but = Button(rot, background=self.orange, width=self.buttonWidth, text=tex)
        but["command"] = lambda: self.CopyToFolder(path)
        but.place(x=px, y=py)
        return but

    def GetFolderName(self, fPath):
        folder = fPath.split('/')
        folderNa = folder[len(folder) - 1]
        return folderNa

    def GetScreenResolution(self):
        if self.fullScreen == True:
            screen_width = self.wid.winfo_screenwidth()
            screen_height = self.wid.winfo_screenheight()
        else:
            screen_width = self.screen_w_fix
            screen_height = self.screen_h_fix
        return screen_width, screen_height

    def inFolderCheck(self,pic):
        for i in range(len(self.button_list)):
            result = self.findfile(pic,self.folderList[i])#os.path.join(self.folderList[i], pic)
            if result != None:
                self.button_list[i]['background'] = self.green
            else:
                self.button_list[i]['background'] = self.orange
     
    def findfile(self,name, path):
        for dirpath, dirname, filename in os.walk(path):
            if name in filename:
                return os.path.join(dirpath, name)       

#   ********************************************************************
#                           MAIN
#   ********************************************************************

def main(args):
    gui = GUI()
    width, height = gui.GetScreenResolution()
    gui = gui.CreatWin("Triager "+ gui.version)
    gui.mainloop()

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
