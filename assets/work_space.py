from tkinter  import *
from tkinter.ttk import *
from gui import *
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class Work_Space(GUI):
  
    def __init__(self, master):
        GUI.__init__(self, master)   
         
        self.master = master
        
        self.work_window()
        
        
    def work_window(self):
        #creating the workspace 
        
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

        
def add_habit():
    messagebox.showinfo("Placeholder", "I'm an add_habit stub!")

def add_task():
    messagebox.showinfo("Placeholder", "I'm an add_task stub!")

def add_goal():
    messagebox.showinfo("Placeholder", "I'm an add_goal stub!")
def buy():
    messagebox.showinfo("Placeholder", "I'm a buy stub!")             

def main():
  
    Work_Space(Tk())


if __name__ == '__main__':
    main()  
        
