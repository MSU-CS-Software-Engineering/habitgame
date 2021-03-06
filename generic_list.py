from tkinter  import *
from tkinter.ttk import *

from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)



class Generic (Frame):
    def __init__(self, parent, character):
        Frame.__init__(self, parent)
        self.parent = parent
        self.character = character
        self.rowconfigure(4, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.list_window()

    def list_window(self):

        habit_dict =   {k:self.character.hacks[k] 
                        for k in self.character.hacks 
                          if self.character.hacks[k].h_type == 'habit'}
        dailies_dict = {k:self.character.hacks[k] 
                        for k in self.character.hacks 
                          if self.character.hacks[k].h_type == 'daily'}
        tasks_dict =   {k:self.character.hacks[k] 
                        for k in self.character.hacks 
                          if self.character.hacks[k].h_type == 'task'}


        # Create canvas
        canvas = ResizingCanvas(self,width = 1350, background = '#EBEDF1')
        #canvas = Canvas(self, background = 'gray', width = 800, height = 600)

        canvas.grid(row = 4, column = 0, sticky = 'news', padx = 5, pady = 5)
        canvas.grid_rowconfigure(4, weight = 1)
        canvas.grid_columnconfigure(0, weight = 1)


        # Create scrollbars

        yscrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        yscrollbar.grid(row = 4, column = 1, sticky = 'ns')
        yscrollbar.grid_rowconfigure(4, weight = 1)
        yscrollbar.grid_columnconfigure(1, weight = 1)
        # Create frame inside canvas
        frame_style = Style()
        
        frame_style.configure("f.TFrame", background = '#EBEDF1')
        
        frame = Frame(canvas)
        
        # Attach canvas to scrollbars
        canvas.configure(yscrollcommand=yscrollbar.set)

        #Scrollbar function and bindings
        def set_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
            
        canvas.bind('<Configure>', set_scrollregion)

        # enable mouse wheel scrolling
        def scroll_mouse(event):
            """ allows for mouse wheel scrolling """
            try:
                canvas.yview_scroll(-1 * int(event.delta/120), "units")
            except:
                pass

        canvas.bind("<MouseWheel>", lambda e: scroll_mouse(e))
        
        canvas.addtag_all("all")
        '''
        for i in range(150):
            x = " This is a sentence "
            
            
            label= Label(frame, text = x, style = "L.TLabel")
            label.grid(row = i, column = 0, sticky = 'nsew')
        '''
        row_number = 0
        for h in habit_dict:
            ############
            habit_frame = Frame(frame, width = 800, height = 95, style = "f.TFrame", padding = 5)
            habit_frame.grid(row = row_number, column = 0, sticky = 'news')
            row_number += 1
            #habit_frame.grid_propagate(False)
            habit_frame.columnconfigure(0, weight = 1)
            canvas.addtag_all("all")
            

            habit_name = Label(habit_frame, text = habit_dict[h].title, font = 'arial 14', 
                               padding = 5, foreground = '#64D729', background = '#323232')
            habit_name.grid(row = 0, column = 0, columnspan = 5, sticky = 'news')
            habit_name.configure(anchor = CENTER)
   
            #Description
            habit_description = Frame(habit_frame, width = 400)
            habit_description.grid(row = 2, column = 0,rowspan = 2,
                                   sticky = 'news')


            #####
            habit_description_label = Label(habit_description, text = "Description", 
                                            padding = 3, font = 'arial 12 bold', background = "#D5EA8A")
            
            habit_description_label.grid(row = 0, column = 0,
                                         sticky = 'nesw')
            
 
            habit_description_label.configure(anchor = CENTER)
            #habit_description_label.grid_propagate(False)
            ####
            
            #x = habit.description
            x = "this needs to be fixed"
            #x = "This is a very very very very very very very very very very very very very very very very very very very veryThis is a very very very very very very very very very very very very very very very very very very very veryThis is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long sentence"
            habit_description_value = Label(habit_description, text = x, wraplength = 700, padding = 5,
                                            font = 'arial 12', background = '#EFE4B0')
            habit_description_value.grid(row = 1, column = 0)

            # frame for list item info
            info_frame = Frame(habit_frame, style = 'info.TFrame', padding = 3)
            info_frame.grid(row = 1, column = 0, sticky = 'nesw')
            frame_style.configure('info.TFrame', background = '#232323')
            
            #Type
            type_frame = Frame(info_frame)
            type_frame.grid(row = 0, column = 0, sticky = 'nesw')
            
            habit_type = Label(type_frame, text = "Type: ", font = 'arial 12 bold',
                               background = '#232323', foreground = 'white')
            habit_type.pack(side = LEFT, fill = BOTH)
            
            habit_type_value = Label(type_frame, text = "Habit", font = 'arial 12 bold',
                                     background = '#232323', foreground = '#36AEF5')
            habit_type_value.pack(side = LEFT, fill = BOTH, ipadx = 7)

            #Value
            value_frame = Frame(info_frame)
            value_frame.grid(row = 0, column = 1, sticky = 'nesw')
            
            habit_value = Label(value_frame, text = "Value: ", font = 'arial 12 bold',
                                background = '#232323', foreground = 'white')
            habit_value.pack(side = LEFT, fill = BOTH)
            
            habit_value_value = Label(value_frame, text = '$' + str(habit_dict[h].value),
                                      font = 'arial 12 bold', background = '#232323', foreground='#3BB623')
            habit_value_value.pack(side = LEFT, fill = BOTH, ipadx = 7)

            #Experience
            exp_frame = Frame(info_frame)
            exp_frame.grid(row = 0, column = 2, sticky = 'nesw')
            
            habit_exp = Label(exp_frame, text = "Experience: ", font = 'arial 12 bold',
                              background = '#232323', foreground = 'white')
            habit_exp.pack(side = LEFT, fill = BOTH)
            
            habit_exp_value = Label(exp_frame, text = habit_dict[h].value, font = 'arial 12 bold',
                                    background = '#232323', foreground='#C5BD25')
            habit_exp_value.pack(side = LEFT, fill = BOTH, ipadx = 7)

            #Date Added
            timestamp_frame= Frame(info_frame)
            timestamp_frame.grid(row = 0, column = 3, sticky = 'nesw')
            
            habit_timestamp = Label(timestamp_frame, text = "TimeStamp: ", font = 'arial 12 bold',
                                    background = '#232323', foreground='white')
            habit_timestamp.pack(side = LEFT, fill = BOTH)
            
            habit_timestamp_value = Label(timestamp_frame, text = habit_dict[h].timestamp, font = 'arial 12 bold',
                                          background = '#232323', foreground='#FF7F2A')
            habit_timestamp_value.pack(side = LEFT, fill = BOTH, ipadx = 7)
            

        for t in tasks_dict:
            ############
            tasks_frame = Frame(frame, width = 800 , height = 95, style = "f.TFrame", padding = 5)
            tasks_frame.grid(row = row_number, column = 0, sticky = 'news')
            tasks_frame.columnconfigure(0, weight = 1)
            row_number += 1
            
            #habit_frame.grid_propagate(False)
            canvas.addtag_all("all")
            

            task_name = Label(tasks_frame, text = tasks_dict[t].title, font = 'arial 14',
                              padding = 5, foreground = '#64D729', background = '#323232')
            task_name.grid(row =0, column = 0, columnspan = 5,sticky = 'news')
            task_name.configure(anchor = CENTER)
   
            #Description
            tasks_description = Frame(tasks_frame, width = 400)
            tasks_description.grid(row = 1, column = 0, rowspan = 2, sticky = 'news')
            
            #####
            tasks_description_label = Label(tasks_description, text = "Description", padding = 3,
                                            font = 'arial 12 bold', background = "#D5EA8A")
            
            tasks_description_label.grid(row = 0, column = 0, sticky = 'nesw')
            
            
            tasks_description_label.configure(anchor = CENTER)
            #habit_description_label.grid_propagate(False)
            ####
            
            #x = habit.description
            x = "this needs to be fixed"
            #x = "This is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long sentence"
            tasks_description_value = Label(tasks_description, text = x, wraplength = 700, padding = 5,
                                            font = 'arial 12', background = '#EFE4B0')
            tasks_description_value.grid(row = 1, column = 0, sticky= 'news')
   

            # frame for list item info
            info_frame = Frame(tasks_frame, style = 'info.TFrame', padding = 3)
            info_frame.grid(row = 1, column = 0, sticky = 'nesw')
            frame_style.configure('info.TFrame', background = '#232323')

            #Type
            type_frame = Frame(info_frame)
            type_frame.grid(row = 0, column = 0, sticky = 'nesw')
            
            tasks_type = Label(type_frame, text = "Type: ", font = 'arial 12 bold',
                               background = '#232323', foreground = 'white')
            tasks_type.pack(side = LEFT, fill = BOTH)
            
            tasks_type_value = Label(type_frame, text = "Task", font = 'arial 12 bold',
                                     background = '#232323', foreground = '#36AEF5')
            tasks_type_value.pack(side = LEFT, fill = BOTH, ipadx = 7)
            
            #Value
            value_frame = Frame(tasks_frame)
            value_frame.grid(row = 0, column = 1, sticky = 'nesw')
            
            tasks_value = Label(value_frame, text = "Value: ", font = 'arial 12 bold',
                                background = '#232323', foreground = 'white')
            tasks_value.pack(side = LEFT, fill = BOTH)
            
            tasks_value_value = Label(value_frame, text = '$' + str(tasks_dict[t].value),
                                      font = 'arial 12 bold', background = '#232323', foreground='#3BB623')
            tasks_value_value.pack(side = LEFT, fill = BOTH, ipadx = 7)

            #Experience
            exp_frame = Frame(tasks_frame)
            exp_frame.grid(row = 0, column = 2, sticky = 'nesw')
            
            tasks_exp = Label(exp_frame, text = "Experience: ", font = 'arial 12 bold',
                              background = '#232323', foreground = 'white')
            tasks_exp.pack(side = LEFT, fill = BOTH)
            
            tasks_exp_value = Label(exp_frame, text = tasks_dict[t].value, font = 'arial 12 bold',
                                    background = '#232323', foreground='#C5BD25')
            tasks_exp_value.pack(side = LEFT, fill = BOTH, ipadx = 7)

            #Date Added
            timestamp_frame= Frame(tasks_frame)
            timestamp_frame.grid(row = 0, column = 3, sticky = 'nesw')
            
            tasks_timestamp = Label(timestamp_frame, text = "TimeStamp: ", font = 'arial 12 bold',
                                    background = '#232323', foreground='white')
            tasks_timestamp.pack(side = LEFT, fill = BOTH)
            
            tasks_timestamp_value = Label(timestamp_frame, text = tasks_dict[t].timestamp, font = 'arial 12 bold',
                                          background = '#232323', foreground='#FF7F2A')
            tasks_timestamp_value.pack(side = LEFT, fill = BOTH, ipadx = 7)
            #####################


            #Buttons
            button_style = Style()
            button_style.configure("B.TButton", relief = RAISED, background = "gray")
            complete = Button(tasks_frame, text = "Complete", style = "B.TButton",
                              command = self.completed)
            complete.grid(row = 0, column = 5, sticky = 'news')
            
            edit = Button(tasks_frame, text = "Edit",style = "B.TButton",
                          command = self.edit)
            edit.grid(row = 1, column = 5, sticky = 'news')

            
            delete = Button(tasks_frame, text = "Delete",style = "B.TButton",
                            command = self.delete)
            delete.grid(row = 2, column = 5, sticky = 'news')


        for d in dailies_dict:
            ############
            dailies_frame = Frame(frame, width = 800, height = 95, style = "f.TFrame", padding = 5)
            dailies_frame.grid(row = row_number, column = 0, sticky = 'news')
            dailies_frame.columnconfigure(0, weight = 1)
            row_number += 1
            #habit_frame.grid_propagate(False)
            canvas.addtag_all("all")
            

            dailies_name = Label(dailies_frame, text = dailies_dict[d].title, font = 'arial 14',
                                 padding = 5, foreground = '#64D729', background = '#323232')
            dailies_name.grid(row = 0, column = 0, columnspan = 5, sticky = 'news')
            dailies_name.configure(anchor = CENTER)

            #Description
            dailies_description = Frame(dailies_frame, width = 400)
            dailies_description.grid(row = 2, column = 0, columnspan = 5,
                                   sticky = 'news')
            
            #####
            dailies_description_label = Label(dailies_description, text = "Description", padding = 3,
                                              font = 'arial 12 bold', background = "#D5EA8A")
            
            dailies_description_label.grid(row = 0, column = 0, sticky = 'nesw')
            
            
            dailies_description_label.configure(anchor = CENTER)
            #habit_description_label.grid_propagate(False)
            ####
            
            #x = habit.description
            x = "This is a very very very very very very very very very very very very very very very very very very very veryThis is a very very very very very very very very very very very very very very very very very very very veryThis is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long sentence"
            #x += "This is a very very very very very very very very very very very very very very very very very very very veryThis is a very very very very very very very very very very very very very very very very very very very veryThis is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long sentence"

            dailies_description_value = Label(dailies_description, text = x, wraplength = 700, padding = 5,
                                             font = 'arial 12', background = '#EFE4B0')
            dailies_description_value.grid(row = 1, column = 0, sticky= 'news')


            # frame for list item info
            info_frame = Frame(dailies_frame, style = 'info.TFrame', padding = 3)
            info_frame.grid(row = 1, column = 0, sticky = 'nesw')
            frame_style.configure('info.TFrame', background = '#232323')
            
            #Type
            type_frame = Frame(info_frame)
            type_frame.grid(row = 0, column = 0, sticky = 'nesw')
            
            dailies_type = Label(type_frame, text = "Type: ", font = 'arial 12 bold',
                                 background = '#232323', foreground = 'white')
            dailies_type.pack(side = LEFT, fill = BOTH)
            
            dailies_type_value = Label(type_frame, text = "Daily", font = 'arial 12 bold',
                                       background = '#232323', foreground = '#36AEF5')
            dailies_type_value.pack(side = LEFT, fill = BOTH, ipadx = 7)
            
            #Value
            value_frame = Frame(info_frame)
            value_frame.grid(row = 0, column = 1, sticky = 'nesw')
            
            dailies_value = Label(value_frame, text = "Value: ", font = 'arial 12 bold',
                                  background = '#232323', foreground = 'white')
            dailies_value.pack(side = LEFT, fill = BOTH)
            
            dailies_value_value = Label(value_frame, text = '$' + str(dailies_dict[d].value),
                                        font = 'arial 12 bold', background = '#232323', foreground='#3BB623')
            dailies_value_value.pack(side = LEFT, fill = BOTH, ipadx = 7)

            #Experience
            exp_frame = Frame(info_frame)
            exp_frame.grid(row = 0, column = 2, sticky = 'nesw')
            
            dailies_exp = Label(exp_frame, text = "Experience: ", font = 'arial 12 bold',
                                background = '#232323', foreground = 'white')
            dailies_exp.pack(side = LEFT, fill = BOTH)
            
            dailies_exp_value = Label(exp_frame, text = dailies_dict[d].value, font = 'arial 12 bold',
                                      background = '#232323', foreground='#C5BD25')
            dailies_exp_value.pack(side = LEFT, fill = BOTH, ipadx = 7)
            
            #Date Added
            timestamp_frame= Frame(info_frame)
            timestamp_frame.grid(row = 0, column = 3, sticky = 'nesw')
            
            dailies_timestamp = Label(timestamp_frame, text = "TimeStamp: ", font = 'arial 12 bold',
                                      background = '#232323', foreground='white')
            dailies_timestamp.pack(side = LEFT, fill = BOTH)
            
            dailies_timestamp_value = Label(timestamp_frame, text = dailies_dict[d].timestamp, font = 'arial 12 bold',
                                            background = '#232323', foreground='#FF7F2A')
            dailies_timestamp_value.pack(side = LEFT, fill = BOTH, ipadx = 7)
            #####################



        canvas.create_window((0,0), window = frame)
    def edit(self):
        pass
    def delete(self):
        pass
    def completed(self):
        pass
        



def main():
    #For Testing purposes
    #root = Tk()
    #test=Generic(root)
    #root.mainloop()
    #End Test

    pass

if __name__ == '__main__':
    main()  

    

        
