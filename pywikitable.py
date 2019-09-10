import datetime
import argparse
import csv
from sys import stdin, stdout
"""
WikiTable - convert a .csv file (tab separated)
            to Wiki table format. 
            
Update History:
* Wed Sep 09 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- Update to V2.0.0
- Use csv reader library instead of old code
- Add GUI for easier use.
* Thu Feb 20 2018 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 - Initial release
"""

DESCRIPTION = \
"""
Convert .CSV file to Wiki table format.
"""

EPILOG = \
"""
That's all folks!
"""

class WikiTable():
    def __init__(self):
        pass

    def __version__(self):
        return "2.0.0-beta"

    def readinputfile(self, file_name = None, DeLim='\t'):
        if (file_name == None):
            csv_file = stdin
        else:
            csv_file = open(file_name, "r")
        csv_reader = csv.reader(csv_file, delimiter=DeLim)
        csv_text = []
        for line in csv_reader:
            csv_text.append(line)
        
        csv_file.close()
        return csv_text

    def convert_to_wiki_table(self, csv_text, headers = False):
        wikitext = "{|class='wikitable' border='1'\n"
        needHeader = headers
        for line in csv_text:
            firstCell = True
            for cells in line:
                if (firstCell or needHeader):
                    wikitext += '|'
                else:
                    wikitext += '||'
                if (needHeader):
                    wikitext += "align='left' style='background:#f0f0f0;'|'''"
                    wikitext += cells
                    wikitext += "'''\n" 
                else:
                    wikitext += cells
                firstCell = False
            if (needHeader):
                needHeader = False
                wikitext += '|-\n'
            else:
                wikitext+='\n|-\n'
        wikitext += "|}\n"
        return wikitext
            

    def write_wiki_text_file(self, text, wikitext_file_name = None):
        if (wikitext_file_name == None):
            f = stdout
            f.write(text)
        else:
            with open(wikitext_file_name, 'w') as f:
                f.write(text)

    def appMain(self, inputfile, outputfile, delimiter, headers):
        
        test = self.readinputfile(inputfile, delimiter)
        wtest = self.convert_to_wiki_table(test, headers)
        self.write_wiki_text_file(wtest, outputfile)
        
"""
The main app class.
Only gets called if this file is running stand alone, and
not if it's included as part of a larger application
"""
class theApp():        
    def __init__(self):
        self.appMain()

    def getVersion(self):
        vapp = WikiTable()
        version = '%(prog) s ' + vapp.__version__()
        return version        

    def getArgs(self):
        parser = argparse.ArgumentParser(\
                               description = DESCRIPTION,
                                           epilog = EPILOG)
        parser.add_argument('-v', '--version', 
                                   action='version', 
                                   version = self.getVersion())
        parser.add_argument("-i", "--inputfile", 
            default=None,
            help="Specifies the .csv input file name.")
        parser.add_argument("-o", "--outputfile", 
            default=None,
            help="Specifies the output file name for resulting Wiki page source code.")
        parser.add_argument("-d", "--delimiter", 
            default='\t',
            help='Specifies the .csv file field delimiter.\n' + \
                 'Can be any character or string\n'
                 'default is TAB(\'\t\')')
        parser.add_argument("-t", "--tableheaders", 
            default=False,
            help="-t True specifies table includes a header row.")
        args = parser.parse_args()
        print('Delimiter = %s'%(args.delimiter))
        return args

    def appMain(self):
        args = self.getArgs()
        app = WikiTable()
        app.appMain(args.inputfile, args.outputfile, args.delimiter, args.tableheaders)

"""
Main program - run stand-alone if not included as part of a larger application
"""
if __name__ == '__main__':
   app = theApp()
  
   
