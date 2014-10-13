from tkinter  import *
from tkinter.ttk import *

from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.
class Generic (Frame):
    def __init__(self, parent, character):
        Frame.__init__(self, parent)
        self.parent = parent
        self.character = character
        #self.rowconfigure(4, weight = 1)
        #self.columnconfigure(0, weight = 1)
        #self.columnconfigure(1, weight = 1)

        self.list_window()

    def list_window(self):

        
        habit_list = self.character.habits
        habit_length = len(habit_list)

        # Create canvas
        canvas = Canvas(self, background = 'gray', width = 800, height = 600)
        canvas.grid(row = 4, column = 0)
        #canvas.grid_rowconfigure(4, weight = 1)
        #canvas.grid_columnconfigure(0, weight = 1)
    
        # Create scrollbars

        yscrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        yscrollbar.grid(row=4, column = 1, sticky = 'news')
        #yscrollbar.grid_rowconfigure(4, weight = 1)
        #yscrollbar.grid_columnconfigure(1, weight = 1)
        # Create frame inside canvas
        frame_style = Style()
        
        frame_style.configure("f.TFrame", background = 'black')
        
        frame = Frame(canvas)
        

        # Attach canvas to scrollbars
        canvas.configure(yscrollcommand=yscrollbar.set)

        #Scrollbar function and bindings
        def set_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        canvas.bind('<Configure>', set_scrollregion)
        '''
        for i in range(150):
            x = " This is a sentence "
            
            
            label= Label(frame, text = x, style = "L.TLabel")
            label.grid(row = i, column = 0, sticky = 'nsew')
        '''

        for habit in habit_list:
            ############
            habit_frame = Frame(frame, width = 800 , height = 95,style = "f.TFrame")
            habit_frame.grid(row = habit.ID, column = 0)
            habit_frame.grid_propagate(False)
            
            

            habit_name = Label(habit_frame, text = habit.title,
                               background = 'gray', relief = GROOVE)
            habit_name.grid(row =0, column = 0, columnspan = 5,sticky = 'news')
            habit_name.configure(anchor = CENTER)
   
            #Description

            habit_description = Frame(habit_frame, width = 400)
            habit_description.grid(row = 1, column = 0,rowspan = 2,
                                   sticky = 'news')
            

            scrollbar = Scrollbar(habit_description)
            scrollbar.grid(row = 1, column = 1, sticky = 'nesw')
            

            #####
            habit_description_label = Label(habit_description, text = "Description",
                                            background = "gray", relief = GROOVE)
            
            habit_description_label.grid(row = 0, column = 0,
                                         sticky = 'nesw')
            
            
            habit_description_label.configure(anchor = CENTER)
            #habit_description_label.grid_propagate(False)
            ####
            
            #x = habit.description
            x = "This is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long sentence"
            habit_description_value = Text(habit_description, height = 2, width = 56,
                                           relief = GROOVE, bd = 3)
            habit_description_value.grid(row = 1, column = 0, sticky= 'news')
            habit_description_value.configure(yscrollcommand = scrollbar.set)
            scrollbar.configure(command = habit_description_value.yview)
            habit_description_value.insert(INSERT, x)
            habit_description_value.grid_propagate(False)



            #Type
            type_frame = Frame(habit_frame)
            type_frame.grid(row = 1, column = 3, sticky = 'nesw')
            
            habit_type = Label(type_frame, text = "Type:", width = 9,
                               background = 'gray', relief = GROOVE)
            habit_type.pack(side = LEFT, fill = BOTH)
            
            habit_type_value = Label(type_frame, text = habit.habit_type, width = 10,
                               background = 'white', relief = GROOVE)
            habit_type_value.pack(side = LEFT, fill = BOTH)
            #Value
            value_frame = Frame(habit_frame)
            value_frame.grid(row = 1, column = 4, sticky = 'nesw')
            
            habit_value = Label(value_frame, text = "Value:", width = 9,
                               background = 'gray', relief = GROOVE)
            habit_value.pack(side = LEFT, fill = BOTH)
            
            habit_value_value = Label(value_frame, text = habit.value, width = 4,
                               background = 'white', relief = GROOVE)
            habit_value_value.pack(side = LEFT, fill = BOTH)

            #Date Added
            timestamp_frame= Frame(habit_frame)
            timestamp_frame.grid(row = 2, column = 3, sticky = 'nesw')
            
            habit_timestamp = Label(timestamp_frame, text = "TimeStamp:", width = 9,
                               background = 'gray', relief = GROOVE)
            habit_timestamp.pack(side = LEFT, fill = BOTH)
            
            habit_timestamp_value = Label(timestamp_frame, text = habit.timestamp, width = 10,
                               background = 'white', relief = GROOVE)
            habit_timestamp_value.pack(side = LEFT, fill = BOTH)
            #Experience
            exp_frame = Frame(habit_frame)
            exp_frame.grid(row = 2, column = 4, sticky = 'nesw')
            
            habit_exp = Label(exp_frame, text = "Experience:", width = 9,
                               background = 'gray', relief = GROOVE)
            habit_exp.pack(side = LEFT, fill = BOTH)
            
            habit_exp_value = Label(exp_frame, text = habit.value, width = 4,
                               background = 'white', relief = GROOVE)
            habit_exp_value.pack(side = LEFT, fill = BOTH)
            #####################

            #Buttons
            button_style = Style()
            button_style.configure("B.TButton", relief = RAISED, background = "gray")
            complete = Button(habit_frame, text = "Complete", style = "B.TButton",
                              command = self.completed)
            complete.grid(row = 0, column = 5, sticky = 'news')
            
            edit = Button(habit_frame, text = "Edit",style = "B.TButton",
                          command = self.edit)
            edit.grid(row = 1, column = 5, sticky = 'news')

            
            delete = Button(habit_frame, text = "Delete",style = "B.TButton",
                            command = self.delete)
            delete.grid(row = 2, column = 5, sticky = 'news')
            


        canvas.create_window((0,0), window = frame)
    def edit(self):
        pass
    def delete(self):
        pass
    def completed(self):
        pass



    

        
