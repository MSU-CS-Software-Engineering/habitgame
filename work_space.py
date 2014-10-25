from tkinter  import *
from tkinter.ttk import *
from shop import MyShop
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.




class Work_Space (Frame):

    def __init__(self, parent, character):
        Frame.__init__(self, parent)
        self.parent = parent
        self.character = character
        self.rowconfigure(4, weight =1)
        self.columnconfigure(0, weight = 1)
        self.work_window()
        
    def select_tab(self, tab):
        '''
        Used for selecting tab from an element
        outside of Work_Space
        '''
        tabs = {'task' : self.tab_tasks,
                'daily': self.tab_dailies,
                'habit': self.tab_habit,
                'shop' : self.tab_shop}
        try:
            self.frame.select(tabs[tab])
            
        except:
            messagebox.showerror("Error", "Couldn't change tabs")
            
    def work_window(self):
        habit_dict = self.character.habits
        tasks_dict = self.character.tasks
        dailies_dict = self.character.dailies
        #creating the workspace 

        frame = Notebook(self, height = 200, width = 400, padding=5)
        frame.grid(row=4, column = 0, columnspan = 7, rowspan = 4,
                   sticky = 'nesw')
        frame_style = Style()
        frame_style.configure("W.TFrame", background='black',
                              pady = (10,0), padx =3)
        frame.rowconfigure(4, weight = 1)
        frame.columnconfigure(0, weight = 1)
        #frame.grid_propagate(False)

        tab_habit = Canvas(frame, width=850, height=400)
        tab_dailies = Canvas(frame, width=850, height=400)
        tab_tasks = Canvas(frame, width=850, height=400)
        tab_shop = Canvas(frame, width=850, height=400)

        tab_habit.pack(fill = BOTH, expand = YES)
        tab_dailies.pack(fill = BOTH, expand = YES)
        tab_tasks.pack(fill = BOTH, expand = YES)
        tab_shop.pack(fill = BOTH, expand = YES)
        #Begining of Habit Tab Code
        habit = Canvas(tab_habit, background = 'black')
        habit.grid(sticky = 'news')

        
        habits = Frame(habit, style = "W.TFrame")
        habits.grid(sticky = 'news')

        bar_habit = Scrollbar(tab_habit, orient = VERTICAL,
                              command = habit.yview)
        habit.configure(yscrollcommand = bar_habit.set)

        tab_habit.rowconfigure(0, weight = 1)
        tab_habit.columnconfigure(0, weight = 1)


        habit.create_window(0,20, anchor = N + E, window = habits)
        bar_habit.grid(row = 0, column = 1, sticky = 'ns')

        def setupHabitFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            habit.configure(scrollregion=habit.bbox("all"))


        habit.bind("<Configure>", setupHabitFrame)
        for h in habit_dict:
            individual_habit = Frame(habits)
            individual_habit.grid(row = habit_dict[h].ID, column = 0,
                                  sticky = 'ew', pady = (10,0), padx = 3)

            

            habit_name = Label(individual_habit, text = habit_dict[h].title)
            habit_name.grid(row = 0, column = 0, sticky = 'ew', pady = 5)
            habit_name.configure(width = 130, anchor = CENTER)

            habit_description = Label(individual_habit, text = habit_dict[h].description,
                                      wraplength = 800)
            habit_description.grid(row = 1, column = 0, sticky = 'ew', pady = 5)
            habit_description.configure(width = 130, anchor = CENTER)

            habit_value = Label(individual_habit,
                                text = "Value:     "+str(habit_dict[h].value),
                                wraplength = 800)
            habit_value.grid(row = 2, column = 0, sticky = 'ew', pady = 5)
            habit_value.configure(width = 130, anchor = CENTER)

            habit_date = Label(individual_habit,
                               text = "Date:     "+str(habit_dict[h].timestamp),
                               wraplength = 800)
            habit_date.grid(row = 3, column = 0, sticky = 'ew', pady = 5)
            habit_date.configure(width = 130, anchor = CENTER)

            delete_habit_btn = Button(individual_habit, text='Delete habit',
                                      command = self.delete_habit)
            delete_habit_btn.grid(row = 1, column = 1,sticky = 'news', pady = 5)

            edit_habit_btn = Button(individual_habit, text='Edit habit',
                                    command = self.edit_habit)
            edit_habit_btn.grid (row = 2, column = 1,sticky = 'news', pady = 5)
            
            edit_habit_btn = Button(individual_habit, text='Complete habit',
                                    command = self.edit_habit)
            edit_habit_btn.grid (row = 0, column = 1,sticky = 'news', pady = 5)

        #Begining of Dailies Tab Code

        daily = Canvas(tab_dailies, background = 'black')
        daily.grid(sticky = 'news')

        
        dailies= Frame(daily, style = "W.TFrame")
        dailies.grid(sticky = 'news')

        bar_dailies = Scrollbar(tab_dailies, orient = VERTICAL,
                                command = daily.yview)
        daily.configure(yscrollcommand = bar_dailies.set)

        tab_dailies.rowconfigure(0, weight = 1)
        tab_dailies.columnconfigure(0, weight = 1)


        daily.create_window(0,20, anchor = N + E, window = dailies)
        bar_dailies.grid(row = 0, column = 1, sticky = 'ns')

        def setupDailiesFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            daily.configure(scrollregion=daily.bbox("all"))


        daily.bind("<Configure>", setupDailiesFrame)
        for d in dailies_dict:
            individual_dailies = Frame(dailies)
            individual_dailies.grid(row = dailies_dict[d].ID, column = 0,
                                  sticky = 'ew', pady = (10,0), padx = 3)

            

            dailies_title = Label(individual_dailies, text = dailies_dict[d].title)
            dailies_title.grid(row = 0, column = 0, sticky = 'ew', pady = 5)
            dailies_title.configure(width = 130, anchor = CENTER)

            dailies_description = Label(individual_dailies, text = dailies_dict[d].description,
                                      wraplength = 800)
            dailies_description.grid(row = 1, column = 0, sticky = 'ew', pady = 5)
            dailies_description.configure(width = 130, anchor = CENTER)

            dailies_value = Label(individual_dailies,
                                  text = "Value:     "+str(dailies_dict[d].value),
                                  wraplength = 800)
            dailies_value.grid(row = 2, column = 0, sticky = 'ew', pady = 5)
            dailies_value.configure(width = 130, anchor = CENTER)

            dailies_date = Label(individual_dailies,
                                 text = "Date:     "+str(dailies_dict[d].timestamp),
                                 wraplength = 800)
            dailies_date.grid(row = 3, column = 0, sticky = 'ew', pady = 5)
            dailies_date.configure(width = 130, anchor = CENTER)

            delete_dailies_btn = Button(individual_dailies, text='Delete Daily',
                                      command = self.delete_habit)
            delete_dailies_btn.grid(row = 1, column = 1,sticky = 'news', pady = 5)

            edit_dailies_btn = Button(individual_dailies, text='Edit Daily',
                                      command = self.edit_habit)
            edit_dailies_btn.grid (row = 2, column = 1,sticky = 'news', pady = 5)
            
            edit_dailies_btn = Button(individual_dailies, text='Complete Daily',
                                      command = self.edit_habit)
            edit_dailies_btn.grid (row = 0, column = 1,sticky = 'news', pady = 5)

        
        #Begining of Tasks Tab Code

        task = Canvas(tab_tasks, background = 'black')
        task.grid(sticky = 'news')

        
        tasks= Frame(task, style = "W.TFrame")
        tasks.grid(sticky = 'news')

        bar_tasks = Scrollbar(tab_tasks, orient = VERTICAL, command = task.yview)
        task.configure(yscrollcommand = bar_tasks.set)

        tab_tasks.rowconfigure(0, weight = 1)
        tab_tasks.columnconfigure(0, weight = 1)


        task.create_window(0,20, anchor = N + E, window = tasks)
        bar_tasks.grid(row = 0, column = 1, sticky = 'ns')

        def setupTasksFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            task.configure(scrollregion=task.bbox("all"))


        task.bind("<Configure>", setupTasksFrame)
        for t in tasks_dict:
            individual_tasks = Frame(tasks)
            individual_tasks.grid(row = tasks_dict[t].ID, column = 0,
                                  sticky = 'ew', pady = (10,0), padx = 3)

            

            tasks_title = Label(individual_tasks, text = tasks_dict[t].title)
            tasks_title.grid(row = 0, column = 0, sticky = 'ew', pady = 5)
            tasks_title.configure(width = 130, anchor = CENTER)

            tasks_description = Label(individual_tasks, text = tasks_dict[t].description,
                                      wraplength = 800)
            tasks_description.grid(row = 1, column = 0, sticky = 'ew', pady = 5)
            tasks_description.configure(width = 130, anchor = CENTER)

            tasks_value = Label(individual_tasks, text = "Value:     "+str(tasks_dict[t].value),
                                      wraplength = 800)
            tasks_value.grid(row = 2, column = 0, sticky = 'ew', pady = 5)
            tasks_value.configure(width = 130, anchor = CENTER)

            tasks_date = Label(individual_tasks,
                               text = "Date:     "+str(tasks_dict[t].timestamp),
                               wraplength = 800)
            tasks_date.grid(row = 3, column = 0, sticky = 'ew', pady = 5)
            tasks_date.configure(width = 130, anchor = CENTER)

            delete_tasks_btn = Button(individual_tasks, text='Delete Task',
                                      command = self.delete_habit)
            delete_tasks_btn.grid(row = 1, column = 1,sticky = 'news', pady = 5)

            edit_tasks_btn = Button(individual_tasks, text='Edit Task',
                                    command = self.edit_habit)
            edit_tasks_btn.grid (row = 2, column = 1,sticky = 'news', pady = 5)
            
            edit_tasks_btn = Button(individual_tasks, text='Complete Task',
                                    command = self.edit_habit)
            edit_tasks_btn.grid (row = 0, column = 1,sticky = 'news', pady = 5)


        frame.add(tab_habit, text='Habits')
        frame.add(tab_tasks, text='Tasks')
        frame.add(tab_dailies, text='Dailies')
        frame.add(tab_shop, text='Shop')

        add_habit_btn = Button(habit, text='Add new habit',
                               command = self.add_habit)
        add_task_btn = Button(task, text='Add new task',
                              command = self.add_task)
        add_daily_btn = Button(daily, text='Add new goal',
                               command = self.add_daily)
        add_buy_btn = Button(tab_shop, text='Buy', command = self.buy)
        
        
        habit.create_window(-675,0,window = add_habit_btn)
        daily.create_window(-675,0,window = add_daily_btn)
        task.create_window(-675,0,window = add_task_btn)
    
        #Set self.frame as local variable 'frame'
        self.frame = frame
        
        self.tab_tasks = tab_tasks
        self.tab_dailies = tab_dailies
        self.tab_shop = tab_shop
        self.tab_habit = tab_habit
        
        MyShop.setShop(self.tab_shop)
        self.frame.select(self.tab_shop)
        

    def add_habit(self):
        self.gather_habit_data("habit")

    def add_task(self):
        self.gather_habit_data("task")

    def add_daily(self):
        self.gather_habit_data("goal")
        
    def delete_habit(self):
        answer = messagebox.askokcancel("Delete Habit", "Delete habit?")
        if answer is True:
            print("User clicked Ok")
        else:
            print("User clicked Cancel")
            
    def delete_task(self):
        answer = messagebox.askokcancel("Delete Task", "Delete task?")
        if answer is True:
            print("User clicked Ok")
        else:
            print("User clicked Cancel")

    def delete_goal(self):
        answer = messagebox.askokcancel("Delete Goal", "Delete goal?")
        if answer is True:
            print("User clicked Ok")
        else:
            print("User clicked Cancel")
            
    def edit_habit(self):
        messagebox.showinfo("Updated Habit", "Habit updated.")

    def edit_task(self):
        messagebox.showinfo("Updated Task", "Task updated.")

    def edit_goal(self):
        messagebox.showinfo("Updated Goal", "Goal updated.")

    def buy(self):
        messagebox.showinfo("Placeholder", "I'm a buy stub!")             

    def gather_habit_data(self, habit_type):
        #Create Window
        #Take information
        #Check for info if 'save' is clicked. Discard if 'cancel' is clicked.
        #Add habit/Daily/Task to list

        data_window = Toplevel(self)

        #Name of habit\daily\task
        name_frame = Frame(data_window)
        name_frame.pack(side="top")

        name_label = Label(name_frame, text="Name")
        name_label.pack(side="top", padx=10, pady=10)

        ticket_name = Entry(name_frame)
        ticket_name.pack(side="bottom", pady=10)

        #Description
        desc_frame = Frame(data_window)
        desc_frame.pack(side="top")

        desc_label = Label(desc_frame, text="Description")
        desc_label.pack(side="top", padx=10)

        ticket_desc = Text(desc_frame, width=40, height=4)
        ticket_desc.pack(side="bottom", padx=10, pady=10)

        #Value
        value_frame = Frame(data_window)
        value_frame.pack(side="top")

        value_label = Label(value_frame, text="Reward Value")
        value_label.pack(side="top", padx=10, pady=10)

        ticket_value = Entry(value_frame)
        ticket_value.pack(side="bottom")

        #Buttons
        button_frame = Frame(data_window, width=100)
        button_frame.grid_propagate(100)
        button_frame.pack(side="bottom", padx=10, pady=10)

        cancelButton = Button(button_frame, text="Cancel",
                              command=data_window.destroy)
        cancelButton.pack(side="left")

        confirmButton = Button(button_frame, text="Save",
                               command=lambda: self.output_window_vals(habit_type,
                                                                       ticket_name.get(),
                                                                       ticket_desc.get(1.0, END).strip('\t\n'),
                                                                       ticket_value.get()))
        confirmButton.pack(side="right")

    def output_window_vals(self, ticket_type, ticket_name, ticket_desc, ticket_value):
        values = [ticket_type, ticket_name, ticket_desc, ticket_value]
        print(values)
        #return values

def main():
    #For Testing purposes
    root = Tk()
    test = Work_Space(root)
    root.mainloop()
    #End Test

    #pass

if __name__ == '__main__':
    main()  
        
