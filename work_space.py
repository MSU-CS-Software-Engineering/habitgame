import os.path
from tkinter  import *
from tkinter.ttk import *

from hack_classes import Hack
from shop import MyShop
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.


class hack_frame(Frame):

    def __init__(self, parent, hack):
        Frame.__init__(self, parent)
        self.parent = parent
        self.ID = hack.ID
        self.hack_type = hack.h_type
        self.top_class = self.parent.parent.parent.parent
        self.delete_img = self.top_class.delete_img
        self.edit_img = self.top_class.edit_img
        self.complete_img = self.top_class.complete_img
        self.configure(style = 'hack.TFrame')
        
        frame_style = Style()
        frame_style.configure('hack.TFrame', background = '#C3C3C3')
        # style delete, edit, and complete buttons for habits,
        #dailies, and tasks tabs
        frame_style.configure('delete.TButton',
                              font = 'arial 14 bold',
                              relief = 'flat',
                              padding = 5,
                              foreground = 'black',
                              background = '#FF3C3C')
        
        frame_style.configure('edit.TButton',
                              font = 'arial 14 bold',
                              relief = 'flat',
                              padding = 5,
                              foreground = 'black',
                              background = '#59AEE1')
        
        frame_style.configure('complete_task.TButton',
                              font = 'arial 14 bold',
                              relief = 'flat',
                              padding = 5,
                              foreground = 'black',
                              background = '#87DC5F')
                              
        self.name_label = Label(self, text = hack.title)
        self.name_label.grid(row = 0, column = 0, sticky = 'ew')
        self.name_label.configure(foreground = 'white', background = '#323232',
                                  padding = 5, font = 'arial 14 bold', anchor = CENTER)
        
        self.description_label = Label(self, text = hack.description, wraplength = 800)
        self.description_label.grid(row = 1, column = 0, sticky = 'ew')
        self.description_label.configure(foreground = '#373737', background = '#D9D9D9',
                                        padding = '15 5 15 5', font = 'arial 12', width = 80)

        self.stats_frame = Frame(self, style = 'stats.TFrame')
        self.stats_frame.grid(row = 2, column = 0, sticky = 'news')

        frame_style.configure('stats.TFrame', background = '#D9D9D9')
            
        self.value_label = Label(self.stats_frame, text = "Value:  " + str(hack.value))
        self.value_label.grid(row = 0, column = 0, sticky = 'ew')
        self.value_label.configure(padding = '15 5 15 5', background = '#D9D9D9',
                                  foreground = '#373737', font = 'arial 12 bold')

        self.date_label = Label(self.stats_frame, text = "Date:  " + str(hack.timestamp))
        self.date_label.grid(row = 0, column = 1, sticky = 'ew')
        self.date_label.configure(padding = 5, background = '#D9D9D9',
                                 foreground = '#373737', font = 'arial 12 bold')

        self.btn_frame = Frame(self)
        self.btn_frame.grid(row = 3, column = 0)
            
        self.delete_btn = Button(self.btn_frame, text='Delete '+self.hack_type, image=self.delete_img, compound="left",
                                      style = 'delete.TButton', cursor = 'hand2',
                                      command = self.delete)
        self.delete_btn.grid(row = 0, column = 0, sticky = 'news')
        self.delete_btn.image = self.delete_img

        self.edit_btn = Button(self.btn_frame, text='Edit '+self.hack_type, image=self.edit_img, compound="left",
                                    style = 'edit.TButton', cursor = 'hand2',
                                    command = self.edit)
        self.edit_btn.grid(row = 0, column = 1, sticky = 'news')
        self.edit_btn.image = self.edit_img

        self.complete_btn = Button(self.btn_frame, text='Complete '+self.hack_type,
                                   image= self.complete_img, compound="left",
                                   style = 'complete_task.TButton', cursor = 'hand2',
                                   command = self.complete)
        
        self.complete_btn.grid(row = 0, column = 2, sticky = 'news')
        self.complete_btn.image = self.complete_img

    '''
    def set_name_label_text(self, text=self.hack.title):
        self.name_label.configure(text = text)
            
    def set_description_label_text(self, text=self.hack.description):
        self.description_label.configure(text = text)
            
    def set_date_label_text(self, text=str(self.hack.timestamp)):
        self.date_label.configure(text = text)
            
    def set_value_label_text(self, text=str(self.hack.value)):
        self.value_label.configure(text = text)

    '''
    
    def redraw(self, hack):
        '''
        Redraws the frame to display the current character data
        '''
        self.hack = hack
        self.set_name_label_text()
        self.set_description_label_text()
        self.set_data_label_text()
        self.set_value_label_text()

    def delete(self):
        self.top_class.delete_hack(self.ID)
        self.destroy()
            
    def edit(self):
        self.top_class.edit_hack(self.ID)
            
    def complete(self):
        self.top_class.complete_hack(self.ID)
        self.destroy()

class Work_Space_Tab(Canvas):
    def __init__(self, parent, width, height):
        Canvas.__init__(self, parent)
        self.parent = parent
        self.configure(width = width, height = height)
        
    def set_width(self, width):
        self.configure(width = width)

    def set_height(self, height):
        self.configure(height = height)

        
class Work_Space_Area(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent)
        self.configure(highlightthickness = 0,
                       background = '#EBEDF1')
        
        self.parent = parent
        self.frame = Frame(self, style = "W.TFrame",
                           borderwidth = 0, padding = 10)
        self.frame.grid(row = 0, column = 0, sticky = 'news')
        self.frames = []
        
        canvas_style = Style()

        canvas_style.configure("W.TFrame", background='#EBEDF1',
                              pady = (10,0), padx =3)
        
        
        self.scrollbar = Scrollbar(self.parent,
                                   orient = "vertical",
                                   command = self.yview)
        
        self.configure(yscrollcommand = self.scrollbar.set)

        self.create_window((0,0), anchor = 'nw', window = self.frame)
        self.scrollbar.grid(row = 1, column = 1, sticky = 'ns')

        self.frame.bind("<Configure>", self.setup_habit_frame)
        self.bind("<MouseWheel>", lambda e: self.scroll_habit(e))

    def remove_frames(self):
        for frame in self.frames:
            frame.destroy()

        self.frames = []


    def redraw(self, hack_dict):
        self.remove_frames()
        self.set_frames(hack_dict)
            
    def set_frames(self, hack_dict):
        for hack in hack_dict.values():
           individual_hack = hack_frame(self, hack) 
           individual_hack.grid(row = hack.ID, column = 0,
                                sticky = 'ew', pady = (10,0))
           self.frames.append(individual_hack)
        
    def setup_habit_frame(event):
        # resets the scroll region for the frame inserted into the canvas
        self.configure(scrollregion = self.bbox("all"))
        
        
    def scroll_habit(event):
        """ allows for mouse wheel scrolling """
        try:
            self.yview_scroll(-1 * int(event.delta/120), "units")
        except:
            pass

class Work_Space_Notebook(Notebook):
    def __init__(self, parent, height, width, padding):
        Notebook.__init__(self, parent)
        self.parent = parent
        self.configure(width = width, height = height,
                       padding = padding)
        
class Work_Space(Frame):

    def __init__(self, parent, character):
        Frame.__init__(self, parent)
        self.style = Style()
        self.parent = parent
        self.character = character
        self.set_dicts()
        self.rowconfigure(4, weight =1)
        self.columnconfigure(0, weight = 1)
        self.set_work_window()

    def set_dicts(self):
        self.habits_dict = {k:self.character.hacks[k]
                           for k in self.character.hacks
                           if self.character.hacks[k].h_type == 'habit'}
        self.dailies_dict = {k:self.character.hacks[k]
                             for k in self.character.hacks
                             if self.character.hacks[k].h_type == 'daily'}
        self.tasks_dict = {k:self.character.hacks[k]
                           for k in self.character.hacks
                           if self.character.hacks[k].h_type == 'task'}

        
    def select_tab(self, tab):
        '''
        Used for selecting tab from an element
        outside of Work_Space
        '''
        tabs = {
                'task' : self.tab_tasks,
                'daily': self.tab_dailies,
                'habit': self.tab_habits,
                'shop' : self.tab_shop
               }
        try:
            self.main_frame.select(tabs[tab])
            
        except:
            messagebox.showerror("Error", "Couldn't change tabs")

            
    def redraw(self, character):
        #Update class' character data instance
        self.character = character
        self.set_dicts()
        
        #Call class canvases redraw function
        self.habit_canvas.redraw(self.habits_dict)
        self.daily_canvas.redraw(self.dailies_dict)
        self.task_canvas.redraw(self.tasks_dict)
        
            
    def set_work_window(self):

        #creating the workspace 
        frame = Work_Space_Notebook(self, height = 200, width = 400, padding=5)
        frame.grid(row=4, column = 0, columnspan = 7, rowspan = 4,
                   sticky = 'nesw')
        frame_style = Style()
        frame_style.configure("W.TFrame", background='#EBEDF1',
                              pady = (10,0), padx =3)
        frame.rowconfigure(4, weight = 1)
        frame.columnconfigure(0, weight = 1)
        #frame.grid_propagate(False)

        self.tab_habits = Work_Space_Tab(frame, width=850, height=400)
        self.tab_dailies = Work_Space_Tab(frame, width=850, height=400)
        self.tab_tasks = Work_Space_Tab(frame, width=850, height=400)
        self.tab_shop = Work_Space_Tab(frame, width=850, height=400)

        self.tab_habits.pack(fill = BOTH, expand = YES)
        self.tab_dailies.pack(fill = BOTH, expand = YES)
        self.tab_tasks.pack(fill = BOTH, expand = YES)
        self.tab_shop.pack(fill = BOTH, expand = YES)

        # load images for complete, edit, delete buttons
        self.delete_img = PhotoImage(file=os.path.join("assets", "art", "minus.gif"))
        self.edit_img = PhotoImage(file=os.path.join("assets", "art", "pencil.gif"))
        self.complete_img = PhotoImage(file=os.path.join("assets", "art", "check.gif"))

        '''
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
        '''

        self.habit_canvas = Work_Space_Area(self.tab_habits) 
        self.daily_canvas = Work_Space_Area(self.tab_dailies)
        self.task_canvas = Work_Space_Area(self.tab_tasks)

        self.habit_canvas.grid(row = 1, column = 0, sticky = 'news')
        self.daily_canvas.grid(row = 1, column = 0, sticky = 'news')
        self.task_canvas.grid(row = 1, column = 0, sticky = 'news')

        self.habit_canvas.set_frames(self.habits_dict)
        self.daily_canvas.set_frames(self.dailies_dict)
        self.task_canvas.set_frames(self.tasks_dict)
        
        '''
        for h in [hack for hack in hack_dict if hack_dict[hack].h_type == 'habit']: #Gather habit-type hacks from dict
            individual_habit = hack_frame(habits_frame, style = 'habit.TFrame')
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
                                        compound="left", style = 'complete_task.TButton', cursor = 'hand2',
                                        command = lambda h=h: self.complete_hack(h))
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
                                          compound="left", style = 'complete_task.TButton', cursor = 'hand2',
                                          command = lambda d=d: self.complete_hack(d))
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
                                        compound="left", style = 'complete_task.TButton', cursor = 'hand2',
                                        command =lambda t=t: self.complete_hack(t))
            complete_tasks_btn.grid(row = 0, column = 2, sticky = 'news')
            complete_tasks_btn.image = complete_img
        '''
        
        frame.add(self.tab_habits, text='Habits')
        frame.add(self.tab_tasks, text='Tasks')
        frame.add(self.tab_dailies, text='Dailies')
        frame.add(self.tab_shop, text='Shop')

        plus_img = PhotoImage(file=os.path.join("assets", "art", "plus.gif"))
        
        add_habit_btn = Button(self.tab_habits, text = 'Add new habit', image=plus_img, compound="left",
                               style = 'add_habit.TButton', cursor = 'hand2',
                               command = lambda: self.add_hack('habit'))
        add_habit_btn.grid(row = 0, column = 0, columnspan = 2, sticky = 'news')
        add_habit_btn.image = plus_img
        
        add_task_btn = Button(self.tab_tasks, text = 'Add new task', image=plus_img, compound="left",
                              style = 'add_task.TButton', cursor = 'hand2',
                              command = lambda: self.add_hack('task'))
        add_task_btn.grid(row = 0, column = 0, columnspan = 2, sticky = 'news')
        add_task_btn.image = plus_img
        
        add_daily_btn = Button(self.tab_dailies, text = 'Add new daily', image=plus_img, compound="left",
                               style = 'add_daily.TButton', cursor = 'hand2',
                               command = lambda: self.add_hack('daily'))
        add_daily_btn.grid(row = 0, column = 0, columnspan = 2, sticky = 'news')
        add_daily_btn.image = plus_img
        
        # style delete, edit, and complete buttons for habits, dailies, and tasks tabs
        frame_style.configure('delete.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#FF3C3C')
        frame_style.configure('edit.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#59AEE1')
        frame_style.configure('complete_task.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#87DC5F')
        
        frame_style.configure('add_habit.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#7A9BC2')
        frame_style.configure('add_task.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#7A9BC2')
        frame_style.configure('add_daily.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#7A9BC2')

        self.main_frame = frame
        
        MyShop.setShop(self.tab_shop)
        self.main_frame.select(self.tab_shop)
        
    def complete_hack(self, hack_ID):
        self.parent.complete_hack(hack_ID)
        
        
    def add_hack(self, h_type):
        ''' Calls input window; Adds result to hack list '''
        self.input_hack_data(h_type)
        #REBUILD_HACK_LIST_ON_GUI
        
    def delete_hack(self, hack_ID):
        answer = messagebox.askokcancel("Delete Hack", "Delete hack?")
        if answer is True:
            self.parent.delete_hack(hack_ID)
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
        self.parent.add_hack(hack_data)
        window.destroy()
        messagebox.showinfo('Hack Saved', 'Your ' + str(hack_data.get_hack_type()) +
                            ' hack has been saved!')

    def save_edited_hack(self, window, hack_ID, hack_data):
        self.parent.edit_hack(hack_ID, hack_data)
        window.destroy()
        messagebox.showinfo('Hack Saved', 'Your ' + str(hack_data.get_hack_type()) +
                            ' hack has been saved!')

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
        
