from tkinter  import *
from tkinter.ttk import *
from engine import *

class game(GUI):
    def __init__(self, master):
        GUI.__init__(self, master)
        self.master.title("Game")
        self.master = master
        self.game_window()
        
    def game_window(self):
        
        lbl = Label(self,text = "hello")
        lbl.grid(row=0, column = 3)
        
     

def main():
    
    game(Tk())

if __name__ == '__main__':
   main()
