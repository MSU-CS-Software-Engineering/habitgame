"""
  Habit game core

  Dependencies: landing_page.py
"""

#import landing_page.py
import os.path
from datetime import date #For timestamps
from tkinter  import *
from tkinter.ttk import *
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders

class Character:
    """
      Class for Habit character profile

      Variables:
        name: Name of character       (string)
        cash: Total currency          (int)
        exp: Total experience points  (int)
        level: Current level          (int)
        habits: Current habits        (list of Habit objects)
        items: Owned (soft|hard)ware  (list of Item objects)
    """
    def __init__(self, name):
        self.name = name
        self.cash = 0
        self.exp = 0
        self.level = 1
        self.habits = []
        self.items = []
    
    def serialize(self):
        """
        Serializes class properties to a dictionary 
        which can then be converted to a string
        """
        character_dict = {'name': self.name,
                          'cash': self.cash,
                          'exp' : self.exp,
                          'level' : self.level,
                          'habits': None,
                          'items': None}


        habits_list = []
        items_list = []
        
        for habit in self.habits:
            habits_list.append(habit.serialize())

        
        for item in self.items:
            items_list.append(item.serialize())

        character_dict['habits'] = habits_list
        character_dict['items'] = items_list
        
        return character_dict
            
    def show_info(self):
        """
        Displays the characters current information:
        Cash, name, experience, level, habits, and items
        """
        print("Player Info:")
        print("Name:       "+self.name)
        print("Cash:      $"+str(self.cash))
        print("Experience: "+str(self.exp))
        print("Level:      "+str(self.level))
        print("\n\nHabits:\n-------")
        self.show_habits()
        print("\n\nItems:\n------")
        self.show_items()


    def add_habit(self, habit):
        habit_ID = 0

        if len(self.habits) != 0:
            habit_ID = len(self.habits)
        
        habit.ID = habit_ID
        
        self.habits.append(habit)
        return habit_ID

    def remove_habit(self, habit_ID):
        try:
            print("Removed habit:", self.habits.pop(habit_ID))
            self.set_habit_IDs()
        except:
            print("Error: Invalid habit id")

    def get_habit(self, habit_ID):
        try:
            habit = self.habits[habit_ID]
            return habit
        except:
            print("Error: Invalid habit id")


    def set_habit_IDs(self):
        for habit in enumerate(self.habits):
            habit[1].ID = habit[0]


    def show_habit(self, habit_id):
        try:
            habit = self.habits[habit_id]
            print("Name:    " + habit.name)
            print("ID:      " + str(habit.ID))
            print("Type:    " + habit.habit_type)
            print("Timestamp: " + str(habit.timestamp))
            print("Value:   " + str(habit.value))
            print("Exp Pts: " + str(habit.exp))

        except:
            print("Error: Invalid habit_id")

    def show_habits(self):
        for habit in self.habits:
            self.show_habit(habit.ID)


    def add_item(self, item):
        item_ID = 0
        if len(self.items) != 0:
            item_ID = len(self.items)
        
        item.ID = item_ID
        self.items.append(item)
        return item_ID

    def remove_item(self, item_ID):
        try:
            print("Removed:", self.items.pop(item_ID))
            self.set_item_IDs()
        except:
            print("Error: Invalid item ID")


    def get_item(self, item_ID):
        try:
            item = self.items[item_ID]
            return self.items[item_ID]
        except:
            print("Error: Invalid item ID")


    def set_item_IDs(self):
        for item in enumerate(self.items):
            item[1].ID = item[0]

 
    def show_item(self, item_ID):
        
        try:
            item = self.items[item_ID]
            print("Name:   " + item.name)
            print("ID:     " + str(item.ID))
            print("Value:  " + str(item.value))
            print("Uses:   " + str(item.uses))
        except:
            print("Error: Invalid item ID")

    def show_items(self):
        for item in self.items:
            self.show_item(item.ID)

class Habit:
    """
      Class for Individual Habits

      Variables:
        name: Name of habit                          (string)
        ID: Number to hold index in                  (int)
        habitlist
        habit_type: Type of habit (Daily, task, etc) (string)
        timestamp: Last-accessed date                (date)
        value: Cash reward/penalty                   (int)
        exp: Experience point value                  (int)
    """
    def __init__(self, name, value, exp, habit_type, ID=0):
        self.name = name
        self.ID = ID
        self.habit_type = habit_type
        self.timestamp = date.today()
        self.value = value
        self.exp = exp

    def serialize(self):
        """
        Serializes class properties to a dictionary 
        which can be converted to a string
        """
        habit_dict = {'name':self.name,
                      'ID'  :self.ID,
                      'timestamp':str(self.timestamp),
                      'type':self.habit_type,
                      'value':self.value,
                      'exp':self.exp}
        
        return habit_dict
    
class Item:
    """
      Class for purchasable software/hardware

      Variables:
        name: Name of item                                (string)
        ID: Number to hold index in itemlist              (int)
        image: Name of accompanying image                 (string)
        value: Currency value of item                     (int)
        uses: Uses before item expires [-1 for infinite]  (int)
        effect: Special function that the item performs   (function)
    """
    def __init__(self, name, image, value, uses, effect = None):
        self.name = name
        self.ID = 0
        self.image = image
        self.value = value
        self.uses = uses
        self.effect = effect

    def serialize(self):
        """
        Serializes class properties to a dictionary
        which can be converted to a string
        """
        item_dict = {'name':self.name,
                      'ID':self.ID,
                      'image':self.image,
                      'value':self.value,
                      'uses':self.uses,
                      'effect':self.effect}
        
        return item_dict

class Game_Data:
    """
    Class for main game functions
    """
    def __init__(self):
        self.savefile = 'character.txt'
        self.character_data = {}

    def save_data(self, character):
        """
        Saves the current character data to
        Game_Data's character_data 
        """
        self.character_data = character.serialize()
        print("Character data saved")
        
    def save_to_file(self):
        """
        Saves character_data to file
        """
        
        if os.path.isfile(self.savefile):
           file_overwrite = input("Overwrite existing data file?(Y/N)")
           if file_overwrite == "Y":
               try:
                   f = open(self.savefile, 'w')
                   f.write(str(self.character_data))
                   print("Data written to file")
                   f.close()
                   
               except:
                   print("Failed to write data to file")
                   
           else:
               print("File not saved")
        else:
            try:
                f = open(self.savefile, 'w')
                f.write(str(self.character_data))
                print("Data written to file")
                f.close()
                
            except:
                self.error("Failed to write data to file")
        
    def load_data(self):
        """
        Loads character_data from file then
        stores it into character_data dict
        """
        try:
            f = open(self.savefile, 'r')
            character_data = eval(f.read())
            self.character_data = character_data
            #return self.build_character(self.character_data)
        
        except:
            self.error('Failed to load data')

    def build_character(self, character_data):
        """
        Builds a character object from the Game_Data's 
        character_data. 
        """
        try:
            new_character = Character(character_data['name'])
            new_character.level = character_data['level']
            new_character.exp = character_data['exp']
            new_character.cash = character_data['cash']
            
            for habit in character_data['habits']:
                new_habit = Habit(habit['name'],
                                  habit['value'],
                                  habit['exp'],
                                  habit['habit_type'],
                                  habit['ID'])
            
                new_character.add_habit(new_habit)
            
            for item in character_data['items']:
                new_item = Item(item['name'],
                                item['image'],
                                item['value'],
                                item['uses'],
                                item['effect'])
            
                new_character.add_item(new_item)

            return new_character

        except:
            self.error("Failed to build character from" \
                       " default character data")
    
    def error(self, error_message):
        print("ERROR:", error_message)


def load(name):
    """
    Loads a default character data configuration. 
    Used for debugging
    """
    new_character = Character(name)
    
    habit_1 = Habit('Read more books', 50, 10, 'habit')  
    habit_2 = Habit('Eat more veggies', 100, 15, 'daily')
    habit_3 = Habit('Get more sleep', 20, 5, 'task')

    item_1 = Item('Laptop', 'laptop.jpg', 5, 1)
    item_2 = Item('CAT-5 Cable', 'cat5.jpg', 4, 15)
    item_3 = Item('SSD', 'ssd.jpg', 6, 20)

    habits = []
    items = []

    habits.append(habit_1)
    habits.append(habit_2)
    habits.append(habit_3)

    items.append(item_1)
    items.append(item_2)
    items.append(item_3)

    for habit in habits:
        new_character.add_habit(habit)

    for item in items:
        new_character.add_item(item)

    return new_character


class GUI (Frame):

    def __init__(self, master, character):
        Frame.__init__(self, master)   
        pad = 3
        self.master = master
        self.character = character
        self.character_name = StringVar()
        self.character_exp = StringVar()
        self.character_cash = StringVar()
        self.character_level = StringVar()
        self.character_name.set(self.character.name)
        self.character_exp.set(self.character.exp)
        self.character_cash.set(self.character.cash)
        self.character_level.set(self.character.level)
        self._geom='800x600+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        self.initUI()
        
    def initUI(self):
        self.master.title("Daily Hack")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, pad=7)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(9, pad=7)
        
        name_lalel = Label(self, text="Player Name")
        name_lalel.grid(row = 0, column = 0,sticky=W, pady=4, padx=5)

        name = Label (self, textvariable = self.character_name)
        name.grid(row = 0, column = 1, sticky=W, pady=4, padx=5)
        

        exp_label = Label(self, text="Experience:")
        exp_label.grid(row = 1, column =0,sticky=W, pady=4, padx=5)

        exp = Label(self, textvariable = self.character_exp)
        exp.grid(row = 1, column =1,sticky=W, pady=4, padx=5)

        cash_label = Label(self, text="CASH:")
        cash_label.grid(row = 2, column =0 ,sticky=W, pady=4, padx=5)

        cash = Label(self, textvariable= self.character_cash)
        cash.grid(row = 2, column =1 ,sticky=W, pady=4, padx=5)

        level_label = Label(self, text="LEVEL:")
        level_label.grid(row = 3, column =0 ,sticky=W, pady=4, padx=5)

        level = Label(self, textvariable = self.character_level)
        level.grid(row = 3, column =1 ,sticky=W, pady=4, padx=5)

        

        mb=  Menubutton ( self, text="Options" )
        mb.grid(row = 0, column = 5, sticky = E)
        mb.menu  =  Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
    
        mayoVar  = IntVar()
        ketchVar = IntVar()
        mb.menu.add_command( label="Habits", command = habit)
        mb.menu.add_command( label="Dailies", command = dailies )
        mb.menu.add_command( label="Tasks", command = task )
        mb.menu.add_command( label="Shop", command = buy )
        mb.menu.add_command ( label="Game", command = no_where)
        mb.menu.add_command( label="Settings", command = no_where)

        footer = Label(self, text="Copyright 2014")
        footer.grid(row =9, columnspan = 7, sticky = (N, E, W, S))
        footer.configure(background = 'black', foreground = 'white', anchor = CENTER)
        
        #manual test for update
        item_test = Item('SSD', 'ssd.jpg', 6, 1)
        self.complete_habit(1)
        self.buy_item(item_test)
        self.use_item(0)
        self.character.show_info()

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
    
    def complete_habit(self, habit_ID):
        habit = self.character.get_habit(habit_ID)
        self.character.cash += habit.value
        self.character.exp += habit.exp
        self.character.remove_habit(habit_ID)
        self.character.set_habit_IDs()
        self.character_exp.set(self.character.exp)
        self.character_cash.set(self.character.cash)
       
        
    def use_item(self, item_ID):
        self.character.items[item_ID].uses -= 1
        if self.character.items[item_ID].uses == 0:
            self.character.remove_item(item_ID)
            self.character.set_item_IDs()
            
    def buy_item(self, item):
        if self.character.cash >= item.value:    
            self.character.add_item(item)
            self.character.cash -= item.value
            self.character.set_item_IDs()
            self.character_cash.set(self.character.cash)
            
        else:
            print("Not enough cash!")
def habit():
    messagebox.showinfo("Placeholder", "I go to Habits work space!")

def task():
    messagebox.showinfo("Placeholder", "I go to Task work space!")

def dailies():
    messagebox.showinfo("Placeholder", "I got to goals work space!")
def buy():
    messagebox.showinfo("Placeholder", "I go to shop!")

def no_where():
    messagebox.showinfo("Placeholder", "I don't have anywher to go yet :( !")

def main():
    """
      Stub for main function
    """
    main_character = load('Tester')
   
    #Display current character's info
    main_character.show_info()
    root = Tk()
    app = GUI(root, main_character)
    root.mainloop()

        
if __name__ == "__main__":
    main()
