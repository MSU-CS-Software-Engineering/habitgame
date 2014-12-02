import os.path
from tkinter  import *
from tkinter.ttk import *

from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.


class Hack_Frame(Frame):
    def __init__(self, parent, ID, hack_type, empty=0):
        Frame.__init__(self, parent)
        self.parent = parent
        self.ID = ID
        self.hack_type = hack_type
        self.top_class = self.parent.parent.parent
        
        self.name_label = Label(self,
                                text = '',
                                anchor = CENTER,
                                background = "#F9D386",
                                font = "Veranda 16 bold")
        self.name_label.pack(fill = X, expand = True)

        self.description_label = Label(self,
                                       text = '',
                                       wraplength = 375,
                                       background = "#EFE4B0",
                                       font = "arial 12",
                                       padding = 5, justify = LEFT)
        self.description_label.pack(fill = X, expand = True)

        self.value_label = Label(self,
                                 text = '',
                                 font = "arial 12",
                                 padding = 5,
                                 background = "#EFE4B0")
        self.value_label.pack(fill = X, expand = True)
        
        self.date_time_label = Label(self,
                                     text = '',
                                     font = "arial 12",
                                     padding = 5,
                                     background = "#EFE4B0")
        self.date_time_label.pack(fill = X, expand = True)
 
        if empty == 0:
            self.complete_button = Button(self)
            self.complete_button.configure(text = 'Complete',
                                           style = 'complete.TButton',
                                           image = self.parent.parent.complete_button_image,
                                           compound = 'left',
                                           cursor = 'hand2',
                                           command = self.remove)

            complete_button_style = Style()
            complete_button_style.configure('complete.TButton',
                                            font = 'arial 12 bold',
                                            relief = 'flat',
                                            padding = '0 3 0 3',
                                            foreground = 'black',
                                            background = '#C6E29A')
            
            self.complete_button.image = self.parent.parent.complete_button_image

            self.complete_button.pack(fill = X,
                                      expand = True,
                                      side = BOTTOM)
            
        self.set_style('frame_style.TFrame', '#EBEDF1', 100)

    def remove(self):
        #Pass the data to the top-level(parent->parent->parent)
        self.top_class.complete_hack(self.ID)
        self.destroy()

    def function_builder(self, args):
        messagebox.showinfo("Place Holder", "go to " + args)

    def set_complete_button_text(self, text):
        self.complete_button.configure(text = text)
        
    def set_style(self, name, background_color, height=None):
        _style = Style()
        
        if height != None:
            _style.configure(name, background = background_color,
                             height = height)
        else:
            _style.configure(name, background = background_color)

        self.configure(style = name)

    def set_description_label(self, text):
        self.description_label.configure(text = "Note: " + text)

    def set_name_label(self, text):
        self.name_label.configure(text = text)

    def set_value_label(self, text):
        self.value_label.configure(text = "Value: " + text)

    def set_date_time_label(self, text):
        self.date_time_label.configure(text = "Date/Time: " + text)

    
        
class Landing_Area_Frame(Frame):
    def __init__(self, parent, hack_type):
        Frame.__init__(self, parent)
        self.set_style()
        self.frames = []
        self.number_of_frames = 0
        self.empty_frames_message = ''
        self.hack_type = hack_type
        self.column = self.get_column()
        self.parent = parent
        self.current_row = 0
        
    def remove_frames(self):
        for frame in self.frames:
            frame.destroy()

        self.current_row = 1
        self.frames = []
        
    def set_style(self, height=None):
        _style = Style()
        _style.configure('frame_style.TFrame',
                         background = '#EBEDF1')
        if height != None:
            _style.configure(height = height)
        
        self.configure(style = 'frame_style.TFrame')

    def set_header(self, text, color):
        self.header = Label(self, text = text,
                            anchor = CENTER,
                            font = "Veranda 18 bold",
                            foreground = 'black',
                            background = color)

        self.header.grid(row = 0, column = self.column, sticky = 'new',
                         pady = (3,0), padx = 3)

    def get_current_row(self):
        self.current_row += 1
        return self.current_row
    
    def get_column(self):
        if self.hack_type == 'habit':
            return 0
            
        elif self.hack_type == 'daily':
            return 2

        else:
            return 4

    def set_frames(self, hack_dict):
        
        #Hack Code Area
        if len(hack_dict) > 4:
            self.number_of_frames = 5
            
        elif len(hack_dict) == 0:
            self.number_of_frames = 0
            
            hack_frame = Hack_Frame(self, 0, self.hack_type, 1)
            hack_frame.grid(row = 1, column = self.column, sticky = 'news',pady = (3,0), padx = 3)

            if self.hack_type == 'daily':
                label_string = 'dailies'
            elif self.hack_type == 'habit':
                label_string = 'habits'
            else:
                label_string = 'tasks'
                
            hack_frame.set_name_label("No "+label_string+" to Display")
            self.frames.append(hack_frame)
            
        else:
            self.number_of_frames = len(hack_dict)

            
        if self.number_of_frames != 0:
            for key in hack_dict.keys():
                hack = hack_dict[key]
                hack_frame = Hack_Frame(self, hack.ID, self.hack_type)
                hack_frame.grid(row = self.get_current_row(),
                                column = self.column,
                                sticky = 'new', pady = (3,0),
                                padx = 3)
                hack_frame.set_name_label(hack.title)
                hack_frame.set_description_label(hack.description)
                hack_frame.set_value_label(str(hack.value))
                hack_frame.set_date_time_label(str(hack.timestamp))
                
                self.frames.append(hack_frame)
  
class Landing_Page (Frame):
    def __init__(self, parent, character):
        Frame.__init__(self, parent)

        self.parent = parent
        self.character = character
        self.complete_button_image = PhotoImage(file=os.path.join("assets", "art", "check.gif"))
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 1)
        #self.columnconfigure(3, weight = 1)
        #self.rowconfigure (4, weight =1)
        #self.rowconfigure (5, weight = 1)
        self.rowconfigure (6, weight = 1)
        
        

        self.habit_dict = {k:self.character.hacks[k]
                           for k in self.character.hacks
                           if self.character.hacks[k].h_type == 'habit'}
        self.dailies_dict = {k:self.character.hacks[k]
                             for k in self.character.hacks
                             if self.character.hacks[k].h_type == 'daily'}
        self.tasks_dict = {k:self.character.hacks[k]
                           for k in self.character.hacks
                           if self.character.hacks[k].h_type == 'task'}

        self.set_landing_window()
        self.go_to_habits_button = Button(self.habit_area,
                                          text = 'GO TO HABITS',
                                          cursor = 'hand2',
                                          style = 'go_to_button.TButton')
                                                  
        self.go_to_dailies_button = Button(self.daily_area,
                                           text = 'GO TO DAILIES',
                                           cursor = 'hand2',
                                           style = 'go_to_button.TButton')
                                           
        self.go_to_tasks_button = Button(self.task_area,
                                         text='GO TO TASKS',
                                         cursor = 'hand2',
                                         style = 'go_to_button.TButton')
                                        
        
        go_to_button_style = Style()

        go_to_button_style.configure('go_to_button.TButton',
                                     font = 'arial 14 bold',
                                     relief = 'flat',
                                     padding = 5,
                                     foreground ='#54C9EB',
                                     background = '#283D57')
        self.go_to_habits_button.pack(fill = X, expand = False, side = BOTTOM)
        self.go_to_dailies_button.pack(fill = X, expand = False, side = BOTTOM)
        self.go_to_tasks_button.pack(fill = X, expand = False, side = BOTTOM)




    def redraw(self, character):
        self.go_to_habits_button.destroy()
        self.go_to_dailies_button.destroy()
        self.go_to_tasks_button.destroy()
        

        
        #Update class' character data instance
        self.character = character
        self.habit_dict = {k:self.character.hacks[k]
                           for k in self.character.hacks
                           if self.character.hacks[k].h_type == 'habit'}
        self.dailies_dict = {k:self.character.hacks[k]
                             for k in self.character.hacks
                             if self.character.hacks[k].h_type == 'daily'}
        self.tasks_dict = {k:self.character.hacks[k]
                           for k in self.character.hacks
                           if self.character.hacks[k].h_type == 'task'}

        #Destroy frames
        self.habit_area.remove_frames()
        self.daily_area.remove_frames()
        self.task_area.remove_frames()
        
        #Update area frames
        self.habit_area.set_frames(self.habit_dict)
        self.daily_area.set_frames(self.dailies_dict)
        self.task_area.set_frames(self.tasks_dict)

        self.go_to_habits_button = Button(self.habit_area,
                                          text = 'GO TO HABITS',
                                          cursor = 'hand2',
                                          style = 'go_to_button.TButton')
                                                  
        self.go_to_dailies_button = Button(self.daily_area,
                                           text = 'GO TO DAILIES',
                                           cursor = 'hand2',
                                           style = 'go_to_button.TButton')
                                           
        self.go_to_tasks_button = Button(self.task_area,
                                         text='GO TO TASKS',
                                         cursor = 'hand2',
                                         style = 'go_to_button.TButton')
                                        
        
        go_to_button_style = Style()

        go_to_button_style.configure('go_to_button.TButton',
                                     font = 'arial 14 bold',
                                     relief = 'flat',
                                     padding = 5,
                                     foreground ='#54C9EB',
                                     background = '#283D57')
        self.go_to_habits_button.pack(fill = X, expand = False, side = BOTTOM)
        self.go_to_dailies_button.pack(fill = X, expand = False, side = BOTTOM)
        self.go_to_tasks_button.pack(fill = X, expand = False, side = BOTTOM)

        self.parent.bind_buttons()
        
    def set_landing_window(self):
        #label above progress bar
        self.progress_label = Label(self, text="Daily Progress", padding=0)
        self.progress_label.grid(row = 4, column =2 ,sticky='ew', pady=4, padx=5)
        self.progress_label.configure(anchor = CENTER, font='arial 18 italic')
        self.progress_label.rowconfigure(4, weight =1) 
        self.progress_label.columnconfigure(3, weight = 1)

        #progress bar
        #progress = Progressbar(self, orient = 'horizontal', mode= 'determinate')
        #progress.grid(row = 5, column=0, columnspan = 6, stick = 'ew', padx = 3)

        #progress.start()
        #progress.rowconfigure(5, weight =1)
        #progress.columnconfigure(0, weight = 1)

        #three areas for adding dailies, task, habit widgets
 
        self.habit_area = Landing_Area_Frame(self, 'habit')
        self.habit_area.set_header('HABITS', '#D95B5B')
        self.habit_area.set_frames(self.habit_dict)
        self.habit_area.grid(row = 6, column = 0,
                             columnspan = 2, rowspan = 4,
                             padx = 5, sticky = 'enws')

        self.habit_area.grid_propagate(False)
        self.habit_area.rowconfigure(6, weight = 1)
        self.habit_area.columnconfigure(0, weight = 1)


        self.daily_area = Landing_Area_Frame(self, 'daily')
        self.daily_area.set_header('DAILIES', '#9AD95B')
        self.daily_area.set_frames(self.dailies_dict)
        self.daily_area.grid(row = 6, column = 2, columnspan = 2,
                             rowspan = 4, padx = 5, sticky = 'enws')
        self.daily_area.rowconfigure(6, weight = 1)
        self.daily_area.columnconfigure(2, weight = 1)
        self.daily_area.grid_propagate(False)
        
        
        self.task_area = Landing_Area_Frame(self, 'task')
        self.task_area.set_header('TASKS', '#5BADD9')
        self.task_area.set_frames(self.tasks_dict)
        self.task_area.grid(row = 6, column = 4, columnspan = 2,
                            rowspan = 4, padx = 5, sticky = 'news')
        self.task_area.rowconfigure(6, weight = 1)
        self.task_area.columnconfigure(4, weight = 1)
        self.task_area.grid_propagate(False)


        
        #Bottom go to buttons

        

        
 



    def start(self):
        self.progress["value"] = 0
        self.max = 24
        self.progress["midnight"]=24
        self.progress["value"] = 12

    def button_default(self):
        #Placeholder
        pass
