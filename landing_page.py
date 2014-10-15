from tkinter  import *
from tkinter.ttk import *


from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class Landing_Page (Frame):
    def __init__(self, parent, character):
        Frame.__init__(self, parent)
        self.landing_window()
        
        self.columnconfigure(0, weight =1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 1)
        #self.columnconfigure(3, weight = 1)
        #self.rowconfigure (4, weight =1)
        #self.rowconfigure (5, weight = 1)
        self.rowconfigure (6, weight = 1)
        self.character = character
    def landing_window(self):

        #label above progress bar
        progress_label = Label(self, text="Daily Progress")
        progress_label.grid(row = 4, column =2 ,sticky='ew', pady=4, padx=5)
        progress_label.configure(anchor = CENTER, font='arial 14 italic')
        progress_label.rowconfigure(4, weight =1)
        progress_label.columnconfigure(3, weight = 1)

        #progress bar
        progress = Progressbar(self, orient = 'horizontal', mode= 'determinate')
        progress.grid(row = 5, column=0, columnspan = 6, stick = 'ew', padx = 3)
        progress.start()
        progress.rowconfigure(5, weight =1)
        progress.columnconfigure(0, weight = 1)

        #three areas for adding dailies, task, habit widgets
        landing_frame_style = Style()
        landing_frame_style.configure("lf.TFrame", background = 'white')
        area1 = Frame(self, style = "lf.TFrame")
        area1.grid(row=6, column=0, columnspan=2, rowspan=4, 
            padx=5, sticky='enws')
        area1.rowconfigure(6, weight =1)
        area1.columnconfigure(0, weight = 1)

        area2 = Frame(self, style = "lf.TFrame")
        area2.grid(row=6, column=2, columnspan=2, rowspan=4, 
            padx=5, sticky='enws')
        area2.rowconfigure(6, weight =1)
        area2.columnconfigure(2, weight = 1)

        area3 = Frame(self, style = "lf.TFrame")
        area3.grid(row=6, column=4, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        area3.rowconfigure(6, weight =1)
        area3.columnconfigure(4, weight = 1)

        
    def start(self):
        self.progress["value"] = 0
        self.max = 24
        self.progress["midnight"]=24
        self.progress["value"] = 12
