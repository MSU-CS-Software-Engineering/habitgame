from tkinter  import *
from tkinter.ttk import *


from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class Landing_Page (Frame):
    def __init__(self, parent, character):
        Frame.__init__(self, parent)
        
        
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


        habit_list = self.character.habits
        tasks_list = self.character.tasks
        dailies_list = self.character.dailies
        
        
        
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

        habit_frame_style = Style()
        habit_frame_style.configure("hf.TFrame", background = 'red', height = 100)

        area1 = Frame(self, style = "lf.TFrame")
        area1.grid(row=6, column=0, columnspan=2, 
            padx=5, sticky='enws')
        area1.grid_propagate(False)
        area1.rowconfigure(6, weight =1)
        area1.columnconfigure(0, weight = 1)
        habit_list = self.character.habits
        counter = 0
    
        for habit in habit_list:
            if counter < 5:
                habit_frame = Frame(area1, style="hf.TFrame", height = 100)
                habit_frame.grid(row = habit.ID, column = 0, sticky = 'new',pady = (3,0), padx = 3)

                habit_name = Label(habit_frame, text = habit.title, anchor = CENTER)
                habit_name.pack(fill = X, expand = True)
                x = "This is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long sentence"

                habit_description = Label (habit_frame, text = x, wraplength = 375,
                                           justify = LEFT)
                habit_description.pack(fill = X, expand = True)


                habit_value=Label(habit_frame, text ="Value:     " + str(habit.value))
                habit_value.pack (fill = X, expand = True)
                habit_date_time = Label(habit_frame, text ="Date/Time:     "+str(habit.timestamp) )
                habit_date_time.pack(fill = X, expand = True)

                def function_builder(args):
                    messagebox.showinfo("Place Holder", "go to " + args)
                    
                complete_button = Button(habit_frame,
                                         text='COMPLETE '+habit.title,
                                         command = self.complete)
                complete_button.pack(fill = X, expand = True, side = BOTTOM)

                



                
                    


                
                
            
        
        
   

    



            counter += 1

        area2 = Frame(self, style = "lf.TFrame")
        area2.grid(row=6, column=2, columnspan=2, 
            padx=5, sticky='enws')
        area2.rowconfigure(6, weight =1)
        area2.columnconfigure(2, weight = 1)

 


        

        area3 = Frame(self, style = "lf.TFrame")
        area3.grid(row=6, column=4, columnspan=2, 
            padx=5, sticky=E+W+S+N)
        area3.rowconfigure(6, weight =1)
        area3.columnconfigure(4, weight = 1)



        #Bottom go to buttons
        go_to_habits = Button(area1, text='GO TO HABITS', command = self.to_habits)
        go_to_dailies = Button(area2, text='GO TO DAILIES', command = self.to_tasks)
        go_to_tasks = Button(area3, text='GO TO TASKS', command = self.to_dailies)
        go_to_habits.grid(row = 10, column = 0, sticky = 'ews')
        #go_to_habits.pack(fill = X, side = 'bottom', expand = True, anchor = S)
        go_to_dailies.pack(fill = X, side = 'bottom', expand = True, anchor = S)
        go_to_tasks.pack(fill = X, side = 'bottom', expand = True, anchor = S)

        
    def start(self):
        self.progress["value"] = 0
        self.max = 24
        self.progress["midnight"]=24
        self.progress["value"] = 12

        
    def to_habits(self):
        pass
        

    def to_dailies(self):
        pass
        

    def to_tasks(self):
        pass

    def complete(self):
        messagebox.showinfo("Placeholder", "I completed something")
