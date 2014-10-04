from tkinter  import *
from tkinter.ttk import *


from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class Top(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        var = StringVar()
      
        self.parent.title("Daily Hack")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, pad=7)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(9, pad=7)
        
        lbl = Label(self, text="Player Name")
        lbl.grid(row = 0, column = 0, columnspan = 2,sticky=W, pady=4, padx=5)

        level = Label(self, text="LEVEL:")
        level.grid(row = 1, column =0 ,columnspan = 2,sticky=W, pady=4, padx=5)

        cash = Label(self, text="CASH:")
        cash.grid(row = 2, column =0 ,columnspan = 2,sticky=W, pady=4, padx=5)

        health = Label(self, text="HEALTH")
        health.grid(row = 3, column =0 ,columnspan = 2,sticky=W, pady=4, padx=5)

        progress_label = Label(self, text="Daily Progress")
        progress_label.grid(row = 3, column =3 ,sticky=W+ E+S + N, pady=4, padx=5)
        progress_label.configure(anchor = CENTER)
        
        
        progress = Progressbar(self, orient = 'horizontal', mode= 'determinate')
        
        progress.grid(row = 4, column=0, columnspan = 6, stick = E + W, padx = 3)
        progress.start()
        
        area1 = Canvas(self)
        area1.grid(row=5, column=0, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)

        area2 = Canvas(self)
        area2.grid(row=5, column=2, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)

        area3 = Canvas(self)
        area3.grid(row=5, column=4, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)



        mb=  Menubutton ( self, text="Options" )
        mb.grid(row = 0, column = 5, sticky = E)
        mb.menu  =  Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
    
        mayoVar  = IntVar()
        ketchVar = IntVar()
        mb.menu.add_command( label="Habits", command = call_work_space )
        mb.menu.add_command( label="Dailies", command = call_work_space  )
        mb.menu.add_command( label="Tasks", command = call_work_space  )
        mb.menu.add_command( label="Shop", command = call_work_space  )
        mb.menu.add_command ( label="Game", command = call_work_space  )
        mb.menu.add_command( label="Settings", command = call_work_space  )
        

        

        
        
        hbtn = Button(self, text="Help")
        hbtn.grid(row=9, column=0, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=9, column=3)

        footer = Label(self, text="Copyright 2014")
        footer.grid(row =9, columnspan = 7, sticky = (N, E, W, S))
        footer.configure(background = 'black', foreground = 'white', anchor = CENTER)
def start(self):
    self.progress["value"] = 0
    self.max = 24
    self.progress["midnight"]=24
    self.progress["value"] = 12

def call_work_space():
    work_space.run()
              

def main():
  
    root = Tk()
    root.geometry("1100x400+300+300")
    app = Top(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
        
