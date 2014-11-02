'''
  Habit game core

  Dependencies: landing_page.py
                file_parser.py
'''

#import landing_page.py
import os.path
from file_parser import *
from tkinter  import *
from tkinter.ttk import *
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders

from hack_classes import *
from landing_page import *
from generic_list import *
from work_space import *
import authenticate
from tkinter import filedialog # open/save file


class Game_Data:
    """
    Class for main game functions
    """
    def __init__(self):
        self.savefile = 'character.xml'
        self.character_data = {}
        self.token = ''
        
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
        try:
            file_parser.update_file(self.character_data)
            
        except:
            self.error
        
    def load_data(self):
        """
        Loads character_data from file with
        XML parser. Stores results into
        character_data dict
        """
        try:
            data = file_parser(self.savefile)
            self.character_data['hacks'] = data.parse_hacks()
            self.character_data['name'] = data.parse_name()
            self.token = data.parse_token()
            self.character_data['level'] = data.parse_level()
            self.character_data['exp'] = data.parse_exp()
            self.character_data['cash'] = data.parse_cash()
            
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
            
            for hack in character_data['hacks']:
                new_hack = Habit(hack['title'],
                                  hack['description'],
                                  None,#value
                                  None,#exp
                                  None,#hack_type
                                  hack['index'])
            
                new_character.add_hack(new_hack)
            '''
            for item in character_data['items']:
                new_item = Item(item['name'],
                                item['image'],
                                item['value'],
                                item['uses'],
                                item['effect'])
            
                new_character.add_item(new_item)
            '''
            #Resynchronize hack index
            new_character.hack_index = max(new_character.hacks.keys())

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
    
    hack_1 = Hack('habit', 'Read More','Read more books', 50, 10)  
    hack_2 = Hack('habit', 'Veggies', 'Eat more veggies', 100, 15)
    hack_3 = Hack('habit', 'Sleep more', 'Get more sleep', 20, 5)

    hack_4 = Hack('task', 'Make dinner', 'and make it delicious', 10, 10)

    hack_5 = Hack('daily', 'Play guitar', 'hit strings in a pleasing combination', 15, 25)

    item_1 = Item('Laptop', 'laptop.jpg', 5, 1)
    item_2 = Item('CAT-5 Cable', 'cat5.jpg', 4, 15)
    item_3 = Item('SSD', 'ssd.jpg', 6, 20)

    hacks = []
    items = []

    hacks.append(hack_1)
    hacks.append(hack_2)
    hacks.append(hack_3)
    hacks.append(hack_4)
    hacks.append(hack_5)

    items.append(item_1)
    items.append(item_2)
    items.append(item_3)

    for hack in hacks:
        new_character.add_hack(hack)

    for item in items:
        new_character.add_item(item)

    return new_character


class GUI (Frame):

    def __init__(self, master, character):
        Frame.__init__(self, master)
        
        pad = 100
        
        self.character = character
        self.character_name = StringVar()
        self.character_exp = StringVar()
        self.character_cash = StringVar()
        self.character_level = StringVar()
        self.character_name.set(self.character.name)
        self.character_exp.set(self.character.exp)
        #self.character_cash.set(self.character.cash)
        self.character_level.set(self.character.level)
        self._geom='800x600+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        self.master = master
        self.initUI()

        # link the shop so it can call GUI's buy_item()
        MyShop.setApp(self)

    def initUI(self):
        self.grid()
        self.current_visible_frame = None
        self.master.title("Daily Hack")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(5, weight=1)
        #self.columnconfigure(0, weight = 1)
        self.columnconfigure(6, pad=7)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(9, pad=7)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(4, pad=7)


        # create menu bar with file, edit, and help drop down tabs
        # temp_menu_func is the default command for all the menu options
        menu = Menu(self)

        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="New game", command=self.temp_menu_func)
        file_menu.add_command(label="Load game", command=self.temp_menu_func)
        file_menu.add_command(label="Save game", command=self.save_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.destroy)
        menu.add_cascade(label="FILE", menu=file_menu)

        edit_menu = Menu(menu, tearoff=0)
        edit_menu.add_command(label="Habits", command=self.temp_menu_func)
        edit_menu.add_command(label="Dailies", command=self.temp_menu_func)
        edit_menu.add_command(label="Tasks", command=self.temp_menu_func)
        menu.add_cascade(label="EDIT", menu=edit_menu)

        options_menu = Menu(menu, tearoff=0)
        options_menu.add_command(label="Game", command=self.no_where)
        options_menu.add_command(label="Settings", command=self.no_where)
        menu.add_cascade(label="OPTIONS", menu=options_menu)
         
        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="How to play", command=self.temp_menu_func)
        help_menu.add_command(label="About", command=self.temp_menu_func)
        menu.add_cascade(label="HELP", menu=help_menu)

        self.master.config(menu=menu)


        # create banner
        self.banner = Frame(self, style='banner.TFrame', padding=0)
        self.banner.grid(row=0, column=0, columnspan=9, sticky='news')
        self.style.configure('banner.TFrame', background='black')

        logo_img = PhotoImage(file=os.path.join("assets", "art", "logo.gif"))
        logo_image = Label(self.banner, image=logo_img, style='hack_logo.TLabel', padding='7 7 7 6', cursor="hand2")
        logo_image.grid(row=0, column=0, sticky='e', padx=(0,30))
        logo_image.image = logo_img
        logo_image.bind('<Enter>', lambda e: logo_image.configure(background='#0F0F0F'))
        logo_image.bind('<Leave>', lambda e: logo_image.configure(background='black')) 
        logo_image.bind('<1>', lambda e: self.home()) 
        self.style.configure('hack_logo.TLabel', background='black')

        # make common 'menu bar' links
        def make_menu(col_number, name, function):
            menu_title = Label(self.banner, padding='12 7 12 7', cursor='hand2', text=name)
            menu_title.configure(background='black', foreground='#EBEBEB', font='arial 12 bold')
            menu_title.bind('<Enter>', lambda e: menu_title.configure(background='#0F0F0F', foreground='#FFD237'))
            menu_title.bind('<Leave>', lambda e: menu_title.configure(background='black', foreground='#EBEBEB'))
            menu_title.bind('<1>', lambda e: function()) 
            menu_title.grid(row=0, column=col_number+1, sticky='e')

        menu_titles = ['Home', 'Habits', 'Tasks', 'Dailies', 'List', 'Shop']
        menu_functions = [self.home, self.habit, self.task, self.dailies, self.generic, self.buy]
        for i in range(6):
            make_menu(i, menu_titles[i], menu_functions[i])
            
      
        # create character data frame
        self.char_frame = Frame(self)
        self.char_frame.grid(row=2, column=0, sticky='news')
        
        name_lalel = Label(self.char_frame, text="Player Name")
        name_lalel.grid(row = 0, column = 0,sticky=W, pady=4, padx=5)
        name_lalel.configure(font='arial 12')
        
        name = Label(self.char_frame, textvariable = self.character_name)
        name.grid(row = 0, column = 1, sticky=W, pady=4, padx=5)
        name.configure(font='arial 12 bold')
        
        # load character image
        char_img = PhotoImage(file=os.path.join("assets", "art", "main.gif"))
        character_image = Label(self.char_frame, image=char_img)
        character_image.grid(row=1, column=0, stick=W, padx=5)
        character_image.image = char_img


        # create stats frame; embedded in the character frame
        statsBg = Frame(self, style="statsFrame.TFrame")
        statsBg.grid(row=1, column=0, columnspan=9, sticky='we')
        statsBg.columnconfigure(0, weight=1)
        
        self.stats_frame = Frame(statsBg, style="statsFrame.TFrame")
        self.stats_frame.grid(row=0, column=0)

        # add experience stats info
        exp_label = Label(self.stats_frame, text="exp:", style="statsLabel.TLabel")
        exp_label.grid(row=0, column=0, sticky='nesw', pady=4, padx=5)
        
        exp = Label(self.stats_frame, textvariable = self.character_exp)
        exp.grid(row = 0, column=1, sticky='nesw', pady=4, padx=5)
        exp.configure(background="#283D57", font="arial 12 bold", foreground='#C5BD25')

        # add cash stats info
        self.character_cash.set(self.character.cash)
        cash_label = Label(self.stats_frame, text="cash:", style="statsLabel.TLabel")
        cash_label.grid(row = 0, column =2 ,sticky='nesw', pady=4, padx=5)
        cash = Label(self.stats_frame, textvariable= self.character_cash)
        cash.grid(row = 0, column =3, sticky='nesw', pady=4, padx=5)
        cash.configure(background="#283D57", font="arial 12 bold", foreground='#3BB623')
        
        # add level stats info
        level_label = Label(self.stats_frame, text="level:", style="statsLabel.TLabel")
        level_label.grid(row = 0, column =4 ,sticky='nesw', pady=4, padx=5)

        level = Label(self.stats_frame, textvariable = self.character_level)
        level.grid(row = 0, column =5 ,sticky='nesw', pady=4, padx=5)
        level.configure(background="#283D57", font="arial 12 bold", foreground='#FF7F2A')
        
        self.style.configure("statsLabel.TLabel", background="#283D57", font="arial 12 bold", foreground='white')
        self.style.configure("statsFrame.TFrame", background="#283D57")
        

        mb=  Menubutton(self, text="Options")
        mb.grid(row = 0, column = 6, sticky = E)
        mb.menu  =  Menu ( mb, tearoff = 0 )
        mb["menu"]  =  mb.menu
    
        mayoVar  = IntVar()
        ketchVar = IntVar()
        mb.menu.add_command( label="Home", command = self.home)
        mb.menu.add_command( label="Habits", command = self.habit)
        mb.menu.add_command( label="Dailies", command = self.dailies )
        mb.menu.add_command( label="Tasks", command = self.task )
        mb.menu.add_command( label="Shop", command = self.buy )
        mb.menu.add_command( label="Game", command = self.no_where)
        mb.menu.add_command( label = "List", command = self.generic)
        mb.menu.add_command( label = "Save Game", command = self.save_game)
        mb.menu.add_command( label="Settings", command = self.no_where)

        # footer
        footer_frame_bg = Frame(self, style='footer.TFrame', padding=3)
        footer_frame_bg.grid(row=10, column=0, columnspan=7, sticky= (W, E))
        footer_frame_bg.columnconfigure(0, weight=1)

        # centered frame; holds logo and copyright text
        footer_frame = Frame(footer_frame_bg, style='footer.TFrame')
        footer_frame.grid()
        
        self.style.configure('footer.TFrame', background='black')

        # archetype logo 
        archetype_img = PhotoImage(file=os.path.join("assets", "art", "Archetype.gif"))
        archetype_logo = Label(footer_frame, image=archetype_img, padding="0 0 5 0")
        archetype_logo.grid(row=0, column=0, sticky=(N, E, W, S))
        archetype_logo.image = archetype_img
        archetype_logo.configure(background = 'black', foreground = 'white', anchor = CENTER)
        
        footer = Label(footer_frame, text="Copyright 2014")
        footer.grid(row=0, column=1, sticky = (N, E, W, S))
        footer.configure(background = 'black', foreground = 'white', anchor = CENTER, font='arial 12')

 
        self.frames = {}
        
        # Add main frames to grid for geometry memory
        # then remove them

        work_space_frame = Work_Space(self, self.character)
        generic_frame = Generic(self, self.character)
        landing_page_frame = Landing_Page(self, self.character)

        self.frames[Work_Space] = work_space_frame
        self.frames[Generic] = generic_frame
        self.frames[Landing_Page] = landing_page_frame
        
        self.show_frame(Landing_Page)

    """ This is the default for all menu bar options, except for exit """
    def temp_menu_func(self):
        print("test menu")
            
    def show_frame(self, c):
        '''
        Show a frame for the given class
        '''
        
        if c in ('habit', 'daily', 'task', 'shop'):
            if self.current_visible_frame != self.frames[Work_Space]: 
                self.current_visible_frame.grid_remove()
                
            frame = self.frames[Work_Space]
            frame.grid(row = 4, column = 0, columnspan = 7,
                       rowspan = 4, sticky = 'news')

            #Adjust notebook to desired tab
            frame.select_tab(c)
            self.current_visible_frame = frame
            
            
        else:
            if self.current_visible_frame != self.frames[c]:
                if self.current_visible_frame != None:
                    self.current_visible_frame.grid_remove()

                frame = self.frames[c]
                frame.grid(row = 4, column = 0, columnspan = 7,
                           rowspan = 4, sticky = 'news')
                self.current_visible_frame = frame
            
        
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
        
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
            print(item.name + " bought!")
        else:
           print("Not enough cash for " + item.name + "!")

        
    def home(self):
        #Currently this goes no where, need to fix the grid_forget issue first
        self.show_frame(Landing_Page)

    def habit(self):
        self.show_frame('habit')

    def task(self):
        self.show_frame('task')
        main.__subclasshook__

    def dailies(self):
        self.show_frame('daily')
        
    def buy(self):
        self.show_frame('shop')
        
    def save_game(self):
        saved_path = filedialog.asksaveasfilename()
        if saved_path != '':
            messagebox.showinfo("Save", "game save at: " + saved_path)  
    
    def generic(self):
        self.show_frame(Generic)

    def no_where(self):
        messagebox.showinfo("Placeholder", "I don't have anywhere to go yet :( !")


def main():
    """
      Stub for main function
    """
    db = authenticate.db()

    main_character = load('Tester')
   
    #Display current character's info
    root = Tk()
    app = GUI(root, main_character)
    
    root.mainloop()

        
if __name__ == "__main__":
    main()
