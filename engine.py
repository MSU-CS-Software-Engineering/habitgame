#!/usr/bin/python3

'''
  Habit game core

  Dependencies: landing_page.py
                file_parser.py
'''

#import landing_page.py
import os.path
from file_parser import *

from tkinter  import *
from tkinter import Frame as Frame
from tkinter.ttk import *
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders

from hack_classes import *
from updater import *
from boss import *
from landing_page import *
from generic_list import *
from work_space import *
import authenticate
from tkinter import filedialog # open/save file
from time import sleep, time
import threading
import queue
from tooltip import *

#current_date = date.today()

class Game_Data:
    """
    Class for main game functions
    """
    def __init__(self, parent):
        self.parent = parent
        self.savefile = 'character.xml'
        self.character_data = {}
        self.character_data['firstname'] = ''
        self.character_data['lastname'] = ''
        self.character_data['birthday'] = ''
        self.token = ''
        self.version = 1.1
        self.lastran = ''
        self.parser = file_parser(self.savefile)

    def show_character_data(self):
        print(self.character_data)

    def save_data(self, character, boss, lastran):
        """
        Saves the current character data to
        Game_Data's character_data
        """
        self.character_data = character.serialize()
        self.character_data['firstname'] = self.firstname
        self.character_data['lastname'] = self.lastname
        self.character_data['birthday'] = self.birthday
        self.character_data['token'] = self.token
        self.character_data['boss'] = boss.serialize()
        self.character_data['version'] = self.version
        self.character_data['lastran'] = str(lastran)
        print("Character data saved")

    def save_to_file(self):
        """
        Saves character_data to file
        """
        try:
            self.parser.update_file(self.character_data, self.savefile)

        except:
            self.error('Failed to write to file')

    def load_data(self):
        """
        Loads character_data from file with
        XML parser. Stores results into
        character_data dict
        """
        try:
            self.character_data['hacks'] = self.parser.parse_hacks()
            self.firstname = self.parser.parse_firstname()
            self.lastname = self.parser.parse_lastname()
            self.character_data['name'] = self.parser.parse_name()
            self.birthday = self.parser.parse_birthday()
            self.token = self.parser.parse_token()
            self.version = self.parser.parse_version()

            #1.1 is the first version available. If this project were
            #to continue we would have self.version pull from a text
            #file that was created during the original build or
            #subsequent updates. For now we are hardcoding the first version.
            self.version =1.1
            #self.parser.parse_version()

            self.character_data['level'] = self.parser.parse_level()
            self.character_data['exp'] = self.parser.parse_exp()
            self.character_data['cash'] = self.parser.parse_cash()
            self.character_data['items'] = self.parser.parse_items()

            lastran = self.parser.parse_lastran()
            
            if lastran == 0:
                self.lastran = ''

            else:
                self.lastran = lastran

            
            boss_data = self.parser.parse_boss()

            if boss_data == 0:
                self.character_data['boss'] = ''

            else:
                self.character_data['boss'] = boss_data

        except:
            self.error('Failed to load data')


    def build_character(self):
        """
        Builds a character object from the Game_Data's
        character_data.
        """
        #try:
        character_data = self.character_data
        new_character = Character(character_data['name'], self.parent)
        new_character.level = character_data['level']
        new_character.exp = character_data['exp']
        new_character.cash = character_data['cash']

        if new_character.level < 1:
            new_character.level = 1


        for hack in character_data['hacks']:
            new_hack = Hack(hack['h_type'],
                            hack['title'],
                            hack['desc'],
                            hack['value'],
                            self.parent.current_date,
                            hack['exp'])

            new_character.add_hack(new_hack)

        for item in character_data['items']:
            new_item = Item(item['title'],
                            item['desc'],
                            item['image'],
                            item['value'],
                            item['uses'],
                            item['item_type'],
                            item['active'],
                            float(item['effect']),
                            float(item['duration']),
                            item['component'])

            new_character.add_item(new_item)

        #Resynchronize hack index
        if len(new_character.hacks.keys()) > 0:
            new_character.hack_index = max(new_character.hacks.keys())

        return new_character

        #except:
        #    self.error("Failed to build character from" \
        #               " default character data")

    def build_boss(self, parent):
        '''
        Returns a boss character from a base64 encoded string
        '''

        if len(self.character_data['boss']) > 0:
            boss_dict = eval(base64.b64decode(bytes(self.character_data['boss'], 'utf-8')).decode())
            options = {'health':boss_dict['health'],
                       'new':boss_dict['new'],
                       'distance_from_character':boss_dict['distance'],
                       'active':boss_dict['active']}

            new_boss = Boss(parent,
                            boss_dict['level'],
                            options)

            return new_boss

        else:
            '''Default boss configuration'''
            return Boss(parent, 1)


    def error(self, error_message):
        print("ERROR:", error_message)



def load_hacks():
    '''
    Loads hacks for character
    Used for debugging
    '''
    hack_1 = Hack('habit', 'Read More','Read more books', 50, 10)
    hack_2 = Hack('habit', 'Veggies', 'Eat more veggies', 100, 15)
    hack_3 = Hack('habit', 'Sleep more', 'Get more sleep', 20, 5)

    hack_4 = Hack('task', 'Make dinner', 'and make it delicious', 10, 10)

    hack_5 = Hack('daily', 'Play guitar', 'hit strings in a pleasing combination', 15, 25)

    hacks = []
    hacks.append(hack_1)
    hacks.append(hack_2)
    hacks.append(hack_3)
    hacks.append(hack_4)
    hacks.append(hack_5)

    return hacks

def load_items():
    '''
    Loads items for character
    Used for debugging
    '''
    item_1 = Item('Laptop', 'laptop.jpg', 5, 1)
    item_2 = Item('CAT-5 Cable', 'cat5.jpg', 4, 15)
    item_3 = Item('SSD', 'ssd.jpg', 6, 20)

    items = []
    items.append(item_1)
    items.append(item_2)
    items.append(item_3)

    return items


class Notification(threading.Thread):
    
    def __init__(self, notify_queue, master):
        threading.Thread.__init__(self)
        self.setDaemon(True) 
        self.notify_queue = notify_queue
        self.master = master
        self.notification = self.master.notification_message
        
    def run(self):

        while True:
            try:
                #in python, .get() blocks until an item is available in the queue.
                #Not a problem; since this thread's only purpose is to handle
                #notifications it can sit there forever for all we care
                notification = self.notification
                msg = self.notify_queue.get()
                notification.configure(text=msg)
                #notification_frame = Frame(self.master, style='footer.TFrame')
                #notification_frame.config(height=50, width=300)
                #notification_frame.place(relx=0.9967, y=230, anchor="se")
                
                #notification = Message(notification_frame, text=msg, width=200)
                #notification.grid(row=0, column=1, sticky = E)
                #notification.configure(background='#d9d9d9', foreground = '#d9d9d9', anchor = E, font='arial 16')
                
                #fade in. since frames don't support alpha, it simulates real alpha
                #by simply changing the background color from the original to black
                notification.configure(foreground='#191919')
                sleep(0.05)
                notification.configure(foreground='#292929')
                sleep(0.05)
                notification.configure(foreground='#393939')
                sleep(0.05)
                notification.configure(foreground='#494949')
                sleep(0.05)
                notification.configure(foreground='#595959')
                sleep(0.05)
                notification.configure(foreground='#696969')
                sleep(0.05)
                notification.configure(foreground='#797979')
                sleep(0.05)
                notification.configure(foreground='#898989')
                sleep(0.05)
                notification.configure(foreground='#999999')
                sleep(0.05)
                notification.configure(foreground='#a9a9a9')
                sleep(0.05)
                notification.configure(foreground='#b9b9b9')
                sleep(0.05)
                notification.configure(foreground='#c9c9c9')
                sleep(0.05)
                notification.configure(foreground='#d9d9d9')

                #wait a few seconds at full alpha
                sleep(1)
                
                #longer messages delay a little bit longer to allow the user to read it
                if len(msg) > 15:
                    sleep(0.5)
                if len(msg) > 30:
                    sleep(1.5)
                if len(msg) > 35:
                    sleep(1)

                #fade out
                sleep(0.05)
                notification.configure(foreground='#c9c9c9')
                sleep(0.05)
                notification.configure(foreground='#b9b9b9')
                sleep(0.05)
                notification.configure(foreground='#a9a9a9')
                sleep(0.05)
                notification.configure(foreground='#999999')
                sleep(0.05)
                notification.configure(foreground='#898989')
                sleep(0.05)
                notification.configure(foreground='#797979')
                sleep(0.05)
                notification.configure(foreground='#696969')
                sleep(0.05)
                notification.configure(foreground='#595959')
                sleep(0.05)
                notification.configure(foreground='#494949')
                sleep(0.05)
                notification.configure(foreground='#393939')
                sleep(0.05)
                notification.configure(foreground='#292929')
                sleep(0.05)
                notification.configure(foreground='#191919')

                notification.configure(text='')
            except:
                pass
            #delay just a smidgeon between messages.
            sleep(0.3)
            
            
            
# Placed here to resolve import loop issues with work_space, engine, and
# shop.
from work_space import *

class GUI(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        pad = 100
        self.current_date = date.today()
        
        self.game_data = Game_Data(self)
        self.game_data.load_data()
        
        
        #This variable holds a constant record
        #of the actual system date, so not to
        #corrupt the lastran in character.xml
        self.const_current_date = self.current_date

        #Check for software updater
        self.updater = Updater(self.game_data.version,
                               master)
        
        self.updater.check_update()

        #bring back root window
        master.deiconify()

        self.character = self.game_data.build_character()

        self.boss = self.game_data.build_boss(self)

        self.character_name = StringVar()
        self.character_exp = StringVar()
        self.character_to_next_level = StringVar()
        self.character_cash = StringVar()
        self.character_level = StringVar()
        self.character_rank = StringVar()
        self.character_item_count = StringVar()
        self.update_item_count()

        self.boss_name = StringVar()
        self.boss_health = StringVar()
        self.boss_distance = StringVar()
        self.boss_distance_progress = IntVar()
        
        self.update_name()
        self.update_exp()
        self.update_to_next_level()
        self.update_cash()
        self.update_level()
        self.update_rank()

        self._geom='800x600+0+0'
        #master.geometry('{0}x{1}+0+0'.format(
        #    master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))

        master.geometry('{0}x{1}+0+0'.format(
            master.winfo_screenwidth()-850, master.winfo_screenheight()-350))
        master.bind('<Escape>',self.toggle_geom)
        self.master = master
        GUI.notification_queue = queue.Queue()
        
        self.initUI()
        self.bind_buttons()

        # link the shop so it can call GUI's buy_item()
        MyShop.setApi(self)
        MyInventory.setApi(self, self.items_frame)

        self.check_boss()

    def inst_notify(self, type, message):
        GUI.notify(type, message)

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

        self.make_menu_bar()
        self.make_character_frame()
        self.make_items_in_use_frame()
        self.make_boss_frame()
        self.make_banner()
        self.make_stats_banner()
        self.make_notification_area()
        self.make_footer()

        self.update_distance_bar()
        
        self.frames = {}

        work_space_frame = Work_Space(self, self.character)
        generic_frame = Generic(self, self.character)
        landing_page_frame = Landing_Page(self, self.character)

        self.frames['Work_Space'] = work_space_frame
        self.frames['Generic'] = generic_frame
        self.frames['Landing_Page'] = landing_page_frame
        self.show_frame('Landing_Page')

        #create the notification handler. this is threaded so the whole program
        #doesn't hang when we make the frame wait.
        Notification(GUI.notification_queue, self).start()
        GUI.notify('put_type_here', 'Welcome to your Daily <Hack>!')

        self.check_dailies_init()

    def configure_distance_bar_color(self):
        #Configure color based on distance
        #Green:100-67 Yellow:66-33 Red:32-0
        style = Style()
        style.theme_use('clam')
        style.configure("red.Horizontal.TProgressbar",
                        foreground='red',
                        background='red')
        
        style.configure("yellow.Horizontal.TProgressbar",
                        foreground='yellow',
                        background='yellow')
        
        style.configure("green.Horizontal.TProgressbar",
                        foreground='green',
                        background='green')


        distance = self.boss.get_distance()

        current_style = ''
        
        if distance > 66:
            current_style = 'green.Horizontal.TProgressbar'

        elif distance > 32:
            current_style = 'yellow.Horizontal.TProgressbar'

        else:
            current_style = 'red.Horizontal.TProgressbar'
            
        self.boss_distance_bar.configure(style=current_style)


    def update_distance_bar(self, debug=0):
        if debug > 0:
            current_val = self.boss_distance_progress.get()
            self.boss_distance_progress.set(current_val - debug)
            
        else:
            value = self.boss.get_distance()
            self.boss_distance_progress.set(value)

        try:
            self.configure_distance_bar_color()
        except:
            pass
        
    def make_notification_area(self):
        notification_style = Style()
        notification_style.configure('notif.TFrame')
        self.notification_area = Frame(self, style='notif.TFrame')
        self.notification_area.columnconfigure(1, weight=1)

        #Boss Distance Area
        boss_distance_bar_label = Label(self.notification_area,
                                        text = "Boss Distance",
                                        padding = 2,
                                        foreground = "black",
                                        font='arial 12 bold')
        boss_distance_bar_label.grid(row=0, column=0, sticky='ew')
        self.boss_distance_bar = Progressbar(self.notification_area,
                                             variable = self.boss_distance_progress,
                                             maximum = 100)

        
        self.boss_distance_bar.grid(row=0, column=1, sticky='ew')
        self.configure_distance_bar_color()
        
        #Feedback Area
        feedback_label = Label(self.notification_area,
                                        text = "Feedback",
                                        padding = 2,
                                        foreground = "black",
                                        font='arial 12 bold')
        feedback_label.grid(row=1, column=0, sticky='ew')
        
        self.notification_message = Message(self.notification_area,
                                            text="", width=1200)
        
        self.notification_message.configure(background='#000000', foreground = '#ffffff', anchor = W, font='arial 12')
        
        self.notification_message.grid(row=1, column=1, sticky='ew')
        self.notification_area.grid(row=3, column=0, columnspan=5, sticky='ew')


    def make_menu_bar(self):
        """
        create menu bar with file, edit, and help drop down tabs
        temp_menu_func is the default command for all the menu options
        """
        self.menu = Menu(self)

        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Save game", command=self.save_game)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.destroy)
        self.menu.add_cascade(label="FILE", menu=self.file_menu)

        self.edit_menu = Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label="Habits", command=self.go_to_habits)
        self.edit_menu.add_command(label="Tasks", command=self.go_to_tasks)
        self.edit_menu.add_command(label="Dailies", command=self.go_to_dailies)
        self.menu.add_cascade(label="EDIT", menu=self.edit_menu)

        self.options_menu = Menu(self.menu, tearoff=0)
        self.options_menu.add_command(label="Enable Debug Mode", command=self.enable_debug)
        self.options_menu.add_command(label="Advance to Next Day", command=self.advance_to_next_day)
        self.options_menu.add_command(label="Set player stats", command=self.set_player_stats)
        self.menu.add_cascade(label="DEBUG", menu=self.options_menu)
        self.options_menu.entryconfig(1, state="disabled")
        self.options_menu.entryconfig(2, state="disabled")

        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="How to play", command=self.temp_menu_func)
        self.help_menu.add_command(label="About", command=self.spawn_about_window)
        #Used for distance bar debugging
        #self.help_menu.add_command(label="Distance test", command=self.distance_test)
        self.menu.add_cascade(label="HELP", menu=self.help_menu)

        self.master.config(menu=self.menu)

    def distance_test(self):
        #Increas boss distance
        self.boss.approach_character(5)
        self.update_boss_data()
        
        #self.update_distance_bar(5)
        
    def enable_debug(self):
        self.options_menu.entryconfig(0, state="disabled")
        self.options_menu.entryconfig(1, state="normal")
        self.options_menu.entryconfig(2, state="normal")
        self.update_boss_data()

    def remove_cash(self, amount):
        self.character.cash -= amount

        #Set lower limit for character cash
        if self.character.cash < 0:
            self.character.cash = 0

        
            
    def check_dailies_init(self):
        if len(self.game_data.lastran) > 0:
            lastran_date = datetime.strptime(self.game_data.lastran,
                                             "%Y-%m-%d").date()

            
            days_missed = (self.current_date - lastran_date).days
            if days_missed > 0:
                missed_dailies = 0
                for hack in self.character.hacks.values():
                    if hack.h_type == "daily":
                        missed_dailies += 1

                        self.remove_cash(int(hack.value)*days_missed)
                        self.boss.approach_character(5)
                        self.redraw()
                        self.update_stats_banner()
                        self.update_boss_data()
                        #self.update_distance_bar()
                        self.change_character_emotion(1, "mainMad.gif")

                if missed_dailies:
                    if missed_dailies > 1:
                        plural_string = "s"

                    else:
                        plural_string = ""
                        self.inst_notify("Exclamation",
                                         "You failed to complete " 
                    + str(missed_dailies) + " daily hack" + plural_string + "!")

                note_message_part_1 = 'Make sure to log in every day and '
                note_message_part_2 = 'complete your hacks or you may be robbed!'
                self.inst_notify("Note", note_message_part_1 + \
                                 note_message_part_2)

                             
        
    def check_dailies(self):
        missed_dailies = 0

        for hack in self.character.hacks.values():
            if hack.h_type == "daily" and (hack.timestamp < 
                (self.current_date - timedelta(hours=24))):

                missed_dailies += 1
                
                days_missed = (self.current_date - hack.timestamp).days
                self.remove_cash(int(hack.value)*days_missed)

                #Make sure character cash isn't negative 
                if self.character.cash < 0:
                    self.character.cash = 0
                    
                self.boss.approach_character(5)
                self.redraw()
                self.update_stats_banner()
                self.update_boss_data()
                self.change_character_emotion(1, "mainMad.gif")

        if missed_dailies:
            if missed_dailies > 1:
                plural_string = "s"
            else:
                plural_string = ""
            self.inst_notify("Exclamation", "You failed to complete " 
                + str(missed_dailies) + " daily hack" + plural_string + "!")
            
    def advance_to_next_day(self):
        self.current_date += timedelta(hours=24)
        self.check_dailies()
        

    def set_player_stats(self):
        data_window = Toplevel(self)

        window_bg = Frame(data_window, style='popup_bg.TFrame')
        window_bg.pack()

        #Exp
        exp_frame = Frame(window_bg, style='popup_bg.TFrame')
        exp_frame.pack(side="top")

        self.style.configure('popup_bg.TFrame', background="#D9D9D9")

        exp_label = Label(exp_frame, text="Exp", padding='150 5 150 5',
                           foreground='white', background='#283D57', font='arial 12 bold')
        exp_label.pack(side="top")

        exp_warning_label = Label(exp_frame, text = "Value cannot be empty!", padding = 5,
                                    foreground = "red", font='arial 12 bold', state = DISABLED)
        exp_warning_label.pack(side="top", padx = 10, pady=10)
        exp_warning_label.pack_forget() #Start invisible

        char_exp = Entry(exp_frame, justify=CENTER)
        char_exp.pack(side="bottom", pady=5)

        #Cash
        cash_frame = Frame(window_bg, style='popup_bg.TFrame')
        cash_frame.pack(side="top")

        self.style.configure('popup_bg.TFrame', background="#D9D9D9")

        cash_label = Label(cash_frame, text="Cash", padding='150 5 150 5',
                           foreground='white', background='#283D57', font='arial 12 bold')
        cash_label.pack(side="top")

        cash_warning_label = Label(cash_frame, text = "Value cannot be empty!", padding = 5,
                                    foreground = "red", font='arial 12 bold', state = DISABLED)
        cash_warning_label.pack(side="top", padx = 10, pady=10)
        cash_warning_label.pack_forget() #Start invisible

        char_cash = Entry(cash_frame, justify=CENTER)
        char_cash.pack(side="bottom", pady=5)

        #Level
        level_frame = Frame(window_bg, style='popup_bg.TFrame')
        level_frame.pack(side="top")

        self.style.configure('popup_bg.TFrame', background="#D9D9D9")

        level_label = Label(level_frame, text="Level", padding='150 5 150 5',
                           foreground='white', background='#283D57', font='arial 12 bold')
        level_label.pack(side="top")

        level_warning_label = Label(level_frame, text = "Value must be a positive integer!", padding = 5,
                                    foreground = "red", font='arial 12 bold', state = DISABLED)
        level_warning_label.pack(side="top", padx = 10, pady=10)
        level_warning_label.pack_forget() #Start invisible

        char_level = Entry(level_frame, justify=CENTER)
        char_level.pack(side="bottom", pady=5)

        #Buttons
        button_frame = Frame(window_bg, width=100)
        button_frame.grid_propagate(100)
        button_frame.pack(side="bottom", padx=10, pady=10)

        cancelButton = Button(button_frame, text="Cancel", style = 'cancel.TButton',
                              cursor = 'hand2', command=data_window.destroy)
        cancelButton.pack(side="left")
        self.style.configure('cancel.TButton', font = 'arial 14 bold', relief = 'flat',
                              padding = 5, foreground = 'black', background = '#FF4848')

        char_exp.insert(INSERT, self.character.exp)
        char_cash.insert(INSERT, self.character.cash)
        char_level.insert(INSERT, self.character.level)

        confirmButton = Button(button_frame, text="Save", style = 'save.TButton', cursor = 'hand2',
            command=lambda: self.check_debug_validity( data_window, 
                            char_exp.get(), char_cash.get(), char_level.get(),
                            exp_warning_label, cash_warning_label, level_warning_label))

        confirmButton.pack(side="right")

        self.style.configure('save.TButton', font = 'arial 14 bold', relief = 'flat',
                             padding = 5, foreground = 'black', background = '#96FF48')

    def check_debug_validity(self, window, exp, cash, level, exp_label, cash_label, level_label):
        error_triggered = False

        try:
            int(exp)
            exp_label.pack_forget()

        except:
            exp_label.pack()
            error_triggered = True

        try:
            int(cash)
            cash_label.pack_forget()

        except:
            cash_label.pack()
            error_triggered = True

        try:
            int(level)
            level_label.pack_forget()

        except:
            level_label.pack()
            error_triggered = True

        if error_triggered:
            return

        else:
            self.character.exp = int(exp)
            self.character.cash = int(cash)
            self.character.level = int(level)
            self.redraw()
            self.update_stats_banner()
            window.destroy()

    def make_banner(self):
        """
        create banner, includes the Daily Hack logo and common links to
        habits, tasks, dailies, etc.
        """

        self.banner = Frame(self, style='banner.TFrame', padding=0)
        self.banner.grid(row=0, column=0, columnspan=9, sticky='news')
        self.style.configure('banner.TFrame', background='black')

        # Daily Hack logo linked to the homepage
        logo_img = PhotoImage(file=os.path.join("assets", "art", "logo.gif"))
        logo_image = Label(self.banner, image=logo_img, style='hack_logo.TLabel', padding='7 7 7 6', cursor="hand2")
        logo_image.grid(row=0, column=0, sticky='e', padx=(0,30))
        logo_image.image = logo_img
        logo_image.bind('<Enter>', lambda e: logo_image.configure(background='#0F0F0F'))
        logo_image.bind('<Leave>', lambda e: logo_image.configure(background='black'))
        logo_image.bind('<1>', lambda e: self.go_to_home())
        self.style.configure('hack_logo.TLabel', background='black')

        self.menu_titles = ['Home', 'Habits', 'Tasks', 'Dailies', 'Shop', 'Inventory']
        self.menu_functions = [self.go_to_home, self.go_to_habits, self.go_to_tasks,
                               self.go_to_dailies, self.go_to_shop, 
                               self.go_to_inventory]

        self.menu_link_buttons = []

        for i in range(len(self.menu_titles)):
            self.make_menu(i, self.menu_titles[i], self.menu_functions[i])

    def clear_menus(self, not_clear):
        """
        this function is called for link buttons outside of the menu banner, so the proper buttons get reset.
        ie: when the user clicks on the daily hack logo, the home button becomes selected and highlighted

        not_clear acceptable values:
        'Home' = 0, 'Habits' = 1, 'Tasks' = 2, 'Dailies' = 3, 'List' = 4, 'Shop' = 5, 'Inventory' = 6
        """
        self.button_selected = True
        self.select_id = not_clear

        self.menu_link_buttons[not_clear].configure(background='#283D57', foreground='#79DB44')
        for i in range(len(self.menu_link_buttons)):
                if i != not_clear:
                    self.menu_link_buttons[i].configure(background='black', foreground='#EBEBEB')

    def make_menu(self, col_number, menu_title, go_to_page):
        """
        Make's common menu links. When the mouse hovers over the link, the foreground/background changes color.
        When a link is clicked on, the foreground/background color stays the same as the hover over color and
        it does not change until a new link is selected. Note: other links can still be hovered over and they will
        highlight independently regardless of which link is currently selected.
        """
        self.button_selected = False
        self.select_id = -1

        def mouse_leave():
            if not self.button_selected or col_number != self.select_id:
                menu_link.configure(background='black', foreground='#EBEBEB')

        def mouse_enter():
            if self.select_id != col_number:
                menu_link.configure(background='#0F0F0F', foreground='#FFD237')

        def go_to():
            self.button_selected = True
            self.select_id = col_number
            for i in range(len(self.menu_link_buttons)):
                if i != col_number:
                    self.menu_link_buttons[i].configure(background='black', foreground='#EBEBEB')

            menu_link.configure(background='#283D57', foreground='#79DB44')
            go_to_page()

        if 'Inventory' != menu_title:
            menu_link = Label(self.banner, padding='12 7 12 7', cursor='hand2', text=menu_title)
            menu_link.grid(row=0, column=col_number+1, sticky='e')
        elif 'Inventory' == menu_title:
            menu_link = Label(self.char_buttons_frame, padding='12 7 12 7', cursor='hand2',
                         textvariable=self.character_item_count)
            menu_link.grid(row=1, column=1, padx=5, sticky='e')

        menu_link.configure(background='black', foreground='#EBEBEB', font='arial 12 bold')

        menu_link.bind('<Enter>', lambda e: mouse_enter())
        menu_link.bind('<Leave>', lambda e: mouse_leave())
        menu_link.bind('<1>', lambda e: go_to())
            
        self.menu_link_buttons.append(menu_link)

    def make_stats_banner(self):
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

        exp_max_label = Label(self.stats_frame, text="/", style="statsLabel.TLabel")
        exp_max_label.grid(row=0, column=2, sticky='nesw', pady=4, padx=5)
        
        exp_max = Label(self.stats_frame, textvariable = self.character_to_next_level)
        exp_max.grid(row = 0, column=3, sticky='nesw', pady=4, padx=5)
        exp_max.configure(background="#283D57", font="arial 12 bold", foreground='#C5BD25')
        
        # add cash stats info
        cash_label = Label(self.stats_frame, text="cash:", style="statsLabel.TLabel")
        cash_label.grid(row = 0, column =4 ,sticky='nesw', pady=4, padx=5)
        cash = Label(self.stats_frame, textvariable=self.character_cash)
        cash.grid(row = 0, column =5, sticky='nesw', pady=4, padx=5)
        cash.configure(background="#283D57", font="arial 12 bold", foreground='#3BB623')

        # add level stats info
        level_label = Label(self.stats_frame, text="level:", style="statsLabel.TLabel")
        level_label.grid(row = 0, column =6 ,sticky='nesw', pady=4, padx=5)

        level = Label(self.stats_frame, textvariable = self.character_level)
        level.grid(row = 0, column =7 ,sticky='nesw', pady=4, padx=5)
        level.configure(background="#283D57", font="arial 12 bold", foreground='#FF7F2A')
        
        # add rank stats info
        rank_label = Label(self.stats_frame, text="class:", style="statsLabel.TLabel")
        rank_label.grid(row = 0, column=8, sticky='nesw', pady=4, padx=5)
        
        rank = Label(self.stats_frame, textvariable = self.character_rank)
        rank.grid(row = 0, column=9, sticky='nesw', pady=4, padx=5)
        rank.configure(background="#283D57", font="arial 12 bold", foreground='#5BADD9')

        self.style.configure("statsLabel.TLabel", background="#283D57", font="arial 12 bold", foreground='white')
        self.style.configure("statsFrame.TFrame", background="#283D57")

    def make_boss_frame(self):
        # create boss data frame
        self.boss_frame_bg = Frame(self, padding = '40 0 0 0')
        self.boss_frame_bg.grid(row = 2, column = 2, sticky = 'news')
        
        boss_name = Label(self.boss_frame_bg, textvariable = self.boss_name)
        boss_name.grid(row = 0, column = 0, sticky = W, pady = 4, padx = 5)
        boss_name.configure(font = 'arial 14 bold')

        self.boss_frame = Frame(self.boss_frame_bg)
        self.boss_frame.grid(row = 1, column = 0, sticky = 'news')
        
        # load boss image
        self.boss_file = PhotoImage(file = self.boss.get_boss_img())
        self.boss_image = Label(self.boss_frame, image = self.boss_file, cursor = 'hand2')
        self.boss_image.grid(row = 0, column = 0, stick = W, padx = 5)
        self.boss_image.image = self.boss_file
        
        self.boss_tip = ToolTip(self.boss_image, self.boss.display_message(), self.update_boss_msg, '#CD3D3D')

        # create boss data frame for defenses and distance variables
        boss_stats_frame = Frame(self.boss_frame)
        boss_stats_frame.grid(row = 0, column = 1, sticky = 'news')
        
        boss_health = Label(boss_stats_frame, textvariable = self.boss_health)
        boss_health.grid(row = 0, column = 0, sticky = W)
        boss_health.configure(font = 'arial 12 bold')

        boss_distance = Label(boss_stats_frame, textvariable = self.boss_distance)
        boss_distance.grid(row = 1, column = 0, sticky = W)
        boss_distance.configure(font = 'arial 12 bold')

        self.update_boss_data()
        
    def update_boss_data(self):
        # call when the boss name, defenses, or distance changes
        self.boss_name.set(self.boss.get_title())
        self.boss_health.set("Defenses: " + str(self.boss.get_health()))
        self.boss_distance.set("Distance: " + str(self.boss.get_distance()))
        
        # change boss image
        self.boss_file = PhotoImage(file = self.boss.get_boss_img())
        self.boss_image = Label(self.boss_frame, image = self.boss_file, cursor = 'hand2')
        self.boss_image.grid(row = 0, column = 0, stick = W, padx = 5)
        self.boss_image.image = self.boss_file

        self.boss_tip = ToolTip(self.boss_image, self.boss.display_message(), self.update_boss_msg, '#CD3D3D')
        
        #Update boss distance progress bar
        self.update_distance_bar()
        
    def update_boss_msg(self):
        # used for updating the boss image tool tip message
        return self.boss.get_message()
        
    def make_character_frame(self):
        # create character data frame
        self.char_frame_bg = Frame(self)
        self.char_frame_bg.grid(row=2, column=0, sticky='news')

        self.name = Label(self.char_frame_bg, textvariable = self.character_name)
        self.name.grid(row = 0, column = 0, sticky=W, pady=4, padx=5)
        self.name.configure(font='arial 14 bold')

        self.char_frame = Frame(self.char_frame_bg)
        self.char_frame.grid(row=1, column=0, sticky='news')
        
        # place character menu buttons here, self.make_menu() will use this
        self.char_buttons_frame = Frame(self.char_frame)
        self.char_buttons_frame.grid(row=0, column=1, sticky='news')
        
        self.change_character_emotion(0, "main.gif")

    def change_character_emotion(self, i, img_str):
        # load character image
        char_img = PhotoImage(file = os.path.join("assets", "art", img_str))
        character_image = Label(self.char_frame, image = char_img, cursor = "hand2")
        character_image.grid(row = 0, column = 0, stick = W, padx = 5)
        character_image.image = char_img

        char_messages = ["Hi, I'm hacker JOE!", "We are doing great!", "I AM FURIOUS!"]
        ToolTip(character_image, char_messages[i], None, '#6BCD3D')
        
    def make_items_in_use_frame(self):
        self.items_frame = Frame(self, padding='40 0 0 0')
        self.items_frame.grid(row=2, column=1, sticky='news')

        self.items_in_use_title = Label(self.items_frame, text='Active Items')
        self.items_in_use_title.grid(row=0, column=0, columnspan=5, sticky=W, pady=4, padx=5)
        self.items_in_use_title.configure(font='arial 14 bold italic')

        self.software_label = Label(self.items_frame, text="Software:   ")
        self.software_label.grid(row=1, column=0, sticky=W, pady=4, padx=5)
        self.software_label.configure(font='arial 14')

        self.hardware_label = Label(self.items_frame, text="Hardware:   ")
        self.hardware_label.grid(row=2, column=0, sticky=W, pady=4, padx=5)
        self.hardware_label.configure(font='arial 14')

        self.component_label = Label(self.items_frame, text="Components:   ")
        self.component_label.grid(row=3, column=0, sticky=W, pady=4, padx=5)
        self.component_label.configure(font='arial 14')

    def spawn_about_window(self):
        about_window = Toplevel()
        about_window.title("About Daily Hack")

        about_window.config(background='#DCDAD5')
        about_window.columnconfigure(0, weight=1)
        about_window.columnconfigure(1, weight=1)
        about_window.minsize(width=300, height=200)
        about_window.maxsize(width=300, height=200)

        #Center window
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        
        
        x = (about_window.winfo_screenwidth() // 2) - \
            (width // 2)
        y = (about_window.winfo_screenheight() // 2) - \
            (height // 2)

        
        #Image frame
        main_image = PhotoImage(file=os.path.join("assets", "art", "mainHappy.gif"))
        main_image_frame = Label(about_window, image=main_image, padding="25 0 5 0")
        main_image_frame.grid(row=0, column=0, rowspan=3)
        main_image_frame.image = main_image

        #Logo frame
        logo_image = PhotoImage(file=os.path.join("assets", "art", "logo.gif"))
        logo_image_frame = Label(about_window, image=logo_image, padding="0 0 0 0")
        logo_image_frame.grid(row=1, column=1, sticky='w')
        logo_image_frame.image = logo_image
        
        #Text frame
        message_part_1 = 'Version 1.1'
        message_part_2 = '\nDaily Hack is brought to you by \nMSU Software engineering \nTeam 2'
        
        complete_message = message_part_1 + message_part_2
                           
        
        text_frame = Message(about_window, text=complete_message)  

        text_frame.configure(background='#DCDAD5',
                             foreground = '#000000',
                             font='arial 8',
                             justify='center',
                             width=200)
        
        text_frame.grid(row=4, column=0, columnspan=2)
                             
        about_window.geometry('{}x{}+{}+{}'.format(width, height,
                                                   x, y))

    def make_footer(self):
        # footer
        footer_frame_bg = Frame(self, style='footer.TFrame', padding=3)
        footer_frame_bg.grid(row=10, column=0, columnspan=7, sticky= (W, E))
        footer_frame_bg.columnconfigure(0, weight=1)

        # centered frame; holds logo and copyright text
        footer_frame = Frame(footer_frame_bg, style='footer.TFrame')
        footer_frame.grid(row=0, column=0)

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

    def notify(type, message):

        #type will be used later to add a small icon to the notifications
        #(a coin for money, save icon, etc)

        #the notification handler waits for new messages to be put in this queue
        #(it's a blocking wait, so it'll just sit there)
        GUI.notification_queue.put(message)

    def bind_buttons(self):
        #Navigation Buttons
        landing_page = self.frames['Landing_Page']
        landing_page.go_to_habits_button.bind("<1>", lambda e : self.page_navigator('habit'))

        landing_page.go_to_dailies_button.bind("<1>", lambda e : self.page_navigator('daily'))

        landing_page.go_to_tasks_button.bind("<1>", lambda e : self.page_navigator('task'))

    def check_assets(self):
        #for item in self.character.items:
        pass
    
    def update_cash(self):
        self.character_cash.set(str(self.character.cash))

    def update_name(self):
        self.character_name.set(self.character.name)

    def update_exp(self):
        self.character_exp.set(self.character.exp)

    def update_to_next_level(self):
        self.character_to_next_level.set(self.character.level * 100)

    def update_level(self):
        self.character_level.set(self.character.level)

    def update_rank(self):
        self.character_rank.set(self.get_rank_name())

    def update_item_count(self):
        get_count = 0
        for item in self.character.items:
            if item.active == 'False':
                get_count += 1
        str_set = str("Inventory ( " + str(get_count) + " )")
        self.character_item_count.set(str_set)

    def add_hack(self, hack_data):
        #messagebox.showinfo("Hack Info", "Added Hack "+hack_data.title)
        self.character.add_hack(hack_data)
        self.update_stats_banner()
        self.redraw()

    def edit_hack(self, hack_ID, hack_data):
        #messagebox.showinfo("Hack Info", "Edited Hack "+hack_data.title)
        self.character.edit_hack(hack_ID, hack_data)
        self.update_stats_banner()
        self.redraw()

    def complete_hack(self, hack_ID):

        hack_value = int(self.character.get_hack(hack_ID).value)
        hack_type = self.character.get_hack(hack_ID).h_type

        #messagebox.showinfo("Hack Info", "Completed Hack "+str(ID))
        if(self.character.complete_hack(hack_ID, self.current_date)):
            self.redraw()
            self.update_stats_banner()
            if hack_value < 0: # For negative habits
                self.change_character_emotion(2, "mainMad.gif")
            else:
                self.change_character_emotion(1, "mainHappy.gif")
                self.attack_boss(5)
            self.check_time()
            return True


    def delete_hack(self, hack_ID):
        #messagebox.showinfo("Hack Info", "Deleted Hack "+str(ID))
        self.character.remove_hack(hack_ID)
        self.update_stats_banner()
        self.redraw()
        self.change_character_emotion(2, "mainMad.gif")

    def page_navigator(self, page):
        if page == 'habit':
            self.show_frame('habit')

        elif page == 'daily':
            self.show_frame('daily')

        elif page == 'task':
            self.show_frame('task')

    def redraw(self):
        """
        Redraws each area of the GUI after data is modified
        """
        self.frames['Landing_Page'].redraw(self.character)
        self.frames['Work_Space'].redraw(self.character)
        #self.frames['Generic'].redraw(self.character)

    """ This is the default for all menu bar options,
    except for exit """
    def temp_menu_func(self):
        print("test menu")

    def show_frame(self, frame_class):
        '''
        Show a frame for the given frame class
        '''

        if frame_class in ('habit', 'daily', 'task', 'shop', 'inventory'):
            if self.current_visible_frame != self.frames['Work_Space']:
                self.current_visible_frame.grid_remove()

            frame = self.frames['Work_Space']
            frame.grid(row = 4, column = 0, columnspan = 7,
                       rowspan = 4, sticky = 'news')

            #Adjust notebook to desired tab
            frame.select_tab(frame_class)
            self.current_visible_frame = frame

        else:
            if self.current_visible_frame != self.frames[frame_class]:
                if self.current_visible_frame != None:
                    self.current_visible_frame.grid_remove()

                frame = self.frames[frame_class]
                frame.grid(row = 4, column = 0, columnspan = 7,
                           rowspan = 4, sticky = 'news')
                self.current_visible_frame = frame

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

    def set_active(self, item, state):
        try:
            self.character.items[item.ID].active = state
            self.update_item_count()
        except:
            pass
        
    def use_item(self, item):
        if item != None:
            if item.component == 'software':
                if item.item_type == 'smokescreen':
                    self.boss.push_back(item.effect)
                    self.update_boss_data()
                else:
                    self.character.use_item(item)
                    self.update_item_count()
            elif item.component == 'hardware':
                self.character.equip_item(item)
                self.update_item_count()
            elif item.component == 'component':
                self.character.equip_item(item)
                self.update_item_count()
            elif item.component == 'misc':
                self.character.use_item(item)
                self.update_exp()
            elif item.component == 'food':
                messagebox.showinfo('Break Time', 'Go enjoy some ' + str(item.description))
                self.remove_item(item)
            self.update_item_count()

    def unequip_item(self, item):
        return self.character.equipped.pop(item.item_type, None)
        
    def remove_effect(self, item):
        return self.character.effects.pop(item.item_type, None)

    def remove_item(self, item):
        self.character.remove_item(item.ID)
        self.character.set_item_IDs()
        self.update_item_count()

    def buy_item(self, item):
        if self.character.cash >= item.value:
            self.character.add_item(item)
            self.character.cash -= item.value
            self.character.set_item_IDs()
            self.character_cash.set(self.character.cash)
            self.update_item_count()
            GUI.notify("type", str(item.name) + " bought!")
            return item
        else:
           self.inst_notify("exclamation", "Not enough cash for " + item.name + "!")
           return None

    def check_time(self):
        None
        """
        for i in self.character.effects:
            if self.character.effects[i].duration < time.time():
                #something here to connect to time_up() in the inventory
                self.character.effects.pop(i)
        """

    def sell_item(self, item):
        """
        called in Inventory class, sell and remove item at 75% of full price
        """
        self.character.cash += int(float(item.value)*0.75)
        self.character.remove_item(item.ID)
        self.update_stats_banner()
        self.update_item_count()

    def update_stats_banner(self):
        """
        this function is called in landing_page.py and work_space.py when the user
        presses the complete button for a task, daily, or habit. The cash and exp
        data are updated on the banner.
        """
        self.update_cash()
        self.update_exp()
        self.check_level()
        self.update_level()

    #BOSS Methods
    def attack_boss(self, amount):
        damage_mult = 1
        if 'CPU' in self.character.equipped:
            damage_mult *= self.character.equipped['CPU'].effect

        if 'penetrate' in self.character.effects:
            damage_mult *= self.character.effects['penetrate'].effect
            
        self.boss.damage(amount * damage_mult)
        if self.boss.health < 1:
            self.defeat_boss()
        self.check_time()

    #def defeat_boss(self):
    #    self.inst_notify("exclamation", self.boss.get_title() + 
    #                        " attacks your systems!")
    #    self.character.health -= 5

    def defeat_boss(self):
        '''
        You defeat the boss/authoritative figure
        Should gain experience, cash
        '''
        self.inst_notify("exclamation", self.boss.get_defeat_message())

        #Increase character cash based on boss level
        reward = [500,750,1200,2000,5000]

        if self.boss.level < len(reward):
            self.character.cash += reward[self.boss.level]
        else:
            self.character.cash += reward[len(reward)-1]

        #Increase character experience
        experience_gain = [100,400,900,1500,2500]

        if self.boss.level < len(experience_gain):
            self.character.exp += experience_gain[self.boss.level]
        else:
            self.character.exp += experience_gain[len(experience_gain)-1]

        #Upgrade boss to next authoritative figure
        self.boss.next()
        self.update_distance_bar()
        self.check_boss()
        self.update_boss_data()
        
        #Reflect character update
        self.update_stats_banner()
        
    def check_boss(self):
        if self.boss.active == 1:
            if self.boss.new == 1:
                GUI.notify("type",
                           self.boss.display_message())
                print("BOSS:", self.boss.display_message())

    def steal_character_money(self, amount):
        if self.character.cash > 0:
            self.character.cash -= amount

            
            message = 'You were robbed!'
            self.inst_notify('exclamation',
                                message)

        #Set character cash lower limit
        if self.character.cash < 0:
            self.character.cash = 0

        self.update_cash()
        
    def check_level(self):
        curr_level = int(self.character_level.get())
        exp = int(self.character_exp.get())
        level_up = 100 * curr_level
        
        if exp >= level_up and curr_level >0:
            #LEVEL UP! WOOOOOOOOOO HOOOOOOOOOOO!
            #Reset experience
            self.character.level = int(curr_level) + 1
            self.character.exp = 0
            self.update_level()
            self.update_exp()
            self.update_to_next_level()
            GUI.notify("type", "LEVEL UP! lvl"+str(self.character.level))
            self.check_rank_up()
        self.check_boss()

    def damage_character(self):
        pass

    def check_rank_up(self):
        curr_rank = self.get_rank_number()
        # if current rank is not max, check if this level allows a new rank
        if curr_rank < 8:
            rank_up_level = 3 * curr_rank
            curr_level = self.character.level
            if int(curr_level) == rank_up_level:
                #new rank get
                self.update_rank()
                rank_name = self.get_rank_name()
                GUI.notify("type", "CLASS CHANGE TO " + rank_name)

    def get_rank_number(self):
        curr_rank = int(self.character.level / 3)
        if curr_rank > 7:
            return 8
        else:
            return curr_rank

    def get_rank_name(self):
        rank_list = [
        "N00b",
        "Script Kiddie",
        "Programming Neophyte",
        "Code Poet",
        "Initiate Hacker",
        "Journeyman Hacker",
        "Open Sourceeror",
        "Hacker Elite",
        "Grandmaster of the Internet",
        ]
        ranking = self.get_rank_number()
        return rank_list[ranking]
        
    def get_item_count(self):
        print('item count: ' + str(len(self.character.get_all_items())))
        return len(self.character.get_all_items())

    def get_character_items(self):
        return self.character.get_all_items()

    def go_to_home(self):
        self.clear_menus(0)
        self.show_frame('Landing_Page')

    def go_to_habits(self, no_frame = False):
        self.clear_menus(1)
        if not no_frame:
            self.show_frame('habit')

    def go_to_tasks(self, no_frame = False):
        self.clear_menus(2)
        if not no_frame:
            self.show_frame('task')
            main.__subclasshook__

    def go_to_dailies(self, no_frame = False):
        self.clear_menus(3)
        if not no_frame:
            self.show_frame('daily')

    def go_to_generic(self):
        self.clear_menus(4)
        self.show_frame('Generic')

    def go_to_shop(self):
        self.clear_menus(4)
        self.show_frame('shop')

    def go_to_inventory(self):
        self.clear_menus(5)
        self.show_frame('inventory')

    def save_game(self):
        #messagebox.showinfo("Save", "Game Saved!")
        GUI.notify("", "Game data saved!")
        self.game_data.save_data(self.character, self.boss,
                                 self.const_current_date)
        self.game_data.save_to_file()

    def no_where(self):
        messagebox.showinfo("Placeholder", "I don't have anywhere to go yet :( !")


def main():
    """
      Stub for main function
    """
    db = authenticate.db()

    #main_character = load('Tester')

    root = Tk()
    app = GUI(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()

# These imports have been moved to resolve import loops between
# shop, work_space, and engine over the Item class.
from shop import *
from inventory import *
