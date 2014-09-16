#Landing Page for Daily Hack
#Using tkinter.ttk b/c it allows for a better looking gui.
#some functionality varies between tkinter and ttk

from tkinter  import *
from tkinter.ttk import *
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class Application(Frame):              
    def __init__(self, master=None):
        Frame.__init__(self, master)   
        self.grid(sticky=N+S+W+E)                     
        self.top_frame()
        

    def top_frame(self):
        #Top window, this allows for resizing
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        
        self.rowconfigure(3,weight=1)
        self.columnconfigure(0,weight=1)

        
        top_frame = Frame(self)
        top_frame.grid(row=0,sticky='nesw')
       
        app_style = Style() #Necessary to stylize application.

        #Area for Program logo
        header = Label(top_frame, text = 'Daily Hack',
                       foreground='black')
        header.pack(side=LEFT)
        
        #Frame for all of the stats to show up
        stats =Frame(self)
        stats.grid(row=1,sticky='nesw')
        

        task_ratio = Label(stats, text = 'Stats: ')
        task_ratio.grid(row=0,column=0)
        cash = Label(stats, text = 'Cash: ')
        cash.grid(row=0,column=1)
        
        #Progress bar showing daily tasks completion at a glance
        #Example: Between 0001 and 0600 100% task completion = green
        #Example: Between 0600 and 1200 50% task completion = yello
        #Example: Between 1200 and 1800 0% task completion = red
        #This will likely consist of frames that color as the day goes on
        #progression will depend on time of day.
        #right now there is only one progress bar to for place holder
        
        daily_countdown_frame =Frame(self)
        daily_countdown_frame.grid(row=2,sticky='nesw')
        
        daily_timeline_header = Label(daily_countdown_frame,
                                      text = 'Daily Timeline',)
        daily_timeline_header.grid(row = 0, column = 0)

        time_line_progress = Progressbar(daily_countdown_frame,
                                             orient = "horizontal", length = 400,
                                             mode = "determinate")
        time_line_progress.grid(row = 1, column = 0)
        tl_label = Label(daily_countdown_frame, text = 'progress bar')
        tl_label.grid(row = 1, column = 0)
        

        #Habit frame broken into tabed areas that will list respective
        #habits, tasks, or goals
        habit_frame = Notebook(self, height = 200, width = 400, padding=5)
        habit_frame.grid(row=3, sticky=N+S+E+W)
        habit_frame.grid_rowconfigure(3, weight=1)
        

        app_style.configure("W.TFrame", background='white')

        tab_habit = Frame(habit_frame, style="W.TFrame")
        tab_task = Frame(habit_frame, style ="W.TFrame")
        tab_goal = Frame(habit_frame, style ="W.TFrame")

        habit_frame.add(tab_habit, text='Habits')
        habit_frame.add(tab_task, text='Tasks')
        habit_frame.add(tab_goal, text='Goals')

        add_habit_btn = Button(tab_habit, text='Add new habit', command = add_habit)
        add_task_btn = Button(tab_task, text='Add new task', command = add_task)
        add_goal_btn = Button(tab_goal, text='Add new goal', command = add_goal)

        add_habit_btn.place(relx=0.95, rely=0.95, anchor=SE)
        add_task_btn.place(relx=0.95, rely=0.95, anchor=SE)
        add_goal_btn.place(relx=0.95, rely=0.95, anchor=SE)

        habit1=Frame(tab_habit)
        habit1.grid()
                
        #standard bottom footer for contact infor, company info, and other
        bottom_frame =Frame(self)
        bottom_frame.grid(row=4, sticky=N+S+E+W)
        bottom_header = Label(bottom_frame, text = 'Copyright 2014',
                              foreground='black')
        bottom_header.pack()

def add_habit():
    messagebox.showinfo("Placeholder", "I'm an add_habit stub!")

def add_task():
    messagebox.showinfo("Placeholder", "I'm an add_task stub!")

def add_goal():
    messagebox.showinfo("Placeholder", "I'm an add_goal stub!")

app = Application()                       
app.master.title('Daily Hack')    
app.mainloop()




