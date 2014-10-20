from tkinter  import *
from tkinter.ttk import *
from shop import MyShop
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.




class Work_Space (Frame):

    def __init__(self, parent, character):
        Frame.__init__(self, parent)
        self.parent = parent
        self.work_window()
        
        self.rowconfigure(4, weight =1)
        self.columnconfigure(0, weight = 1)


    def work_window(self):
        #creating the workspace 

        frame = Notebook(self, height = 200, width = 400, padding=5)
        frame.grid(row=4, column = 0, columnspan = 7, rowspan = 4, sticky = 'nesw')
        frame_style = Style()
        frame_style.configure("W.TFrame", background='black',
                              height = 100, width = 800, pady = 100, padx = 300)
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

        habit = Canvas(tab_habit)
        habit.grid(sticky = 'news')
        #habit.grid_propagate(False)

        
        habits = Frame(habit)
        habits.grid(sticky = 'news')
        #habits.grid_propagate(False)



        bar_habit = Scrollbar(tab_habit, orient = VERTICAL, command = habit.yview)
        habit.configure(yscrollcommand = bar_habit.set)

        tab_habit.rowconfigure(0, weight = 1)
        tab_habit.columnconfigure(0, weight = 1)


        habit.create_window(0,20, anchor = N + E, window = habits)
        bar_habit.grid(row = 0, column = 1, sticky = 'ns')
        '''
        bar_dailies = Scrollbar(tab_dailies, orient = VERTICAL, command = tab_dailies.yview)
        tab_dailies.configure(yscrollcommand = bar_dailies.set)
        
        bar_tasks = Scrollbar(tab_tasks, orient = VERTICAL, command = tab_tasks.yview)
        tab_tasks.configure(yscrollcommand = bar_tasks.set)
        

        bar_tasks.pack(side = RIGHT, fill = Y)
        bar_dailies.pack(side = RIGHT, fill = Y)

        '''
        def setupHabitFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            habit.configure(scrollregion=habit.bbox("all"))


        habit.bind("<Configure>", setupHabitFrame)
        for x in range(15):
            individual_habit = Frame(habits, style = "W.TFrame")
            individual_habit.grid(row = x, column = 0,
                                  sticky = 'ew')

            

            habit_name = Label(individual_habit, text = "Hello Hello Hello")
            habit_name.grid(row = 0, column = 0, sticky = 'news')
            habit_name.configure(width = 130, anchor = CENTER)
            x = "This is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long sentence"

            habit_description = Label(individual_habit, text = x,
                                      wraplength = 800)
            habit_description.grid(row = 1, column = 0, sticky = 'ew')
            habit_description.configure(width = 130, anchor = CENTER)
        
        
        '''
        frame_habit = Frame(tab_habit)
        frame_habit.pack(side = LEFT, fill = BOTH)


        frame_tasks = Frame(tab_tasks)
        frame_tasks.pack(side = LEFT, fill = BOTH)

        frame_dailies = Frame(tab_dailies)
        frame_dailies.pack(side = LEFT, fill = BOTH)
        '''                               

        frame.add(tab_habit, text='Habits')
        frame.add(tab_tasks, text='Tasks')
        frame.add(tab_dailies, text='Dailies')
        frame.add(tab_shop, text='Shop')

        add_habit_btn = Button(habit, text='Add new habit', command = self.add_habit)
        add_task_btn = Button(tab_tasks, text='Add new task', command = self.add_task)
        add_goal_btn = Button(tab_dailies, text='Add new goal', command = self.add_goal)
        add_buy_btn = Button(tab_shop, text='Buy', command = self.buy)
        
        delete_habit_btn = Button(habit, text='Delete habit', command = self.delete_habit)
        delete_task_btn = Button(tab_tasks, text='Delete task', command = self.delete_task)
        delete_goal_btn = Button(tab_dailies, text='Delete goal', command = self.delete_goal)

        edit_habit_btn = Button(habit, text='Edit habit', command = self.edit_habit)
        edit_task_btn = Button(tab_tasks, text='Edit task', command = self.edit_task)
        edit_goal_btn = Button(tab_dailies, text='Edit goal', command = self.edit_goal)
        
        habit.create_window(-700,0,window = add_habit_btn)
        habit.create_window(-600,0,window = edit_habit_btn)
        habit.create_window(-500,0,window = delete_habit_btn)

        #add_habit_btn.grid(row = 0, column = 0, padx  =(385, 50), pady = 10)
        #delete_habit_btn.grid(row = 0, column = 1, padx = (0, 50))
        #edit_habit_btn.grid(row = 0, column = 2)
        #add_habit_btn.rowconfigure(0, weight = 1)
        #add_habit_btn.columnconfigure(0, weight = 1)
        MyShop.setShop(tab_shop)

        frame.select(tab_shop)
    


    def add_habit(self):
        self.gather_habit_data("habit")

    def add_task(self):
        self.gather_habit_data("task")

    def add_goal(self):
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

        cancelButton = Button(button_frame, text="Cancel", command=data_window.destroy)
        cancelButton.pack(side="left")

        confirmButton = Button(button_frame, text="Save", command=lambda: self.output_window_vals(habit_type,
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
    test=Work_Space(root)
    root.mainloop()
    #End Test

    #pass

if __name__ == '__main__':
    main()  
        
