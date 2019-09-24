#!/usr/bin/env python
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from tkMessageBox import *
from tkFileDialog   import askopenfilename
from tkFileDialog   import askdirectory
from tkFileDialog   import asksaveasfilename
from pywikitable import WikiTable
import os.path

VERSION = '0.0.1'

class wikiWin(WikiTable):
    def __init__(self, RUN = True):
        self.appMain(RUN)
        
    #Creation of init_window
    def client_exit(self):
        print ("Exiting...")
        exit()

    def helpmenu(self):
        print ('Help Menu...')
        
    def About(self):
        print ('About...')
        
    def OpenFile(self):
        print ("Open FLLog File!")
        fileName = askopenfilename(title = "Select Input File:",
                                      filetypes=[("LOG files","*.log"),
                                                 ("CSV files","*.csv"),
                                                 ("Text files","*.txt"),
                                                 ("All Files","*.*")])
        if os.path.isfile(fileName):
            print('File name selected: %s'%(fileName))
            self.wikistuff.fileName = fileName
            self.csvdata = self.readinputfile(fileName, self.Delchar)
            self.fillLogTextfromData(self.csvdata, self.LogText)
            self.filemenu.entryconfigure("Convert to Wiki...", state="normal")
            #self.filemenu.entryconfigure("Convert to Wiki Table...", state="normal")
            #print('Raw logDate: %s'%(self.wikistuff.logData))
        
    
    def SaveWiki(self):
        print ('Convert to Wiki format...')
        temp = self.wikistuff.convert_to_wiki(self.wikistuff.logData)
        wikiText = self.wikistuff.make_wiki_entry( \
                        temp, whichnet = None)
        self.fillLogTextfromData(wikiText, self.LogText, clearWin=True)

    def SaveWikiTable(self):
        print ('Convert to Wiki Table format...')
        temp = self.wikistuff.convert_to_wiki_table(self.wikistuff.logData)
        #print('===>WikiText:\n%s'%(temp))
        wikiText = self.wikistuff.make_wiki_entry( \
                                temp, whichnet = None)

        self.fillLogTextfromData(wikiText, self.LogText, clearWin=True)

    def fillLogTextfromData(self, Data, textWindow, clearWin = False):
        if (clearWin):
            textWindow.delete(1.0, END)
        for item in Data:
            for line in item:
                textWindow.insert(END, line)
            textWindow.insert(END,'\n')

    def fillLogTextfromFile(self, filename, textWindow, clearWin = False):
        if (clearWin):
            textWindow.delete(1.0, END)
        try: 
           with open(filename,'r') as f:
              retText = f.readlines()
           self.fillLogTextfromData(retText, textWindow, clearWin)
        except IOError:
           retText = ('Could not read file: '%(fName))
        return retText
        
    def del_options(self):
        tabs = self.Tabs.get()
        if (tabs == 0):
            self.Delchar = '\t'
        elif (tabs == 1):
            self.Delchar = ','
        else:
            self.Delchar = '\t'
            print ('Bad DELIMITER option: %d\n' + \
                   'Defaulting to TAB character'%(tabs))
  
    def head_options(self):
        headers = self.Headers.get()
        print('Headers: %s\n'%(headers))
  
  
    def init_window(self):
        self.root = Tk()
        self.S = Scrollbar(self.root)
        self.LogText = Text(self.root, height=10, width=120)
        self.S.pack(side=RIGHT, fill=Y)
        self.LogText.pack(side=LEFT, fill=Y)
        self.S.config(command=self.LogText.yview)
        self.LogText.config(yscrollcommand=self.S.set)

        self.root.title("Convert CSV File to Wiki Table")
        menu = Menu(self.root)
        self.root.config(menu=menu)
        self.filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open Input File", command=self.OpenFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Convert to Wiki...", command=self.SaveWiki, state="disabled")
        self.filemenu.add_command(label="Convert to Wiki Table...", command=self.SaveWikiTable, state="disabled")
        self.filemenu.add_command(label="Exit", command=self.root.quit)
    
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)
        
        self.Tabs = IntVar()
        self.optionsmenu = Menu(menu)
        menu.add_cascade(label='Options', menu=self.optionsmenu)
        self.optionsmenu.add_radiobutton(label = 'Tabs as Field Delimiters',
                                          variable = self.Tabs,
                                          value = 0,
                                          command = self.del_options)
        self.optionsmenu.add_radiobutton(label = 'Commas as Field Delimiters', 
                                          variable = self.Tabs,
                                          value = 1,
                                          command = self.del_options)
        self.optionsmenu.add_separator()
        
        self.Headers = IntVar()
        self.optionsmenu.add_checkbutton(\
                                  label='Column Headers',
                                  onvalue=1, 
                                  offvalue=0, 
                                  variable=self.Headers,
                                  command = self.head_options)
        
        return self.root

    def appMain(self,run = True):
        if (run):
            self.wikistuff = WikiTable()
            win = self.init_window()
            print ('run = True')
            win.mainloop()
        else:
            print ('run = False')

if __name__ == '__main__':
      #creation of an instance
      win = wikiWin()
