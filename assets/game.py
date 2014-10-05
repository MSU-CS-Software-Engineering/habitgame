from tkinter  import *
from tkinter.ttk import *
from gui import *

class game (GUI):
    def __init__(self, master):
        GUI.__init__(self, master)
        self.master.title("Game")
        self.master = master
        self.game_window()
        
    def game_window(self):
        self.master.geometry("800x600+300+300")
        self.master.lbl = Label(self,text = "hello")
        self.master.lbl.grid(row=0, column = 3)
        
     

def main():
    
    game(Tk())

if __name__ == '__main__':
   main()
