import os.path
from tkinter  import *
from tkinter.ttk import *

from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class Landing_Page (Frame):
    
    def __init__(self, parent, character):
        
        Frame.__init__(self, parent)

        self.to_habits = parent.habit
        self.to_tasks = parent.task
        self.to_dailies = parent.dailies
        
        self.character = character
        self.columnconfigure(0, weight =1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 1)
        #self.columnconfigure(3, weight = 1)
        #self.rowconfigure (4, weight =1)
        #self.rowconfigure (5, weight = 1)
        self.rowconfigure (6, weight = 1)
        self.landing_window()
        
        
    def landing_window(self):

        habit_dict =   {k:self.character.hacks[k] 
                        for k in self.character.hacks 
                          if self.character.hacks[k].h_type == 'habit'}
        dailies_dict = {k:self.character.hacks[k] 
                        for k in self.character.hacks 
                          if self.character.hacks[k].h_type == 'daily'}
        tasks_dict =   {k:self.character.hacks[k] 
                        for k in self.character.hacks 
                          if self.character.hacks[k].h_type == 'task'}

        # apply this to all completion buttons
        complete_img = PhotoImage(file=os.path.join("assets", "art", "check.gif"))
        
        #label above progress bar
        progress_label = Label(self, text="Daily Progress", padding=0)
        progress_label.grid(row = 4, column = 0, columnspan = 5, sticky='ew', pady=4, padx=5)
        progress_label.configure(anchor = CENTER, font='arial 18 italic')
        progress_label.rowconfigure(4, weight =1)
        progress_label.columnconfigure(3, weight = 1)

        #progress bar
        #progress = Progressbar(self, orient = 'horizontal', mode= 'determinate')
        #progress.grid(row = 5, column=0, columnspan = 6, stick = 'ew', padx = 3)

        #progress.start()
        #progress.rowconfigure(5, weight =1)
        #progress.columnconfigure(0, weight = 1)

        #three areas for adding dailies, task, habit widgets
        landing_frame_style = Style()
        landing_frame_style.configure("lf.TFrame", background = '#EBEDF1')

        habit_frame_style = Style()
        habit_frame_style.configure("hf.TFrame", height = 100)

        area1 = Frame(self, style = "lf.TFrame")
        area1.grid(row = 6, column = 0, columnspan = 2, rowspan = 4, 
            padx = 5, sticky = 'enws')
        area1.grid_propagate(False)
        area1.rowconfigure(6, weight = 1)
        area1.columnconfigure(0, weight = 1)

        counter = 0

        habit_header = Label(area1, text = "HABITS", anchor = CENTER, font = "Veranda 18 bold",
                             foreground = 'black', background = '#D95B5B')
        habit_header.grid(row = 0, column = 0, sticky = 'new',pady = (3,0), padx = 3)

        area2 = Frame(self, style = "lf.TFrame")
        area2.grid(row = 6, column = 2, columnspan = 2, rowspan = 4, 
            padx = 5, sticky = 'enws')
        area2.rowconfigure(6, weight = 1)
        area2.columnconfigure(2, weight = 1)
        area2.grid_propagate(False)

        dailies_header = Label(area2, text = "DAILIES", anchor = CENTER, font = "Veranda 18 bold",
                               foreground = 'black', background = '#9AD95B')
        dailies_header.grid(row = 0, column = 2, sticky = 'new',pady = (3,0), padx = 3)

        area3 = Frame(self, style = "lf.TFrame")
        area3.grid(row = 6, column = 4, columnspan = 2, rowspan = 4, 
            padx = 5, sticky = 'news')
        area3.rowconfigure(6, weight = 1)
        area3.columnconfigure(4, weight = 1)
        area3.grid_propagate(False)

        tasks_header = Label(area3, text = "TASKS", anchor = CENTER, font = "Veranda 18 bold",
                             foreground = 'black', background = '#5BADD9')
        tasks_header.grid(row = 0, column = 4, sticky = 'new',pady = (3,0), padx = 3)

        #Habits Code Area
        if len(habit_dict) > 4:
            number = 5
        elif len(habit_dict) == 0:
                number = 0
            
                habit_frame = Frame(area1, style="hf.TFrame")
                habit_frame.grid(row = 1, column = 0, sticky = 'news',pady = (3,0), padx = 3)

                habit_name = Label(habit_frame, text = "No Habits to Display", anchor = CENTER)
                habit_name.pack(fill = X, expand = True)
        else:
            number = len(habit_dict)

        if number != 0:

            for x in habit_dict.keys():
                habit = habit_dict[x]
                habit_frame = Frame(area1, style = "hf.TFrame", height = 100)
                habit_frame.grid(row = habit.ID + 1, column = 0,
                                        sticky = 'new', pady = (3,0), padx = 3)

                habit_name = Label(habit_frame, text = habit.title, anchor = CENTER,
                                   background = "#F9D386", font = "Veranda 16 bold")
                habit_name.pack(fill = X, expand = True)

                habit_description = Label (habit_frame, text = "Note: " + habit.description, wraplength = 375,
                                           background = "#EFE4B0", font = "arial 12", padding = 5, justify = LEFT)
                habit_description.pack(fill = X, expand = True)

                habit_value=Label(habit_frame, text ="Value: " + str(habit.value), font = "arial 12",
                                  padding = 5, background = "#EFE4B0")
                habit_value.pack (fill = X, expand = True)
                habit_date_time = Label(habit_frame, text ="Date/Time: "+str(habit.timestamp), font = "arial 12",
                                        padding = 5, background = "#EFE4B0")

                habit_date_time.pack(fill = X, expand = True)

                def function_builder(args):
                    messagebox.showinfo("Place Holder", "go to " + args)

                def remove(top, habitID):
                    self.character.complete_hack(habitID)
                    top.destroy()

                complete_button = Button(habit_frame, style = 'complete_habit.TButton')
                complete_button.configure(text = 'COMPLETE ' + habit.title, image = complete_img,
                                          compound="left", cursor = 'hand2',
                                          command = lambda top = habit_frame,
                                          habitID = habit.ID : remove(top, habitID))
                complete_button.pack(fill = X, expand = True, side = BOTTOM)
                complete_button.image = complete_img
                

        #Dailies landing area
        if len(dailies_dict) > 4:
            number = 5
        elif len(dailies_dict) == 0:
                number = 0
            
                dailies_frame = Frame(area2, style = "hf.TFrame")
                dailies_frame.grid(row = 1, column = 2, sticky = 'news',pady = (3,0), padx = 3)

                dailies_name = Label(dailies_frame, text = "No Habits to Display",
                                     anchor = CENTER)
                dailies_name.pack(fill = BOTH, expand = True)
        else:
            number = len(dailies_dict)

        if number != 0:
            for x in dailies_dict.keys():
                dailies = dailies_dict[x]
                dailies_frame = Frame(area2, style = "hf.TFrame", height = 100)
                dailies_frame.grid(row = dailies.ID + 1, column = 2,
                                   sticky = 'new',pady = (3,0), padx = 3)

                dailies_name = Label(dailies_frame, text = dailies.title, background = "#F9D386",
                                     anchor = CENTER, font = "Veranda 16 bold")
                dailies_name.pack(fill = X, expand = True)

                dailies_description = Label(dailies_frame, text = "Note: " + dailies.description, 
                                             wraplength = 375, font = "arial 12", padding = 5, background = "#EFE4B0",
                                             justify = LEFT)
                dailies_description.pack(fill = X, expand = True)


                dailies_value=Label(dailies_frame, text ="Value: " + str(dailies.value),
                                    font = "arial 12", padding = 5, background = "#EFE4B0")
                dailies_value.pack (fill = X, expand = True)
                dailies_date_time = Label(dailies_frame, text ="Date/Time: "+str(dailies.timestamp),
                                          font = "arial 12", padding = 5, background = "#EFE4B0")
                dailies_date_time.pack(fill = X, expand = True)

                def function_builder(args):
                    messagebox.showinfo("Place Holder", "go to " + args)

                def remove_d(top, taskID):
                    self.character.complete_hack(taskID)
                    top.destroy()
                    
                complete_button = Button(dailies_frame, style = 'complete_dailies.TButton',
                                         cursor = 'hand2', text = 'COMPLETE ' + dailies.title,
                                         image = complete_img, compound="left",
                                         command = lambda top = dailies_frame,
                                         dailyID = dailies.ID : remove_d(top, dailyID))
                complete_button.pack(fill = X, expand = True, side = BOTTOM)
                complete_button.image = complete_img
                

        #Tasks
        if len(tasks_dict) > 4:
            number = 5
        elif len(tasks_dict) == 0:
                number = 0
            
                task_frame = Frame(area3, style="hf.TFrame")
                task_frame.grid(row = 1, column = 4,rowspan = 4,
                                sticky = 'news',pady = (3,0), padx = 3)

                task_name = Label(task_frame, text = "No Habits to Display",
                                  anchor = CENTER, font = "Veranda 16 bold")
                task_name.pack(fill = BOTH, expand = True)
        else:
            number = len(tasks_dict)
            
        if number != 0:
            for x in tasks_dict.keys():
                task = tasks_dict[x]
                
                task_frame = Frame(area3, style="hf.TFrame", height = 100)
                task_frame.grid(row = task.ID+1, column = 4, sticky = 'new',pady = (3,0), padx = 3)

                task_name = Label(task_frame, text = task.title, background = "#F9D386",
                                  anchor = CENTER, font = "Veranda 16 bold")
                task_name.pack(fill = X, expand = True)
                x = ("This is a very very very very very very very very " 
                    "very very very very very very very very very very "  
                    "very very very very very very very very very very "  
                    "very very very very very very very very long sentence")

                task_description = Label(task_frame, text = "Note: " + x, wraplength = 375,
                                         font = "arial 12", padding = 5,
                                         background = "#EFE4B0", justify = LEFT)
                task_description.pack(fill = X, expand = True)


                task_value=Label(task_frame, text ="Value: " + str(task.value),
                                 font = "arial 12", padding = 5, background = "#EFE4B0")
                task_value.pack(fill = X, expand = True)
                task_date_time = Label(task_frame, text ="Date/Time: " + str(task.timestamp),
                                       font = "arial 12", padding = 5, background = "#EFE4B0")
                task_date_time.pack(fill = X, expand = True)

                def function_builder(args):
                    messagebox.showinfo("Place Holder", "go to " + args)

                def remove_t(top, taskID):
                    self.character.complete_hack(taskID)
                    top.destroy()
                    
                complete_button = Button(task_frame, style = 'complete_task.TButton',
                                         cursor = 'hand2', text='COMPLETE ' + task.title,
                                         image = complete_img, compound="left",
                                         command = lambda top = task_frame,
                                         taskID = task.ID : remove_t(top, taskID))
                complete_button.pack(fill = X, expand = True, side = BOTTOM)
                complete_button.image = complete_img
                
        #Bottom go to buttons
        go_to_habits = Button(area1, text = 'GO TO HABITS', style = 'go_habits.TButton',
                              cursor = 'hand2', command = self.to_habits)
        go_to_dailies = Button(area2, text = 'GO TO DAILIES', style = 'go_dailies.TButton',
                               cursor = 'hand2', command = self.to_tasks)
        go_to_tasks = Button(area3, text='GO TO TASKS', style = 'go_tasks.TButton',
                             cursor = 'hand2', command = self.to_dailies)
        
        go_to_habits.grid(row = 10, column = 0, sticky = 'ews')
        #go_to_habits.pack(fill = X, side = 'bottom', expand = True, anchor = S)
        go_to_dailies.pack(fill = X, side = 'bottom', expand = True, anchor = S)
        go_to_tasks.pack(fill = X, side = 'bottom', expand = True, anchor = S)

        # style completion buttons for habits, dailies, and tasks
        landing_frame_style.configure('complete_habit.TButton', font = 'arial 12 bold', relief = 'flat',
                                      padding = '0 3 0 3', foreground = 'black', background = '#C6E29A')
        landing_frame_style.configure('complete_dailies.TButton', font = 'arial 12 bold', relief = 'flat',
                                      padding = '0 3 0 3', foreground = 'black', background = '#C6E29A')
        landing_frame_style.configure('complete_task.TButton', font = 'arial 12 bold', relief = 'flat',
                                      padding = '0 3 0 3', foreground = 'black', background = '#C6E29A')
        
        # style the go to buttons; habits, dailies, and tasks
        landing_frame_style.configure('go_habits.TButton', font = 'arial 14 bold', relief = 'flat',
                                      padding = 5, foreground = '#54C9EB', background = '#283D57')
        landing_frame_style.configure('go_dailies.TButton', font = 'arial 14 bold', relief = 'flat',
                                      padding = 5, foreground = '#54C9EB', background = '#283D57')
        landing_frame_style.configure('go_tasks.TButton', font = 'arial 14 bold', relief = 'flat',
                                      padding = 5, foreground = '#54C9EB', background = '#283D57')


    def start(self):

        self.progress["value"] = 0
        self.max = 24
        self.progress["midnight"]=24
        self.progress["value"] = 12

