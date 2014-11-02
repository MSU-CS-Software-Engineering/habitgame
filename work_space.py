import os.path
from tkinter  import *
from tkinter.ttk import *

from hack_classes import Hack
from shop import MyShop
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.


class Work_Space (Frame):

    def __init__(self, parent, character):
        Frame.__init__(self, parent)
        self.style = Style()
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
        frame_style.configure("W.TFrame", background='#EBEDF1',
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

        # load images for complete, edit, delete buttons
        delete_img = PhotoImage(file=os.path.join("assets", "art", "minus.gif"))
        edit_img = PhotoImage(file=os.path.join("assets", "art", "pencil.gif"))
        complete_img = PhotoImage(file=os.path.join("assets", "art", "check.gif"))
            
        #Begining of Habit Tab Code
        habit_canvas = Canvas(tab_habit, highlightthickness = 0, background = '#EBEDF1')
        habit_canvas.grid(row = 1, column = 0, sticky = 'news')

        habits_frame = Frame(habit_canvas, style = "W.TFrame", borderwidth = 0, padding = 10)
        habits_frame.grid(row = 0, column = 0, sticky = 'news')
        
        bar_habit = Scrollbar(tab_habit, orient = "vertical", command = habit_canvas.yview)
        habit_canvas.configure(yscrollcommand = bar_habit.set)

        tab_habit.grid_columnconfigure(0, weight = 1)
        #tab_habit.grid_rowconfigure(0, weight = 1)
        tab_habit.grid_rowconfigure(1, weight=1)
        
        habit_canvas.create_window((0,0), anchor = 'nw', window = habits_frame, tags = 'habits_frame')
        bar_habit.grid(row = 1, column = 1, sticky = 'ns')

        def setupHabitFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            habit_canvas.configure(scrollregion = habit_canvas.bbox("all"))

        habits_frame.bind("<Configure>", setupHabitFrame)
        
        def scroll_habit(event):
            """ allows for mouse wheel scrolling """
            try:
                habit_canvas.yview_scroll(-1 * int(event.delta/120), "units")
            except:
                pass

        habit_canvas.bind("<MouseWheel>", lambda e: scroll_habit(e))

        for h in [hack for hack in hack_dict if hack_dict[hack].h_type == 'habit']: #Gather habit-type hacks from dict
            individual_habit = Frame(habits_frame, style = 'habit.TFrame')
            individual_habit.grid(row = hack_dict[h].ID, column = 0, sticky = 'ew', pady = (10,0))
            
            frame_style.configure('habit.TFrame', background = '#C3C3C3')
            
            habit_name = Label(individual_habit, text = hack_dict[h].title)
            habit_name.grid(row = 0, column = 0, sticky = 'ew')
            habit_name.configure(foreground = 'white', background = '#323232',
                                 padding = 5, font = 'arial 14 bold', anchor = CENTER)

            habit_description = Label(individual_habit, text = hack_dict[h].description, wraplength = 800)
            habit_description.grid(row = 1, column = 0, sticky = 'ew')
            habit_description.configure(foreground = '#373737', background = '#D9D9D9',
                                        padding = '15 5 15 5', font = 'arial 12', width = 80)

            habit_stats_frame = Frame(individual_habit, style = 'habit_stats.TFrame')
            habit_stats_frame.grid(row = 2, column = 0, sticky = 'news')
            frame_style.configure('habit_stats.TFrame', background = '#D9D9D9')
            
            habit_value = Label(habit_stats_frame, text = "Value:  " + str(hack_dict[h].value))
            habit_value.grid(row = 0, column = 0, sticky = 'ew')
            habit_value.configure(padding = '15 5 15 5', background = '#D9D9D9',
                                  foreground = '#373737', font = 'arial 12 bold')

            habit_date = Label(habit_stats_frame, text = "Date:  " + str(hack_dict[h].timestamp))
            habit_date.grid(row = 0, column = 1, sticky = 'ew')
            habit_date.configure(padding = 5, background = '#D9D9D9',
                                 foreground = '#373737', font = 'arial 12 bold')

            habit_btn_frame = Frame(individual_habit)
            habit_btn_frame.grid(row = 3, column = 0)
            
            delete_habit_btn = Button(habit_btn_frame, text='Delete habit', image=delete_img, compound="left",
                                      style = 'delete.TButton', cursor = 'hand2',
                                      command = lambda h=h: self.delete_hack(h))
            delete_habit_btn.grid(row = 0, column = 0, sticky = 'news')
            delete_habit_btn.image = delete_img

            edit_habit_btn = Button(habit_btn_frame, text='Edit habit', image=edit_img, compound="left",
                                    style = 'edit.TButton', cursor = 'hand2',
                                    command = lambda h=h: self.edit_hack(h))
            edit_habit_btn.grid(row = 0, column = 1, sticky = 'news')
            edit_habit_btn.image = edit_img

            complete_habit_btn = Button(habit_btn_frame, text='Complete habit', image=complete_img,
                                        compound="left", style = 'complete.TButton', cursor = 'hand2',
                                        command = lambda h=h: self.edit_hack(h)) #FIX ME -D
            complete_habit_btn.grid(row = 0, column = 2, sticky = 'news')
            complete_habit_btn.image = complete_img
 
        #Begining of Dailies Tab Code
        daily = Canvas(tab_dailies, highlightthickness = 0, background = '#EBEDF1')
        daily.grid(row = 1, column = 0, sticky = 'news')

        dailies = Frame(daily, style = "W.TFrame", borderwidth = 0, padding = 10)
        dailies.grid(row = 0, column = 0, sticky = 'news')

        bar_dailies = Scrollbar(tab_dailies, orient = VERTICAL, command = daily.yview)
        daily.configure(yscrollcommand = bar_dailies.set)

        tab_dailies.rowconfigure(1, weight = 1)
        tab_dailies.columnconfigure(0, weight = 1)

        daily.create_window((0,0), anchor = N + E, window = dailies, tags = 'dailies')
        bar_dailies.grid(row = 1, column = 1, sticky = 'ns')

        def setupDailiesFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            daily.configure(scrollregion=daily.bbox("all"))

        daily.bind("<Configure>", setupDailiesFrame)

        def scroll_daily(event):
            """ allows for mouse wheel scrolling """
            try:
                daily.yview_scroll(-1 * int(event.delta/120), "units")
            except:
                pass

        daily.bind("<MouseWheel>", lambda e: scroll_daily(e))
        
        #Gather dailies from dict
        for d in [hack for hack in hack_dict if hack_dict[hack].h_type == 'daily']:  
            individual_dailies = Frame(dailies, style = 'dailies.TFrame')
            individual_dailies.grid(row = hack_dict[d].ID, column = 0, sticky = 'ew', pady = (10,0))
            
            frame_style.configure('dailies.TFrame', background = '#C3C3C3')
            
            dailies_title = Label(individual_dailies, text = hack_dict[d].title)
            dailies_title.grid(row = 0, column = 0, sticky = 'ew')
            dailies_title.configure(foreground = 'white', background = '#323232',
                                    padding = 5, font = 'arial 14 bold', anchor = CENTER)

            dailies_description = Label(individual_dailies, text = hack_dict[d].description, wraplength = 800)
            dailies_description.grid(row = 1, column = 0, sticky = 'ew')
            dailies_description.configure(foreground = 'black', background = '#D9D9D9',
                                          padding = '15 5 15 5', font = 'arial 12', width = 80)

            dailies_stats_frame = Frame(individual_dailies, style = 'dailies_stats.TFrame')
            dailies_stats_frame.grid(row = 2, column = 0, sticky = 'news')
            frame_style.configure('dailies_stats.TFrame', background = '#D9D9D9')
            
            dailies_value = Label(dailies_stats_frame, text = "Value:  " + str(hack_dict[d].value))
            dailies_value.grid(row = 0, column = 0, sticky = 'ew')
            dailies_value.configure(padding = '15 5 15 5', background = '#D9D9D9',
                                    foreground = '#373737', font = 'arial 12 bold')

            dailies_date = Label(dailies_stats_frame, text = "Date:  " + str(hack_dict[d].timestamp))
            dailies_date.grid(row = 0, column = 1, sticky = 'ew')
            dailies_date.configure(padding = 5, background = '#D9D9D9',
                                   foreground = '#373737', font = 'arial 12 bold')

            dailies_btn_frame = Frame(individual_dailies)
            dailies_btn_frame.grid(row = 3, column = 0)

            delete_dailies_btn = Button(dailies_btn_frame, text = 'Delete Daily', image=delete_img, compound="left",
                                        style = 'delete.TButton', cursor = 'hand2',
                                        command = lambda d=d: self.delete_hack(d))
            delete_dailies_btn.grid(row = 0, column = 0, sticky = 'news')
            delete_dailies_btn.image = delete_img
            
            edit_dailies_btn = Button(dailies_btn_frame, text = 'Edit Daily', image=edit_img, compound="left",
                                      style = 'edit.TButton', cursor = 'hand2',
                                      command = lambda d=d: self.edit_hack(d))
            edit_dailies_btn.grid(row = 0, column = 1, sticky = 'news')
            edit_dailies_btn.image = edit_img
            
            complete_dailies_btn = Button(dailies_btn_frame, text = 'Complete Daily', image=complete_img,
                                          compound="left", style = 'complete.TButton', cursor = 'hand2',
                                          command = lambda d=d: self.edit_hack(d)) #FIX ME -D
            complete_dailies_btn.grid(row = 0, column = 2, sticky = 'news')
            complete_dailies_btn.image = complete_img

        #Begining of Tasks Tab Code
        task = Canvas(tab_tasks, highlightthickness = 0, background = '#EBEDF1')
        task.grid(row = 1, column = 0, sticky = 'news')

        tasks= Frame(task, style = "W.TFrame", padding = 10)
        tasks.grid(row = 0, column = 0, sticky = 'news')

        bar_tasks = Scrollbar(tab_tasks, orient = VERTICAL, command = task.yview)
        task.configure(yscrollcommand = bar_tasks.set)

        tab_tasks.rowconfigure(1, weight = 1)
        tab_tasks.columnconfigure(0, weight = 1)

        task.create_window((0,0), anchor = N + E, window = tasks)
        bar_tasks.grid(row = 1, column = 1, sticky = 'ns')

        def setupTasksFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            task.configure(scrollregion=task.bbox("all"))

        task.bind("<Configure>", setupTasksFrame)

        def scroll_task(event):
            """ allows for mouse wheel scrolling """
            try:
                task.yview_scroll(-1 * int(event.delta/120), "units")
            except:
                pass

        task.bind("<MouseWheel>", lambda e: scroll_task(e))
        
        #Gather tasks from dict
        for t in [hack for hack in hack_dict if hack_dict[hack].h_type == 'task']: 
            individual_tasks = Frame(tasks, style = 'tasks.TFrame')
            individual_tasks.grid(row = hack_dict[t].ID, column = 0, sticky = 'ew', pady = (10,0))

            frame_style.configure('tasks.TFrame', background = '#C3C3C3')
            
            tasks_title = Label(individual_tasks, text = hack_dict[t].title)
            tasks_title.grid(row = 0, column = 0, sticky = 'ew')
            tasks_title.configure(foreground = 'white', background = '#323232',
                                  padding = 5, font = 'arial 14 bold', anchor = CENTER)

            tasks_description = Label(individual_tasks, text = hack_dict[t].description, wraplength = 800)
            tasks_description.grid(row = 1, column = 0, sticky = 'ew')
            tasks_description.configure(foreground = 'black', background = '#D9D9D9',
                                        padding = '15 5 15 5', font = 'arial 12', width = 80)

            tasks_stats_frame = Frame(individual_tasks, style = 'tasks_stats.TFrame')
            tasks_stats_frame.grid(row = 2, column = 0, sticky = 'news')
            frame_style.configure('tasks_stats.TFrame', background = '#D9D9D9')
            
            tasks_value = Label(tasks_stats_frame, text = "Value:  " + str(hack_dict[t].value))
            tasks_value.grid(row = 0, column = 0, sticky = 'ew')
            tasks_value.configure(padding = '15 5 15 5', background = '#D9D9D9',
                                  foreground = '#373737', font = 'arial 12 bold')

            tasks_date = Label(tasks_stats_frame, text = "Date:  " + str(hack_dict[t].timestamp))
            tasks_date.grid(row = 0, column = 1, sticky = 'ew')
            tasks_date.configure(padding = 5, background = '#D9D9D9',
                                 foreground = '#373737', font = 'arial 12 bold')

            tasks_btn_frame = Frame(individual_tasks)
            tasks_btn_frame.grid(row = 3, column = 0)
            
            delete_tasks_btn = Button(tasks_btn_frame, text = 'Delete Task', image=delete_img, compound="left",
                                      style = 'delete.TButton', cursor = 'hand2',
                                      command = lambda t=t: self.delete_hack(t))
            delete_tasks_btn.grid(row = 0, column = 0, sticky = 'news')
            delete_tasks_btn.image = delete_img
            
            edit_tasks_btn = Button(tasks_btn_frame, text = 'Edit Task', image=edit_img, compound="left",
                                    style = 'edit.TButton', cursor = 'hand2',
                                    command = lambda t=t: self.edit_hack(t))
            edit_tasks_btn.grid(row = 0, column = 1, sticky = 'news')
            edit_tasks_btn.image = edit_img
            
            complete_tasks_btn = Button(tasks_btn_frame, text = 'Complete Task', image=complete_img,
                                        compound="left", style = 'complete.TButton', cursor = 'hand2',
                                        command =lambda t=t: self.edit_hack(t)) #FIX ME -D
            complete_tasks_btn.grid(row = 0, column = 2, sticky = 'news')
            complete_tasks_btn.image = complete_img
            
        frame.add(tab_habit, text='Habits')
        frame.add(tab_tasks, text='Tasks')
        frame.add(tab_dailies, text='Dailies')
        frame.add(tab_shop, text='Shop')

        plus_img = PhotoImage(file=os.path.join("assets", "art", "plus.gif"))
        
        add_habit_btn = Button(tab_habit, text = 'Add new habit', image=plus_img, compound="left",
                               style = 'add_habit.TButton', cursor = 'hand2',
                               command = lambda: self.add_hack('habit'))
        add_habit_btn.grid(row = 0, column = 0, columnspan = 2, sticky = 'news')
        add_habit_btn.image = plus_img
        
        add_task_btn = Button(tab_tasks, text = 'Add new task', image=plus_img, compound="left",
                              style = 'add_task.TButton', cursor = 'hand2',
                              command = lambda: self.add_hack('task'))
        add_task_btn.grid(row = 0, column = 0, columnspan = 2, sticky = 'news')
        add_task_btn.image = plus_img
        
        add_daily_btn = Button(tab_dailies, text = 'Add new daily', image=plus_img, compound="left",
                               style = 'add_daily.TButton', cursor = 'hand2',
                               command = lambda: self.add_hack('daily'))
        add_daily_btn.grid(row = 0, column = 0, columnspan = 2, sticky = 'news')
        add_daily_btn.image = plus_img
        
        # style delete, edit, and complete buttons for habits, dailies, and tasks tabs
        frame_style.configure('delete.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#FF3C3C')
        frame_style.configure('edit.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#59AEE1')
        frame_style.configure('complete.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#87DC5F')
        
        frame_style.configure('add_habit.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#7A9BC2')
        frame_style.configure('add_task.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#7A9BC2')
        frame_style.configure('add_daily.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#7A9BC2')

        
        #habit.create_window(-675, 0, window  =  add_habit_btn)
        #daily.create_window(-675, 0, window  =  add_daily_btn)
        #task.create_window(-675,  0, window  =  add_task_btn)

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
        #REBUILD_HACK_LIST_ON_GUI
        
    def delete_hack(self, hack_ID):
        answer = messagebox.askokcancel("Delete Hack", "Delete hack?")
        if answer is True:
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


    def input_hack_data(self, h_type, hack_data = None):
        data_window = Toplevel(self)

        #Name of habit\daily\task
        window_bg = Frame(data_window, style='popup_bg.TFrame')
        window_bg.pack()
        
        name_frame = Frame(window_bg, style='popup_bg.TFrame')
        name_frame.pack(side="top")

        self.style.configure('popup_bg.TFrame', background='#D9D9D9')
        
        name_label = Label(name_frame, text="Name", padding='150 5 150 5',
                           foreground='white', background='#283D57', font='arial 12 bold')
        name_label.pack(side="top")

        ticket_name = Entry(name_frame, justify=CENTER)
        ticket_name.pack(side="bottom", pady=5)

        #Description
        desc_frame = Frame(window_bg, style='popup_bg.TFrame')
        desc_frame.pack(side="top")

        desc_label = Label(desc_frame, text="Description", padding='128 5 128 5',
                           foreground='white', background='#283D57', font='arial 12 bold')
        desc_label.pack(side="top")

        ticket_desc = Text(desc_frame, width=40, height=4)

        if hack_data != None:
            ticket_desc.insert(INSERT, hack_data.description)

        ticket_desc.pack(side="bottom", pady=5)

        #Value
        value_frame = Frame(window_bg, style='popup_bg.TFrame')
        value_frame.pack(side="top")

        value_label = Label(value_frame, text="Reward Value", padding='119 5 119 5',
                            foreground='white', background='#283D57', font='arial 12 bold')
        value_label.pack(side="top")

        value_warning_label = Label(value_frame, text = "Value must be a number!", padding = 5,
                                    foreground = "red", font='arial 12 bold', state = DISABLED)
        value_warning_label.pack(side="top", padx = 10, pady=10)
        value_warning_label.pack_forget() #Start invisible

        ticket_value = Entry(value_frame, justify=CENTER)
        ticket_value.pack(side="bottom", pady=5)

        #Buttons
        button_frame = Frame(window_bg, width=100)
        button_frame.grid_propagate(100)
        button_frame.pack(side="bottom", padx=10, pady=10)

        cancelButton = Button(button_frame, text="Cancel", style = 'cancel.TButton',
                              cursor = 'hand2', command=data_window.destroy)
        cancelButton.pack(side="left")
        self.style.configure('cancel.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#FF4848')
        
        if hack_data == None:
            confirmButton = Button(button_frame, text="Save", style = 'save.TButton', cursor = 'hand2',
                command=lambda: 
                    self.save_new_hack(data_window, Hack(
                                            h_type,
                                            ticket_name.get(),
                                            ticket_desc.get(1.0, END).strip('\t\n'),
                                            ticket_value.get())))
        else:
            ticket_name.insert(INSERT, hack_data.title)
            ticket_value.insert(INSERT, str(hack_data.value))

            confirmButton = Button(button_frame, text="Save", style = 'save.TButton', cursor = 'hand2',
                command=lambda: 
                    self.save_edited_hack(data_window, hack_data.ID, Hack(
                                          h_type,
                                          ticket_name.get(),
                                          ticket_desc.get(1.0, END).strip('\t\n'),
                                          ticket_value.get())))

        confirmButton.pack(side="right")
        ticket_value.bind('<FocusOut>', lambda event: self.check_input_validity(
                                                value_warning_label, ticket_value.get(), confirmButton)) 
        self.style.configure('save.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#96FF48')
        
    #Helper functions for input_hack_data
    def save_new_hack(self, window, hack_data):
        self.character.add_hack(hack_data)
        window.destroy()

    def save_edited_hack(self, window, hack_ID, hack_data):
        self.character.edit_hack(hack_ID, hack_data)
        window.destroy()

    def check_input_validity(self, warn_label, value_string, confirmButton):
        try:
            int(value_string)
            warn_label.pack_forget()
            confirmButton.config(state = 'normal')
        except:
            warn_label.pack()
            confirmButton.config(state = 'disabled')

def main():
    #For Testing purposes
    root = Tk()
    test = Work_Space(root)
    root.mainloop()
    #End Test

    #pass

if __name__ == '__main__':
    main()  
        
