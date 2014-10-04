from tkinter  import *
from tkinter.ttk import *

from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class Work_Space(Frame):
  
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

        #Habit frame broken into tabed areas that will list respective
        #habits, tasks, or goals
        
        habit_frame = Notebook(self, height = 200, width = 400, padding=5)
        habit_frame.grid(row=4, column = 0, columnspan = 6, rowspan= 4,sticky='nesw')
        habit_frame_style = Style()
        habit_frame_style.configure("W.TFrame", background='white')

        tab_habit = Frame(habit_frame, style="W.TFrame")
        tab_task = Frame(habit_frame, style ="W.TFrame")
        tab_goal = Frame(habit_frame, style ="W.TFrame")
        tab_shop = Frame(habit_frame, style = "W.TFrame")

        habit_frame.add(tab_habit, text='Habits')
        habit_frame.add(tab_task, text='Tasks')
        habit_frame.add(tab_goal, text='Goals')
        habit_frame.add(tab_shop, text='Shop')

        add_habit_btn = Button(tab_habit, text='Add new habit', command = add_habit)
        add_task_btn = Button(tab_task, text='Add new task', command = add_task)
        add_goal_btn = Button(tab_goal, text='Add new goal', command = add_goal)
        add_buy_btn = Button(tab_shop, text='Buy', command = buy)

        add_habit_btn.place(relx=0.95, rely=0.95, anchor=SE)
        add_task_btn.place(relx=0.95, rely=0.95, anchor=SE)
        add_goal_btn.place(relx=0.95, rely=0.95, anchor=SE)
        add_buy_btn.place(relx=0.95, rely=0.95, anchor=SE)

        habit1=Frame(tab_habit)
        habit1.grid()

        


        

      



        mb=  Menubutton ( self, text="Options" )
        mb.grid(row = 0, column = 5, sticky = E)
        mb.menu  =  Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
    
        mayoVar  = IntVar()
        ketchVar = IntVar()
        mb.menu.add_command( label="Habits" )
        mb.menu.add_command( label="Dailies" )
        mb.menu.add_command( label="Tasks" )
        mb.menu.add_command( label="Shop" )
        mb.menu.add_command ( label="Game" )
        mb.menu.add_command( label="Settings" )
        

        

        
        
        hbtn = Button(self, text="Help")
        hbtn.grid(row=9, column=0, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=9, column=3)

        footer = Label(self, text="Copyright 2014")
        footer.grid(row =9, columnspan = 7, sticky = (N, E, W, S))
        footer.configure(background = 'black', foreground = 'white', anchor = CENTER)

def add_habit():
    messagebox.showinfo("Placeholder", "I'm an add_habit stub!")

def add_task():
    messagebox.showinfo("Placeholder", "I'm an add_task stub!")

def add_goal():
    messagebox.showinfo("Placeholder", "I'm an add_goal stub!")
def buy():
    messagebox.showinfo("Placeholder", "I'm a buy stub!")
              

def main():
  
    root = Tk()
    root.geometry("1100x400+300+300")
    app = Work_Space(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
        
