"""
Copyright 2013 Štěpán Bahník

This file is part of Carousel Maze Manager.

Carousel Maze Manager is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Carousel Maze Manager is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Carousel Maze Manager.  If not, see <http://www.gnu.org/licenses/>.
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import localtime, strftime

import traceback
import os
import sys


from controller import Controller
from explorer import Explorer
from processor import Processor
from menu import MenuCM
from filestorage import FileStorage
from optionget import optionGet
from version import version
from window import placeWindow
from tools import saveFileStorage, doesFileStorageRequiresSave


class GUI(Tk):
    "represents GUI"
    def __init__(self):
        super().__init__()
   
        self.title("CM Manager " + ".".join(version()))
        self.option_add("*tearOff", FALSE)
        self.resizable(FALSE, FALSE)
        
        '''
        # used when size of the window is changed for placeWindow arguments     
        self.after(250, lambda: print(self.winfo_width()))
        self.after(250, lambda: print(self.winfo_height()))
        '''
        placeWindow(self, 1010, 834)

        # notebook
        self.selectFunction = ttk.Notebook(self)
        self.selectFunction.grid()

        # FileStorage is associated with the Notebook
        self.selectFunction.fileStorage = FileStorage()
        
        self.processor = Processor(self.selectFunction)
        self.explorer = Explorer(self.selectFunction)
        self.controller = Controller(self.selectFunction)

        notepageWidth = 20
        self.selectFunction.add(self.processor, text = "{:^{}}".format("Process", notepageWidth))
        self.selectFunction.add(self.explorer, text = "{:^{}}".format("Explore", notepageWidth))
        self.selectFunction.add(self.controller, text = "{:^{}}".format("Control", notepageWidth))

        self.selectFunction.bind("<<NotebookTabChanged>>", lambda e: self.checkProcessing(e))
            
        # menu
        self["menu"] = MenuCM(self)

        if not optionGet("Developer", False, 'bool'):
            self.protocol("WM_DELETE_WINDOW", self.closeFun)

        self.mainloop()


    def closeFun(self):
        "ask for saving files on exit"
        if doesFileStorageRequiresSave(self):
            answ = messagebox.askyesno(message = "Do you want to save files before leaving?",
                                       icon = "question", title = "Save files?")
            if answ:
                saveFileStorage(self)                
        self.destroy()


    def checkProcessing(self, event):
        """checks whether it is possible for processor and controller to process files and change
        states of buttons accordingly"""
        self.processor.checkProcessing()
        self.controller.checkProcessing()
        self.explorer.checkProcessing()

     
            

def main():
    if optionGet("Developer", False, 'bool'):
        GUI()
    else:
        for directory in ["Bugs", "Logs", "Selected files"]:
            dirname = os.path.join(os.getcwd(), "Stuff", directory)
            if not os.path.exists(dirname):
                os.mkdir(dirname)
        filepath = os.path.join(os.getcwd(), "Stuff", "Bugs")
        writeTime = localtime()
        filename = os.path.join(filepath, strftime("%y_%m_%d_%H%M%S", writeTime) +
                                "_bugs" + ".txt")
        with open(filename, mode = "w") as bugfile:
            sys.stderr = bugfile
            GUI()



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.getcwd())))
    main()
