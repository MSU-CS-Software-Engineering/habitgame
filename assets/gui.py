from tkinter  import *
from tkinter.ttk import *



from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class GUI(Frame):
  
    def __init__(self, master):
        Frame.__init__(self, master)   
        pad = 3
        self.master = master
        self._geom='800x600+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        self.initUI()
        
    def initUI(self):
        self.master.title("Daily Hack")
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

        

        mb=  Menubutton ( self, text="Options" )
        mb.grid(row = 0, column = 5, sticky = E)
        mb.menu  =  Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
    
        mayoVar  = IntVar()
        ketchVar = IntVar()
        mb.menu.add_command( label="Habits", command = habit)
        mb.menu.add_command( label="Dailies", command = dailies )
        mb.menu.add_command( label="Tasks", command = task )
        mb.menu.add_command( label="Shop", command = buy )
        mb.menu.add_command ( label="Game", command = no_where)
        mb.menu.add_command( label="Settings", command = no_where)

        footer = Label(self, text="Copyright 2014")
        footer.grid(row =9, columnspan = 7, sticky = (N, E, W, S))
        footer.configure(background = 'black', foreground = 'white', anchor = CENTER)

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

def habit():
    messagebox.showinfo("Placeholder", "I go to Habits work space!")

def task():
    messagebox.showinfo("Placeholder", "I go to Task work space!")

def dailies():
    messagebox.showinfo("Placeholder", "I got to goals work space!")
def buy():
    messagebox.showinfo("Placeholder", "I go to shop!")

def no_where():
    messagebox.showinfo("Placeholder", "I don't have anywher to go yet :( !")

 


