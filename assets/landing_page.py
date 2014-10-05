from tkinter  import *
from tkinter.ttk import *
from engine import *

from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class Landing_Page(GUI):
  
    def __init__(self, master):
        GUI.__init__(self, master)   
        self.master = master
        
        self.landing_window()
 
 
    def landing_window(self):
 

        progress_label = Label(self, text="Daily Progress")
        progress_label.grid(row = 3, column =3 ,sticky=W+ E+S + N, pady=4, padx=5)
        progress_label.configure(anchor = CENTER)

        area1 = Canvas(self)
        area1.grid(row=5, column=0, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)

        area2 = Canvas(self)
        area2.grid(row=5, column=2, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)

        area3 = Canvas(self)
        area3.grid(row=5, column=4, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)

        progress_label = Label(self, text="Daily Progress")
        progress_label.grid(row = 3, column =3 ,sticky=W+ E+S + N, pady=4, padx=5)
        progress_label.configure(anchor = CENTER)
        
        
        progress = Progressbar(self, orient = 'horizontal', mode= 'determinate')
        
        progress.grid(row = 4, column=0, columnspan = 6, stick = E + W, padx = 3)
        progress.start()
                  
def start(self):
    self.progress["value"] = 0
    self.max = 24
    self.progress["midnight"]=24
    self.progress["value"] = 12
    
def main():
  
    Landing_Page(Tk()) 


if __name__ == '__main__':
    main()  
        
