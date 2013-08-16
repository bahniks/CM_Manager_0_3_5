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

import os.path
import os
from os.path import basename
from tkinter import ttk, messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tempfile


class HelpCM(Tk):
    "application for creating help files for CM Manager"
    def __init__(self):
        if not os.path.exists(os.path.join(os.getcwd(), "Stuff", "Help")):
            messagebox.showinfo(message = "Folder 'Help' doesn't exist in the " + 
                                "'Stuff' directory!", title = "Error", icon = "error")
            return
        
        super().__init__()
        self["padx"] = 7
        self["pady"] = 7
        
        self.title("Help maker")
        self.geometry("+435+135")
        self.resizable(FALSE, FALSE)
        self.saved = True
        self.parent = ""
        self.infile = None
        self.item = "Help"
        self.unfinished = []
        self.name = StringVar()
   
        self.linkMapping = {} # variable containing texts and items that the texts refer to

        for file in os.listdir(os.path.join(os.getcwd(), "Stuff", "Help")):
            if file[0] == "~":
                os.remove(os.path.join(os.getcwd(), "Stuff", "Help", file))
                

        def makeTree():
            "makes tree of existing help pages"
            files = os.listdir(os.path.join(os.getcwd(), "Stuff", "Help"))

            items = []
            for file in sorted(files):             
                filename = os.path.join(os.getcwd(), "Stuff", "Help", file)
                infile = open(filename, mode = "r")
                parent = infile.readline()[1:].rstrip()
                infile.close()
                if parent:
                    items.append([parent, os.path.splitext(file)[0]])
            branches = []

            # if parent of item is a number, item is inserted in the top level of the tree  
            for item in items:
                if 47 < ord(item[0][0]) < 58:
                    tree.insert("", item[0], item[1], text = item[1].replace("_", " "))
                    branches.append(item[1])
                    tree.see(item[1])
                    
            # inserts children of every already inserted parent
            for rep in range(6): # maximal number of levels of the tree
                level = []
                for item in items:
                    if item[1] in branches:
                        continue
                    elif item[0] in branches:
                        tree.insert(item[0], "end", item[1], text = item[1].replace("_", " "))
                        level.append(item[1])
                        tree.see(item[1])
                    else:
                        pass
                branches = branches + level                        
                           

        def makeText():
            "takes text from a file and displays it in a 'text' widget (takes care of formatting)"

            text["state"] = "normal"
            text.delete("1.0", "end")

            infile = open(os.path.join(os.getcwd(), "Stuff", "Help", self.item + ".txt"),
                          mode = "r")
           
            content = []
            for count, line in enumerate(infile):
                if count < 2:
                    continue
                words = line.rstrip().split(" ")
                content = content + words

            text.insert("end", self.name.get(), ("header"))
            text.insert("end", "\n")
            
            for word in content:
                if len(word) and word[0] == "$":
                    divided = word.split("$")
                    if len(divided) > 1:
                        if divided[1] and divided[1][0] == "n": # $nn - adds new lines
                            text.insert("end", "\n" * divided[1].count("n"))
                        elif divided[1] and divided[1][0] in ".,';:-": # interpunctions
                            text.insert("end", divided[1])
                        elif divided[1] == "s" and len (divided) > 2:
                            # $s$See_also: - makes subheader and new line
                            text.insert("end", divided[2], ("subheader"))
                            text.insert("end", "\n")
                        elif divided[1] == "b" and len (divided) > 2:
                            # $b$Bold_text - bold formating
                            text.insert("end", divided[2], ("bold"))
                            text.insert("end", " ")
                        elif divided[1] == "l":
                            # $l$link$Linked_item - $Linked_item not needed if link corresponds
                            # to linked item
                            if len(divided) > 2:
                                text.insert("end", divided[2].replace("_", " "), ("link"))
                            if len(divided) == 4:
                                self.linkMapping[divided[2].replace(" ", "_").capitalize()]\
                                = divided[3]
                            text.insert("end", " ")
                else:
                    word = word + " "
                    text.insert("end", word)

            # 'See also:' is automatically added to the end
            text.insert("end", "\n\n")                
            text.insert("end", "See also:", ("subheader"))

            # first the parent is added as a link
            if tree.exists(self.parent) and self.parent:
                text.insert("end", "\n")
                text.insert("end", "- ")
                text.insert("end", self.parent.replace("_", " "), ("link"))
            # next childen are added as links
            if tree.exists(self.item[1:]):
                children = tree.get_children(self.item[1:])
                if children:
                    for child in children:
                        text.insert("end", "\n")
                        text.insert("end", "+ ")
                        text.insert("end", child.replace("_", " "), ("link"))
                    
            # configuration of tagged text
            text.tag_configure("header", font = "TkDefaultFont 10 bold")
            text.tag_configure("subheader", font = "TkDefaultFont 9 bold")
            text.tag_configure("link", foreground = "blue")
            text.tag_configure("bold", font = "TkDefaultFont 9 bold")

            text.tag_bind("link", "<1>", link)
                
            text["state"] = "disabled"                    

        def makeTextUp():
            textUp.delete("1.0", "end")
            infile = open(os.path.join(os.getcwd(), "Stuff", "Help", self.item + ".txt"),
                          mode = "r")
            for count, line in enumerate(infile, 1):
                position = str(count) + ".0"
                textUp.insert(position, line)
                
            textUp.edit_modified(False)
                       
                               
        def treeSelect(event):
            "called when tree item is clicked on"
            item = tree.identify("item", event.x, event.y)
            if item:
                loadFun(clickedTree = True, item = "~" + item)
                self.item = "~" + item
                if tree.get_children(item):
                    tree.see(tree.get_children(item)[0])


        def link(event):
            "function that is called when linked term is clicked on"
            item = text.get(text.tag_prevrange("link", "current")[0],
                            text.tag_prevrange("link", "current")[1]).replace(" ",
                                                                              "_").capitalize()
            # needed for mapped links (i.e. those in format: $l$distance$Total_distance)
            if item in self.linkMapping.keys(): 
                item = self.linkMapping[item]

            loadFun(clickedTree = True, item = "~" + item)
            self.item = "~" + item

            if tree.exists(item):
                tree.selection_set(item)
                tree.see(item)
            

        def newFun(parent = ""):
            unfinishedSet()
            if self.item == "temp" or self.item == "~temp":
                messagebox.showinfo(message = "Save before opening new file.", icon = "warning")
                return
            
            self.name.set("temp")
            self.item = "~temp"
            file = os.path.join(os.getcwd(), "Stuff", "Help", self.item + ".txt")
            infile = open(file, mode = "w")
            if parent:
                infile.write("@" + parent)
            else:
                infile.write("@")
            infile.close()
            textUp.delete("1.0", "end")
            if parent:
                textUp.insert("end", "@" + parent)
            else:
                textUp.insert("end", "@")
            text["state"] = "normal"
            text.delete("1.0", "end")
            text["state"] = "disabled"
            self.saved = True


        def loadFun(clickedTree = False, item = "set"):           
            if not clickedTree:
                file = askopenfilename(initialdir = os.path.join(os.getcwd(), "Stuff", "Help"),
                                       filetypes = [("Text files", "*.txt")])
                if not file:
                    return

            unfinishedSet()
            
            if item != "set":
                self.item = item
            
            if not clickedTree:
                self.item = "~" + os.path.splitext(basename(file))[0]
            else:
                file = os.path.join(os.getcwd(), "Stuff", "Help", self.item[1:] + ".txt")

            self.saved = True           
            self.name.set(self.item.replace("_", " ")[1:])

            if not self.item in self.unfinished:           
                tempFile = os.path.join(os.getcwd(), "Stuff", "Help", self.item + ".txt")
                copyfile = open(file, mode = "r")
                infile = open(tempFile, mode = "w")
                for line in copyfile:
                    infile.write(line)
                copyfile.close()
                infile.close()
            
            textUp.delete("1.0", "end")
            makeTextUp()
            if textUp.get("1.0", "1.1") == "@":
                self.parent = textUp.get("1.1", "2.0").rstrip()
            makeText()

            if tree.exists(self.item[1:]):
                tree.see(self.item[1:])
                tree.selection_set(self.item[1:])                
            

        def saveFun():
            if not self.name.get() or self.name.get() == "temp":
                messagebox.showinfo(message = "You have to select page name.", icon = "warning")
                return

            fileList = os.listdir(os.path.join(os.getcwd(), "Stuff", "Help"))
            if self.name.get() in fileList:
                messagebox.showinfo(message = "Selected name is already used.", icon = "warning")
                return                

            if self.item in self.unfinished:
                self.unfinished.remove(self.item)

            if self.item == "~temp":
                self.item = "~" + self.name.get().rstrip().replace(" ", "_")

            if self.item != "~" + self.name.get().rstrip().replace(" ", "_"):
                os.remove(os.path.join(os.getcwd(), "Stuff", "Help", self.item + ".txt"))
                os.remove(os.path.join(os.getcwd(), "Stuff", "Help", self.item[1:] + ".txt"))
                tree.delete(self.item[1:])
                self.item = "~" + self.name.get().rstrip().replace(" ", "_")
                                
            tempFile = open(os.path.join(os.getcwd(), "Stuff", "Help", self.item + ".txt"),
                            mode = "w")
            tempFile.write(textUp.get("1.0", "end"))
            tempFile.close()
            
            oldFile = open(os.path.join(os.getcwd(), "Stuff", "Help", self.item[1:] + ".txt"),
                           mode = "w")
            oldFile.write(textUp.get("1.0", "end"))
            oldFile.close()
            
            self.saved = True
            unfinishedSet()

            if tree.exists(self.parent) and not tree.exists(self.item[1:]):
                tree.insert(self.parent, "end", self.item[1:], text = self.name.get())
                tree.see(self.item[1:])
                tree.selection_set(self.item[1:])         


        def makeUnfinished(item, row):
            ID = ttk.Label(unsavedFrame, text = item)
            ID.grid(column = 0, row = row, padx = 2, pady = 2, sticky = "W")
            ID.bind("<1>", lambda e: loadFun(clickedTree = True, item = item))
                  

                 
        def unfinishedSet():
            nonlocal unsavedFrame
            
            if not self.saved:
                tempFile = open(os.path.join(os.getcwd(), "Stuff", "Help", self.item + ".txt"),
                                mode = "w")
                tempFile.write(textUp.get("1.0", "end"))
                tempFile.close()
                if not self.item in self.unfinished:
                    self.unfinished.append(self.item)
                else:
                    return

            unsavedFrame.destroy()
            unsavedFrame = ttk.Frame(self)
            unsavedFrame.grid(column = 1, row = 2, padx = 4, pady = 4, sticky = (N, W))
            
            for row, unfinished in enumerate(self.unfinished):
                makeUnfinished(unfinished, row)


        def modifiedText(event):
            self.saved = False
            if textUp.get("1.0", "1.1") == "@":
                self.parent = textUp.get("1.1", "2.0").rstrip()
            tempFile = open(os.path.join(os.getcwd(), "Stuff", "Help", self.item + ".txt"),
                            mode = "w")
            tempFile.write(textUp.get("1.0", "end"))
            tempFile.close()
            makeText()
            unfinishedSet()


        def onquit():
            ret = False
            if self.unfinished:
                ret = messagebox.askyesnocancel(message = "There are some unsaved files.\n" + 
                                                "Do you want to save them?",
                                                title = "Unsaved files", default = "cancel",
                                                icon = "warning")
            if ret == None:
                return
            elif ret == True:
                if not self.saved:
                    tempFile = open(os.path.join(os.getcwd(), "Stuff", "Help", self.item + ".txt"),
                                    mode = "w")
                    tempFile.write(textUp.get("1.0", "end"))
                    tempFile.close()
                    if not self.item in self.unfinished:
                        self.unfinished.append(self.item)
                for item in self.unfinished:
                    tempFile = os.path.join(os.getcwd(), "Stuff", "Help", item + ".txt")       
                    oldFile = os.path.join(os.getcwd(), "Stuff", "Help", item[1:] + ".txt")
                    os.remove(oldFile)
                    os.rename(tempFile, oldFile)
            else:
                pass
            
            for file in os.listdir(os.path.join(os.getcwd(), "Stuff", "Help")):
                if file[0] == "~" or file == "temp":
                    os.remove(os.path.join(os.getcwd(), "Stuff", "Help", file))
            self.destroy()
        

        def popUp(event):
            "called when tree item is clicked on"
            item = tree.identify("item", event.x, event.y)
            if item:
                menu = Menu(self, tearoff = 0)
                menu.add_command(label = "Selecet as parent", command = selectAsParent)
                menu.add_command(label = "Add child", command = addChild)
                menu.add_command(label = "Remove item", command = removeItem)
                menu.post(event.x_root, event.y_root)
                self.clickedItem = item

                
        def selectAsParent():
            self.parent = self.clickedItem
            textUp.delete("1.0", "2.0")
            textUp.insert("1.0", "@" + self.parent)
            makeText()


        def addChild():
            newFun(parent = self.clickedItem)        

            
        def removeItem():
            ret = messagebox.askyesno(message = "Are you sure you want to remove the item?",
                                      icon = "question", title = "Remove")
            if ret == True:
                file = os.path.join(os.getcwd(), "Stuff", "Help", self.clickedItem + ".txt") 
                os.remove(file)
                tree.delete(self.clickedItem)
            else:
                return
                          
                                                          

        # widgets                                    
        text = Text(self, width = 70, height = 18, wrap = "word")
        text.grid(column = 2, row = 2, pady = 4, sticky = E)

        scroll = ttk.Scrollbar(self, orient = VERTICAL, command = text.yview)
        scroll.grid(column = 3, row = 2, pady = 4, sticky = (N, S, W))
        text.configure(yscrollcommand = scroll.set)

        textUp = Text(self, width = 90, height = 25, state = "normal", wrap = "word")
        textUp.grid(column = 1, row = 1, pady = 4, columnspan = 2)

        scrollUp = ttk.Scrollbar(self, orient = VERTICAL, command = textUp.yview)
        scrollUp.grid(column = 3, row = 1, pady = 4, sticky = (N, S, W))
        textUp.configure(yscrollcommand = scrollUp.set)

        buttonBar = ttk.Frame(self)
        buttonBar.grid(column = 1, row = 0, pady = 4, sticky = (N, S, E, W),
                       columnspan = 2)
        buttonBar.columnconfigure(2, weight = 1)

        saveBut = ttk.Button(buttonBar, text = "Save", command = saveFun)
        saveBut.grid(column = 4, row = 0)

        nameEntry = ttk.Entry(buttonBar, width = 30, justify = "left",
                                textvariable = self.name)
        nameEntry.grid(column = 3, row = 0, padx = 4)

        nameLab = ttk.Label(buttonBar, text = "Name:")
        nameLab.grid(column = 2, row = 0, padx = 4, sticky = E)

        loadBut = ttk.Button(buttonBar, text = "Load", command = loadFun)
        loadBut.grid(column = 0, row = 0, padx = 4)

        newBut = ttk.Button(buttonBar, text = "New", command = newFun)
        newBut.grid(column = 1, row = 0, padx = 4)       

        tree = ttk.Treeview(self, selectmode = "browse")
        tree.grid(column = 0, row = 0, rowspan = 3, pady = 4, padx = 4, sticky = (N, S, E, W))

        unsavedFrame = ttk.Frame(self)
        unsavedFrame.grid(column = 1, row = 2, padx = 4, pady = 4, sticky = (N, W))

        makeTree()

        tree.bind("<1>", treeSelect)
        tree.bind("<3>", popUp)
        textUp.bind("<KeyRelease>", modifiedText)
        
        def controlKey(text):     
            textUp.insert("insert", text)
            return "break"
        def controlNewLine(text, number):
            textUp.insert("insert", text + "\n" * number)
            return "break"
        textUp.bind("<Control-j>", lambda e: controlKey("$n "))
        textUp.bind("<Control-b>", lambda e: controlKey("$b$"))
        textUp.bind("<Control-l>", lambda e: controlKey("$l$"))
        textUp.bind("<Control-s>", lambda e: controlKey("$s$"))
        textUp.bind("<Control-k>", lambda e: controlKey("$nn "))        
        textUp.bind("<Control-.>", lambda e: controlKey("$. "))
        textUp.bind("<Control-,>", lambda e: controlKey("$, "))
        textUp.bind("<Control-n>", lambda e: controlNewLine("$n", 1))
        textUp.bind("<Control-m>", lambda e: controlNewLine("$nn", 2))
        

        self.protocol("WM_DELETE_WINDOW", onquit)


        self.name.set("Help")
        makeText()
        makeTextUp()
        self.item = "~Help"

        
        self.mainloop()
      

if __name__ == "__main__": HelpCM()
    
