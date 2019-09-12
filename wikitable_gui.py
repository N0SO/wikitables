#!/usr/bin/env python
"""
wikitable_gui - GUI front end for pywikitables.py. 
            
Update History:
* Thu Sep 12 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 - Initial release
"""
import sys
python_version = sys.version_info[0]
if (python_version == 2):
    from Tkinter import *
    from tkMessageBox import *
    from tkFileDialog   import askopenfilename
else:
    from tkinter import *
    from tkinter.messagebox import showinfo
    from tkinter.filedialog import askopenfilename
    
from pywikitable import WikiTable
import os.path

VERSION = '1.0.0'

class wikiWin(WikiTable):
    def __init__(self, RUN = True):
        self.fileName = None
        self.csvdata =[]
        self.appMain(RUN)
        
    #Creation of init_window
    def client_exit(self):
        print ("Exiting...")
        exit()

    def helpmenu(self):
        print ('Help Menu...')
        
    def About(self):
        print ('About...')
        pythonversion = sys.version.splitlines()
        infotext = \
        'WIKITABLE_GUI - Version ' + VERSION + '\n' + \
        'Utilities to convert CSV files to Wiki TABLE format.\n' \
        + 'Python ' + pythonversion[0]
        showinfo('WIKITABLE_GUI', infotext)
       
    def OpenFile(self):
        if (self.Tabs.get() == 1):
            FILETYPES = [("CSV files","*.csv"),
                         ("Text files","*.txt")]
            debugtext = 'Open COMMA delimited CSV file...'
        else:
            FILETYPES = [("Text files","*.txt"),
                         ("CSV files","*.csv")]
            debugtext = 'Open TAB delimited CSV file...'
        FILETYPES.append( ("LOG files","*.log") ) 
        FILETYPES.append( ("All Files","*.*") )
        
        print (debugtext)
        fileName = askopenfilename(title = "Select Input File:",
                                      filetypes=FILETYPES)
        if os.path.isfile(fileName):
            print('File name selected: %s'%(fileName))
            self.fileName = fileName
            self.csvdata = self.readinputfile(fileName, 
                                              self.Delchar)

            #Convert csvdata for display in TextBox                                  
            textboxdata = []                                  
            for line in self.csvdata:
                item1 = True
                item =''
                for litem in line:
                    if (item1):
                        item1 = False
                        item += litem
                    else:
                        item += ',' + litem
                textboxdata.append(item + '\n')
            #print ('csvdata:\n%s'%(self.csvdata))
            self.fillLogTextfromData(textboxdata, self.LogText, 
                                                   clearWin=True)
            self.filemenu.entryconfigure("Convert to Wiki...", 
                                                  state="normal")
        else:
            print('File open CANCEL.')
    
    def SaveWiki(self):
        print ('Convert to Wiki format...')
        temp = self.convert_to_wiki_table(self.csvdata, self.headerflag)
        wikiText = temp.splitlines()
        #print('wikiText:\n%s'%(wikiText))
        textboxdata = []
        for line in wikiText:
            textboxdata.append(line + '\n')
        self.fillLogTextfromData(textboxdata, self.LogText, clearWin=True)

    def fillLogTextfromData(self, Data, textWindow, clearWin = False):
        if (clearWin):
            textWindow.delete(1.0, END)
        for line in Data:
            #print ('+++>line:\n%s'%(line))
            textWindow.insert(END, line)

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
        self.headerflag = self.Headers.get()
  
    def init_window(self):
        self.root = Tk()

        self.Tabs = IntVar()
        self.Headers = IntVar()

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
        #self.filemenu.add_command(label="Convert to Wiki Table...", command=self.SaveWikiTable, state="disabled")
        self.filemenu.add_command(label="Exit", command=self.root.quit)
    
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)
        
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
        
        self.optionsmenu.add_checkbutton(\
                                  label='Column Headers',
                                  onvalue=1, 
                                  offvalue=0, 
                                  variable=self.Headers,
                                  command = self.head_options)
        
        return self.root

    def appMain(self,run = True):
        if (run):
            print ('run = True')
            win = self.init_window()
            
            #Set OPTIONS  to match options menu.
            self.del_options() # Set DELIMITER char 
            self.head_options() # Set HEADER option
            
            win.mainloop()
        else:
            print ('run = False')

if __name__ == '__main__':
      #creation of an instance
      win = wikiWin()
