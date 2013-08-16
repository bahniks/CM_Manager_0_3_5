"""
Carousel Maze Manager - a program for analysis of data from behavioral neuroscience tasks
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
from tkinter import messagebox
from urllib.request import urlopen
import zipfile
import os
import shutil
import sys


def returnSiteContent(link):
    "return text obtained from web site"
    site = urlopen(link)
    text = site.read()
    site.close()
    text = str(text)[2:-1]
    return text    


def checkNewVersion(version):
    "checks whether there is a new version available"
    newVersion = returnSiteContent("http://www.cmmanagerweb.appspot.com/version").split(".")
    try:
        from optionget import optionGet
        versionSeen = optionGet("DontShowVersion", version(), "list")
    except Exception:
        versionSeen = version
    for i in range(3):
        if int(newVersion[i]) > int(versionSeen[i]):
            message = "New version of Carousel Maze Manager ({}.{}.{}) is available.\n".format(
                *newVersion) + "Do you want to download and install the new version?"
            root = makeRoot()
            answ = messagebox.askyesnocancel(message = message, icon = "question",
                                             title = "New version available", default = "yes",
                                             detail = "Select 'No' to not be asked again.")
            if answ is None:
                pass
            elif answ:
                root.config(cursor = "wait")
                try:
                    download(newVersion)
                except Exception as e:
                    messagebox.showinfo(title = "Error", icon = "error", detail = e,
                                        message = "Some problem with updating occured.")
                finally:
                    root.config(cursor = "")
            else:
                try:
                    from optionwrite import optionWrite
                    optionWrite("DontShowVersion", newVersion)
                except Exception:
                    pass
            root.destroy()
            break

    
def download(version):
    "downloads the version from github"
    stuffname = os.path.join(os.getcwd(), "Stuff")
    if not os.path.exists(stuffname):
        os.mkdir(stuffname)
    url = "https://github.com/bahniks/CM_Manager_{}_{}_{}/archive/master.zip".format(*version)
    filename = os.path.join(stuffname, "CMM.zip")

    with open(filename, mode = "wb") as outfile:
        with urlopen(url) as infile:
            for line in infile:
                outfile.write(line)
                
    if zipfile.is_zipfile(filename):
        extractedFile = zipfile.ZipFile(filename, mode = "r")
        commonname = os.path.commonprefix(extractedFile.namelist())
        for file in extractedFile.namelist():
            if not os.path.basename(file).startswith("."):
                extractedFile.extract(file, path = stuffname)
    extractedFile.close()

    os.remove(filename)
    unzipped = os.path.join(stuffname, commonname)

    for directory in ["Help", "Modules"]:
        dirname = os.path.join(stuffname, directory)
        shutil.rmtree(dirname, ignore_errors = True)
        shutil.move(os.path.join(unzipped, "Stuff", directory), stuffname)

    if not os.path.exists(os.path.join(stuffname, "Parameters")):
        os.mkdir(os.path.join(stuffname, "Parameters"))
    for file in os.listdir(os.path.join(unzipped, "Stuff", "Parameters")):        
        old = os.path.join(stuffname, "Parameters", file)       
        if not os.path.exists(old):
            new = os.path.join(unzipped, "Stuff", "Parameters", file)
            os.rename(new, old)        

    for file in os.listdir(os.path.join(unzipped, "Stuff")):
        new = os.path.join(unzipped, "Stuff", file)
        if os.path.isfile(new):
            old = os.path.join(stuffname, file)       
            if os.path.exists(old):
                os.remove(old)
            os.rename(new, old)

    shutil.rmtree(unzipped, ignore_errors = True)


def makeRoot():
    "makes root window for messagebox"
    root = Tk()
    root.withdraw()
    return root

    
def main():
    "starts CMM"
    # developer?
    try:
        from optionget import optionGet
        if optionGet("Developer", False, 'bool'):
            start()
            return
    except Exception:
        pass
    
    modules = os.path.join(os.getcwd(), "Stuff", "Modules")
    # new version?
    try:
        if os.path.extists(modules):
            sys.path.append(modules)
            from version import version
            version = version()
        else:
            version = [0, 3, 4]
    except Exception:
        version = [0, 3, 4]
    checkNewVersion(version)
    # starting
    try:     
        if modules not in sys.path:
            sys.path.append(modules)
        from starter import main as start
    except Exception as e:
        root = makeRoot()
        messagebox.showinfo(title = "Error", icon = "error", detail = e,
                            message = "Epic fail!\nTry to start CMM again.")
        root.destroy()
    else:
        start()
        
        
if __name__ == "__main__": main()
