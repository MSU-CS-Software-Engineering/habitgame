import os.path
from tkinter  import *
from tkinter.ttk import *

from hack_classes import Hack
from shop import MyShop
from inventory import MyInventory
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.
from engine import GUI

class hack_frame(Frame):
    def __init__(self, parent, canvas_frame, hack):
        Frame.__init__(self, canvas_frame)
        self.canvas_frame = canvas_frame
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
        self.name_label.grid(row = 0, column = 0, sticky = 'news')
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

        self.columnconfigure(0, weight = 1)
        self.name_label.columnconfigure(0, weight = 1)
        self.description_label.columnconfigure(0, weight = 1)
        self.value_label.columnconfigure(0, weight = 1)
        self.btn_frame.columnconfigure(0, weight = 1)

        

    
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
        if self.top_class.delete_hack(self.ID):
            self.destroy()
            
    def edit(self):
        self.top_class.edit_hack(self.ID)
            
    def complete(self):
        if(self.top_class.complete_hack(self.ID)):
            if self.hack_type != "habit":
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
        Canvas.grid(self, sticky='news')
        
        self.configure(highlightthickness = 0,
                       background = '#EBEDF1')
        
        self.parent = parent
        self.frame = Frame(self, style = "W.TFrame",
                           borderwidth = 0, padding='10 10 0 0')
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
        self.scrollbar.grid(row = 1, column = 1, rowspan=2, sticky = 'ns')
        
        self.bind("<Enter>", lambda e: self.set_scrolling())
        self.frame.bind("<Configure>", self.setup_habit_frame)

    def set_scrolling(self):
        self.bind_all("<MouseWheel>", lambda e: self.scroll_habit(e))
        
    def remove_frames(self):
        for frame in self.frames:
            frame.destroy()

        self.frames = []

    def redraw(self, hack_dict):
        self.remove_frames()
        self.set_frames(hack_dict)
            
    def set_frames(self, hack_dict):
        for hack in hack_dict.values():
           individual_hack = hack_frame(self, self.frame, hack) 
           individual_hack.grid(row = hack.ID, column = 0,
                                sticky = 'ew', pady = (0,10))
           self.frames.append(individual_hack)
        
    def setup_habit_frame(self, event):
        # resets the scroll region for the frame inserted into the canvas
        self.configure(scrollregion = self.bbox("all"))
        
        
    def scroll_habit(self, event):
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
                'shop' : self.tab_shop,
                'inventory' : self.tab_inventory
               }
        try:
            if tabs[tab] == tabs['habit']:
                self.parent.go_to_habits(True)
            elif tabs[tab] == tabs['task']:
                self.parent.go_to_tasks(True)
            elif tabs[tab] == tabs['daily']:
                self.parent.go_to_dailies(True)
            
            for frame_tab in self.main_frame.tabs():
                self.main_frame.tab(frame_tab, state='hidden')

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
        self.tab_inventory = Work_Space_Tab(frame, width=850, height=400)
        
        #self.tab_habits.grid(row = 0, column = 1,sticky = 'news')
        self.tab_habits.pack(fill = BOTH, expand = YES)
        self.tab_tasks.pack(fill = BOTH, expand = YES)
        self.tab_shop.pack(fill = BOTH, expand = YES)
        self.tab_inventory.pack(fill = BOTH, expand = YES)

        # load images for complete, edit, delete buttons
        self.delete_img = PhotoImage(file=os.path.join("assets", "art", "minus.gif"))
        self.edit_img = PhotoImage(file=os.path.join("assets", "art", "pencil.gif"))
        self.complete_img = PhotoImage(file=os.path.join("assets", "art", "check.gif"))

        plus_img = PhotoImage(file=os.path.join("assets", "art", "plus.gif"))
        
        add_habit_btn = Button(self.tab_habits, text = 'Add new habit', image=plus_img, compound="left",
                               style = 'add_habit.TButton', cursor = 'hand2',
                               command = lambda: self.add_hack('habit'))
        add_habit_btn.grid(row = 0, column = 0, columnspan = 2, sticky = 'news')
        add_habit_btn.image = plus_img

        self.habit_canvas = Work_Space_Area(self.tab_habits) 
        self.daily_canvas = Work_Space_Area(self.tab_dailies)
        self.task_canvas = Work_Space_Area(self.tab_tasks)

        self.habit_canvas.grid(row = 1, column = 0, sticky = 'news')
        self.daily_canvas.grid(row = 1, column = 0, sticky = 'news')
        self.task_canvas.grid(row = 1, column = 0, sticky = 'news')

        self.habit_canvas.set_frames(self.habits_dict)
        self.daily_canvas.set_frames(self.dailies_dict)
        self.task_canvas.set_frames(self.tasks_dict)
        
        
        frame.add(self.tab_habits, state='hidden')
        frame.add(self.tab_tasks, state='hidden')
        frame.add(self.tab_dailies, state='hidden')
        frame.add(self.tab_shop, state='hidden')
        frame.add(self.tab_inventory, state='hidden')


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
        
        MyInventory.setInventory(self.tab_inventory)
        MyShop.setShop(self.tab_shop)
        self.main_frame.select(self.tab_shop)


        frame.rowconfigure(0, weight = 1)
        frame.columnconfigure(0, weight = 1)
        self.tab_habits.rowconfigure(1, weight = 1)
        self.tab_habits.columnconfigure(0, weight = 1)
        #self.habit_canvas.rowconfigure(1, weight = 1)
        self.habit_canvas.columnconfigure(0, weight = 1)
        
        self.tab_dailies.rowconfigure(1, weight = 1)
        self.tab_dailies.columnconfigure(0, weight = 1)
        #self.daily_canvas.rowconfigure(1, weight = 1)
        self.daily_canvas.columnconfigure(0, weight = 1)
        
        self.tab_tasks.rowconfigure(1, weight = 1)
        self.tab_tasks.columnconfigure(0, weight = 1)
        #self.task_canvas.rowconfigure(1, weight = 1)
        self.task_canvas.columnconfigure(0, weight = 1)
        
            

    def complete_hack(self, hack_ID):
        if self.parent.complete_hack(hack_ID):
            return True
        else:
            if self.parent.character.get_hack(hack_ID).h_type == "daily":
                self.parent.inst_notify("exclamation", "Dailies can only be completed once a day.")
            return False
        
    def add_hack(self, h_type):
        ''' Calls input window; Adds result to hack list '''
        self.input_hack_data(h_type)
        
    def delete_hack(self, hack_ID):
        answer = messagebox.askokcancel("Delete Hack", "Delete hack?")
        if answer:
            self.parent.delete_hack(hack_ID)
            return True
            
        else:
            return False

            
    def edit_hack(self, hack_ID):
        try:
            hack_data = self.character.get_hack(hack_ID)
            self.input_hack_data(hack_data.h_type, hack_data)
            
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

        name_warning_label = Label(name_frame, text = "Title cannot be empty!", padding = 5,
                                    foreground = "red", font='arial 12 bold', state = DISABLED)
        name_warning_label.pack(side="top", padx = 10, pady=10)
        name_warning_label.pack_forget() #Start invisible

        ticket_name = Entry(name_frame, justify=CENTER)
        ticket_name.pack(side="bottom", pady=5)

        #Description
        desc_frame = Frame(window_bg, style='popup_bg.TFrame')
        desc_frame.pack(side="top")

        desc_label = Label(desc_frame, text="Description", padding='128 5 128 5',
                           foreground='white', background='#283D57', font='arial 12 bold')
        desc_label.pack(side="top")

        desc_warning_label = Label(desc_frame, text = "Description cannot be empty!", padding = 5,
                                    foreground = "red", font='arial 12 bold', state = DISABLED)
        desc_warning_label.pack(side="top", padx = 10, pady=10)
        desc_warning_label.pack_forget() #Start invisible

        ticket_desc = Text(desc_frame, width=40, height=4)

        #if hack_data:
        #    ticket_desc.insert(INSERT, hack_data.description)

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
        
        if hack_data:
            ticket_name.insert(INSERT, hack_data.title)
            ticket_value.insert(INSERT, str(hack_data.value))
            ticket_desc.insert(INSERT, hack_data.description)

        confirmButton = Button(button_frame, text="Save", style = 'save.TButton', cursor = 'hand2',
            command=lambda: self.check_input_validity(data_window, h_type, name_warning_label, 
                                            desc_warning_label, value_warning_label, ticket_name.get(), 
                                            ticket_desc.get(1.0, END), ticket_value.get(), hack_data)) 
        confirmButton.pack(side="right")


        self.style.configure('save.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#96FF48')
        
    #Helper function for input_hack_data

    def check_input_validity(self, window, h_type, title_label, desc_label, value_label, 
                             title_string, desc_string, value_string, hack_data):

        error_triggered = False

        if title_string == "":
            title_label.pack()
            error_triggered = True
        
        else:
            title_label.pack_forget()

        if desc_string.strip('\t\n') == "": 
            desc_label.pack()
            error_triggered = True

        else:
            desc_label.pack_forget()

        try:
            int(value_string)
            value_label.pack_forget()

        except:
            value_label.pack()
            error_triggered = True

        if error_triggered:
            return

        else:

            submitted_hack = Hack(h_type, title_string,
                                  desc_string.strip('\t\n'), value_string)

            if not hack_data:
                self.parent.add_hack(submitted_hack)

            else:
                self.parent.edit_hack(hack_data.ID, submitted_hack)

        window.destroy()

        self.parent.inst_notify('put_type_here', "Your " + str(submitted_hack.get_hack_type()) +
                            " has been saved!")

def main():
    #For Testing purposes
    root = Tk()
    test = Work_Space(root)
    root.mainloop()
    #End Test

    #pass

if __name__ == '__main__':
    main()  
