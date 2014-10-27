from tkinter  import *
from tkinter.ttk import *

from engine import Hack
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
        tabs = {
                'task' : self.tab_tasks,
                'daily': self.tab_dailies,
                'habit': self.tab_habit,
                'shop' : self.tab_shop
               }
        try:
            self.frame.select(tabs[tab])
            
        except:
            messagebox.showerror("Error", "Couldn't change tabs")
            
    def work_window(self):
        hack_dict = self.character.hacks

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
        for h in [hack for hack in hack_dict if hack_dict[hack].h_type == 'habit']: #Gather habit-type hacks from dict
            individual_habit = Frame(habits)
            individual_habit.grid(row = hack_dict[h].ID, column = 0,
                                  sticky = 'ew', pady = (10,0), padx = 3)

            habit_name = Label(individual_habit, text = hack_dict[h].title)
            habit_name.grid(row = 0, column = 0, sticky = 'ew', pady = 5)
            habit_name.configure(width = 130, anchor = CENTER)

            habit_description = Label(individual_habit, text = hack_dict[h].description,
                                      wraplength = 800)
            habit_description.grid(row = 1, column = 0, sticky = 'ew', pady = 5)
            habit_description.configure(width = 130, anchor = CENTER)

            habit_value = Label(individual_habit,
                                text = "Value:     " + str(hack_dict[h].value),
                                wraplength = 800)
            habit_value.grid(row = 2, column = 0, sticky = 'ew', pady = 5)
            habit_value.configure(width = 130, anchor = CENTER)

            habit_date = Label(individual_habit,
                               text = "Date:     " + str(hack_dict[h].timestamp),
                               wraplength = 800)
            habit_date.grid(row = 3, column = 0, sticky = 'ew', pady = 5)
            habit_date.configure(width = 130, anchor = CENTER)

            delete_habit_btn = Button(individual_habit, text='Delete habit',
                command = lambda h=h: self.delete_hack(h))
            delete_habit_btn.grid(row = 1, column = 1,sticky = 'news', pady = 5)

            edit_habit_btn = Button(individual_habit, text='Edit habit',
                command = lambda h=h: self.edit_hack(h) )
            edit_habit_btn.grid (row = 2, column = 1,sticky = 'news', pady = 5)
            
            edit_habit_btn = Button(individual_habit, text='Complete habit',
                command = lambda h=h: self.edit_hack(h)) #FIX ME -D
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
        for d in [hack for hack in hack_dict if hack_dict[hack].h_type == 'daily']:  #Gather dailies from dict
            individual_dailies = Frame(dailies)
            individual_dailies.grid(row = hack_dict[d].ID, column = 0,
                                  sticky = 'ew', pady = (10,0), padx = 3)

            dailies_title = Label(individual_dailies, text = hack_dict[d].title)
            dailies_title.grid(row = 0, column = 0, sticky = 'ew', pady = 5)
            dailies_title.configure(width = 130, anchor = CENTER)

            dailies_description = Label(individual_dailies, text = hack_dict[d].description,
                                      wraplength = 800)
            dailies_description.grid(row = 1, column = 0, sticky = 'ew', pady = 5)
            dailies_description.configure(width = 130, anchor = CENTER)

            dailies_value = Label(individual_dailies,
                                  text = "Value:     " + str(hack_dict[d].value),
                                  wraplength = 800)
            dailies_value.grid(row = 2, column = 0, sticky = 'ew', pady = 5)
            dailies_value.configure(width = 130, anchor = CENTER)

            dailies_date = Label(individual_dailies,
                                 text = "Date:     " + str(hack_dict[d].timestamp),
                                 wraplength = 800)
            dailies_date.grid(row = 3, column = 0, sticky = 'ew', pady = 5)
            dailies_date.configure(width = 130, anchor = CENTER)

            delete_dailies_btn = Button(individual_dailies, text='Delete Daily',
                command = lambda d=d: self.delete_hack(d))
            delete_dailies_btn.grid(row = 1, column = 1,sticky = 'news', pady = 5)

            edit_dailies_btn = Button(individual_dailies, text='Edit Daily',
                command = lambda d=d: self.edit_hack(d))
            edit_dailies_btn.grid (row = 2, column = 1,sticky = 'news', pady = 5)
            
            edit_dailies_btn = Button(individual_dailies, text='Complete Daily',
                command = lambda d=d: self.edit_hack(d)) #FIX ME -D
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
        for t in [hack for hack in hack_dict if hack_dict[hack].h_type == 'task']: #Gather tasks from dict
            individual_tasks = Frame(tasks)
            individual_tasks.grid(row = hack_dict[t].ID, column = 0,
                                  sticky = 'ew', pady = (10,0), padx = 3)

            tasks_title = Label(individual_tasks, text = hack_dict[t].title)
            tasks_title.grid(row = 0, column = 0, sticky = 'ew', pady = 5)
            tasks_title.configure(width = 130, anchor = CENTER)

            tasks_description = Label(individual_tasks, text = hack_dict[t].description,
                                      wraplength = 800)
            tasks_description.grid(row = 1, column = 0, sticky = 'ew', pady = 5)
            tasks_description.configure(width = 130, anchor = CENTER)

            tasks_value = Label(individual_tasks, text = "Value:     " + str(hack_dict[t].value),
                                      wraplength = 800)
            tasks_value.grid(row = 2, column = 0, sticky = 'ew', pady = 5)
            tasks_value.configure(width = 130, anchor = CENTER)

            tasks_date = Label(individual_tasks,
                               text = "Date:     " + str(hack_dict[t].timestamp),
                               wraplength = 800)
            tasks_date.grid(row = 3, column = 0, sticky = 'ew', pady = 5)
            tasks_date.configure(width = 130, anchor = CENTER)

            delete_tasks_btn = Button(individual_tasks, text='Delete Task',
                command = lambda t=t: self.delete_hack(t))
            delete_tasks_btn.grid(row = 1, column = 1,sticky = 'news', pady = 5)

            edit_tasks_btn = Button(individual_tasks, text='Edit Task',
                command = lambda t=t: self.edit_hack(t))
            edit_tasks_btn.grid (row = 2, column = 1,sticky = 'news', pady = 5)
            
            edit_tasks_btn = Button(individual_tasks, text='Complete Task',
                command =lambda t=t: self.edit_hack(t)) #FIX ME -D
            edit_tasks_btn.grid (row = 0, column = 1,sticky = 'news', pady = 5)


        frame.add(tab_habit, text='Habits')
        frame.add(tab_tasks, text='Tasks')
        frame.add(tab_dailies, text='Dailies')
        frame.add(tab_shop, text='Shop')

        add_habit_btn = Button(habit, text='Add new habit',
                               command = lambda: self.add_hack('habit'))
        add_task_btn = Button(task, text='Add new task',
                               command = lambda: self.add_hack('task'))
        add_daily_btn = Button(daily, text='Add new daily',
                               command = lambda: self.add_hack('daily'))
        add_buy_btn = Button(tab_shop, text='Buy', command = self.buy)
        
        habit.create_window(-675, 0, window  =  add_habit_btn)
        daily.create_window(-675, 0, window  =  add_daily_btn)
        task.create_window(-675,  0, window  =  add_task_btn)

        #Set self.frame as local variable 'frame'
        self.frame = frame
        
        self.tab_tasks = tab_tasks
        self.tab_dailies = tab_dailies
        self.tab_shop = tab_shop
        self.tab_habit = tab_habit
        
        MyShop.setShop(self.tab_shop)
        self.frame.select(self.tab_shop)
        

    def add_hack(self, h_type):
        ''' Calls input window; Adds result to hack list '''
        new_hack = self.input_hack_data(h_type)
        self.character.add_hack(new_hack)
        #REBUILD_HACK_LIST_ON_GUI
        
    def delete_hack(self, hack_ID):
        answer = messagebox.askokcancel("Delete Hack", "Delete hack?")
        if answer is True:
            print("Deleting ", hack_ID, "...")  #TEST PLEASE REMOVE
            self.character.remove_hack(hack_ID)
            #REBUILD_HACK_LIST_ON_GUI() 
        else:
            #print("User clicked Cancel")
            return False

            
    def edit_hack(self, hack_ID):
        try:
            hack_data = self.character.get_hack(hack_ID)
            self.input_hack_data(hack_data.h_type, hack_data)
            #REBUILD_HACK_LIST_ON_GUI()
        except:
            print("Failed to pass hack to input_hack_data")


    def buy(self):
        messagebox.showinfo("Placeholder", "I'm a buy stub!")             


    def input_hack_data(self, h_type, hack_data = None):
        data_window = Toplevel(self)

        #Name of habit\daily\task
        name_frame = Frame(data_window)
        name_frame.pack(side="top")

        name_label = Label(name_frame, text="Name")
        name_label.pack(side="top", padx=10, pady=10)

        ticket_name = Entry(name_frame, justify=CENTER)
        ticket_name.pack(side="bottom", pady=10)

        #Description
        desc_frame = Frame(data_window)
        desc_frame.pack(side="top")

        desc_label = Label(desc_frame, text="Description")
        desc_label.pack(side="top", padx=10)

        ticket_desc = Text(desc_frame, width=40, height=4)
        ticket_desc.insert(INSERT, hack_data.description)
        ticket_desc.pack(side="bottom", padx=10, pady=10)

        #Value
        value_frame = Frame(data_window)
        value_frame.pack(side="top")

        value_label = Label(value_frame, text="Reward Value")
        value_label.pack(side="top", padx=10, pady=10)

        ticket_value = Entry(value_frame, justify=CENTER)
        ticket_value.pack(side="bottom")

        #Buttons
        button_frame = Frame(data_window, width=100)
        button_frame.grid_propagate(100)
        button_frame.pack(side="bottom", padx=10, pady=10)

        cancelButton = Button(button_frame, text="Cancel",
                              command=data_window.destroy)
        cancelButton.pack(side="left")

        if hack_data == None:
            confirmButton = Button(button_frame, text="Save",
                command=lambda: 
                    self.save_new_hack(data_window, Hack(
                                            h_type,
                                            ticket_name.get(),
                                            ticket_desc.get(1.0, END).strip('\t\n'),
                                            ticket_value.get())))
        else:

            ticket_name.insert(INSERT, hack_data.title)
            ticket_value.insert(INSERT, str(hack_data.value))

            confirmButton = Button(button_frame, text="Save",
                command=lambda: 
                    self.save_edited_hack(data_window, hack_data.ID, Hack(
                                          h_type,
                                          ticket_name.get(),
                                          ticket_desc.get(1.0, END).strip('\t\n'),
                                          ticket_value.get())))

        confirmButton.pack(side="right")

    #Helper functions for input_hack_data
    def save_new_hack(self, window, hack_data):
        self.character.add_hack(hack_data)
        window.destroy()

    def save_edited_hack(self, window, hack_ID, hack_data):
        self.character.edit_hack(hack_ID, hack_data)
        window.destroy()

def main():
    #For Testing purposes
    root = Tk()
    test = Work_Space(root)
    root.mainloop()
    #End Test

    #pass

if __name__ == '__main__':
    main()  
        
