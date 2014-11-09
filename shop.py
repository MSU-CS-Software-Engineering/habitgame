from tkinter import *
from tkinter.ttk import *
from enum import Enum
from hack_classes import Item
from inventory import MyInventory
import os.path

# Each item in the store is placed in an Item object
class SetItem():
    def __init__(self, name, file, description, cost, uses, item_type):
        self.name = name
        self.file = file
        self.description = description
        self.cost = cost
        self.uses = uses
        self.item_type = item_type
        
    def getName(self):
        return self.name
    
    def getFile(self):
        return self.file
    
    def getDescription(self):
        return self.description
    
    def getCost(self):
        return self.cost

    def getUses(self):
        return self.uses

    def getItemType(self):
        return self.item_type
    
# this class is used for link the shop class with the GUI class
class MyShop():
    api = None
    my_shop = None
    
    # called in work_space.py
    def setShop(shop_frm):
        MyShop.my_shop = Shop(shop_frm)

    # called at the end of engine/GUI's constructor function 
    def setApi(api_ref):
        MyShop.api = api_ref

        
class Shop():
    def __init__(self, shop_plugin_frame):
        """
            shop_plugin_frame is a frame reference that will contain the shop frame.
            This prevents adding more columns to the main GUI's column count
        """
        
        # store all items that can be bought in this list
        self.items = []

        # used for highlighting an item when the mouse hovers an item
        self.border_frames = []
        
        # store an engine.Item object for each shop item.
        #Object will be used as parameter for the GUI buy_item function
        self.live_items = []
        
        # used to select self.live_items object
        self.buy_item_id = 0
        
        # component items
        self.items.append(SetItem('Motherboard', os.path.join("assets", "art", "mobo.gif"),
                                  "motherboard description",
                                  200, 1, "component"))
        
        self.items.append(SetItem('RAM 16gb', os.path.join("assets", "art", "ramred.gif"),
                                  "ram 16gb description",
                                  150, 1, "component"))
        
        self.items.append(SetItem('RAM 8gb', os.path.join("assets", "art", "ramgreen.gif"),
                                  "ram 8gb description",
                                  75, 1, "component"))
        
        self.items.append(SetItem('CPU fan', os.path.join("assets", "art", "cpufan.gif"),
                                  "cpu fan description",
                                  50, 1, "component"))
        
        self.items.append(SetItem('CPU 3.5 Ghz', os.path.join("assets", "art", "cpu.gif"),
                                  "cpu 3.5 Ghz description",
                                  300, 1, "component"))
        
        self.items.append(SetItem('GPU 2gb', os.path.join("assets", "art", "gpured.gif"),
                                  "gpu 2gb description",
                                  300, 1, "component"))
        
        self.items.append(SetItem('GPU 1gb', os.path.join("assets", "art", "gpugreen.gif"),
                                  "gpu 1gb description",
                                  150, 1, "component"))


        # software items
        self.items.append(SetItem('Fortify', os.path.join("assets", "art", "fortify.gif"),
                                  "50% less damage for bad habits and missing habits",
                                  2500, 1, "software"))
        
        self.items.append(SetItem('Fork', os.path.join("assets", "art", "fork.gif"),
                                  "2x habit reward",
                                  10000, 1, "software"))
        
        self.items.append(SetItem('Smokescreen', os.path.join("assets", "art", "smoke.gif"),
                                  "restore to full health",
                                  5000, 1, "software"))
        
        self.items.append(SetItem('Penetrate', os.path.join("assets", "art", "penetrate.gif"),
                                  "2x damage to bosses, receive 1/2 of habit reward",
                                  7500, 1, "software"))

        
        # hardware items
        self.items.append(SetItem('Laptop', os.path.join("assets", "art", "laptop.gif"),
                                  "laptop description",
                                  1250, 1, "hardware"))
        
        self.items.append(SetItem('Desktop', os.path.join("assets", "art", "desktop.gif"),
                                  "desktop description",
                                  2000, 1, "hardware"))
        
        self.items.append(SetItem('Terminal', os.path.join("assets", "art", "terminal.gif"),
                                  "terminal description",
                                  10000, 1, "hardware"))
        
        self.items.append(SetItem('Server', os.path.join("assets", "art", "server.gif"),
                                  "server description",
                                  5000, 1, "hardware"))
        
        self.items.append(SetItem('Desk', os.path.join("assets", "art", "desk.gif"),
                                  "desk description",
                                  500, 1, "hardware"))

        
        # food items
        self.items.append(SetItem('Cake', os.path.join("assets", "art", "cake.gif"),
                                  "cake description",
                                  15, 1, "food"))
        
        self.items.append(SetItem('Chicken', os.path.join("assets", "art", "chicken.gif"),
                                  "chicken description",
                                  10, 1, "food"))
        
        self.items.append(SetItem('Pizza', os.path.join("assets", "art", "pizza.gif"),
                                  "pizza description",
                                  20, 1, "food"))
        
        self.items.append(SetItem('Soda', os.path.join("assets", "art", "soda.gif"),
                                  "soda description",
                                  30, 1, "food"))
        
        self.items.append(SetItem('Popcorn', os.path.join("assets", "art", "popcorn.gif"),
                                  "popcorn description",
                                  5, 1, "food"))


        # miscellaneous items
        self.items.append(SetItem('Gold coins', os.path.join("assets", "art", "goldcoins.gif"),
                                  "gold coins description",
                                  50000, 1, "misc"))
        
        self.items.append(SetItem('Change', os.path.join("assets", "art", "change.gif"),
                                  "change description",
                                  50, 1, "misc"))
        
        self.items.append(SetItem('Dollars', os.path.join("assets", "art", "dollars.gif"),
                                  "dollars description",
                                  500, 1, "misc"))
        
        self.items.append(SetItem('Money bag', os.path.join("assets", "art", "moneybag.gif"),
                                  "money bag description",
                                  2000, 1, "misc"))


        # create a canvas to allow for scrolling of the shop Frame
        sh_canvas = Canvas(shop_plugin_frame, highlightthickness=0, background='#EBEDF1')
        sh_canvas.grid(row=4, column=0, sticky='news')

        # create the shop frame and place it inside the canvas
        self.shopFrame = Frame(sh_canvas, borderwidth=0, style='shopFrame.TFrame', padding=10) 
        self.shopFrame.grid(sticky='news')
        
        self.scrollBar = Scrollbar(shop_plugin_frame, orient="vertical", command=sh_canvas.yview)
        sh_canvas.configure(yscrollcommand=self.scrollBar.set)
        
        shop_plugin_frame.grid_columnconfigure(0, weight=1)
        shop_plugin_frame.grid_rowconfigure(4, weight=1)
        
        sh_canvas.create_window((0,0), window=self.shopFrame, anchor='nw', tags='self.shopFrame')
        self.scrollBar.grid(row=0, column=1, rowspan=5, sticky='ns')

        def setupCanvasFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            sh_canvas.configure(scrollregion=sh_canvas.bbox("all"))
            
        self.shopFrame.bind("<Configure>", setupCanvasFrame)

        self.style = Style()
        self.style.configure('shopFrame.TFrame', background='#EBEDF1')

        def scroll_m(event):
            """ allows for mouse wheel scrolling """
            try:
                sh_canvas.yview_scroll(-1 * int(event.delta/120), "units")
            except:
                pass

        sh_canvas.bind("<MouseWheel>", lambda e: scroll_m(e))

        
        # shop divider labels
        components = Label(self.shopFrame, text="Components", padding=3)
        components.grid(row=0, column=0, columnspan = 4, sticky='news')
        components.configure(background="#A3BECD", font="arial 16 bold")
        
        software = Label(self.shopFrame, text="Software", padding=3)
        software.grid(row=2, column=0, columnspan = 4, sticky='news')
        software.configure(background="#CDA3A3", font="arial 16 bold")
        
        hardware = Label(self.shopFrame, text="Hardware", padding=3)
        hardware.grid(row=4, column=0, columnspan = 4, sticky='news')
        hardware.configure(background="#ACCDA3", font="arial 16 bold")
        
        food = Label(self.shopFrame, text="Food", padding=3)
        food.grid(row=6, column=0, columnspan = 4, sticky='news')
        food.configure(background="#CDC7A3", font="arial 16 bold")
        
        misc = Label(self.shopFrame, text="Miscellaneous", padding=3)
        misc.grid(row=8, column=0, columnspan = 4, sticky='news')
        misc.configure(background="#BCA3CD", font="arial 16 bold")

        
        self.itemName = StringVar()
        self.itemName.set('name')
        
        self.itemDesc = StringVar()
        self.itemDesc.set('description')
        
        self.itemCost = StringVar()
        self.itemCost.set('cost')
        
        # selected item's name
        self.itemSelect = Label(shop_plugin_frame, textvariable=self.itemName,
                                wraplength=800, padding='10 5 5 5')
        self.itemSelect.grid(sticky='news', row=0)
        self.itemSelect.configure(font='arial 14 bold', foreground='#FFD237', background='#1E1E1E')
        
        # selected item's description
        self.descriptSelect = Label(shop_plugin_frame, textvariable=self.itemDesc,
                                    wraplength=800, padding='10 5 5 5')
        self.descriptSelect.grid(sticky='news', row=1)
        self.descriptSelect.configure(font='arial 12 bold', foreground='white', background='#444444')
        
        # selected item's cost
        self.costSelect = Label(shop_plugin_frame, textvariable=self.itemCost,
                                wraplength=800, padding='10 5 5 5')
        self.costSelect.grid(sticky='news', row=2)
        self.costSelect.configure(font='arial 12 bold', foreground='white', background='#444444')
        
        
        # create a 'buy' label to act as a button
        self.buy_button = Label(shop_plugin_frame, text='Buy', style='buy.TLabel', anchor='center', padding=5)
        self.buy_button.grid(sticky='news', row=3)

        def buy_on_off(buy):
            if self.itemName.get() != 'name' and buy:
                self.style.configure('buy.TLabel', background='#B6DE61')
            elif self.itemName.get() !='name' and not buy:
                self.style.configure('buy.TLabel', background='#82AE24')
            
        self.buy_button.bind('<Enter>', lambda e: buy_on_off(True))
        self.buy_button.bind('<Leave>', lambda e: buy_on_off(False))
        self.buy_button.bind('<1>', lambda e: self.buyItem())
        
        self.style.configure('buy.TLabel', background='#646464',
                             foreground='#1E1E1E', font='arial 14 bold')

        # populate store with items
        self.createItems()

            
    def buyItem(self):
        if self.itemName.get() != 'name':
            get_item = self.live_items[self.buy_item_id]
            item = MyShop.api.buy_item(get_item)
            if item != None:
                MyInventory.my_inventory.addItem(item)

        
    def setItemInfo(self, name, descript, cost, item_id):
        """
        setItemInfo sets the info to be shown in the item
        information frame, right above the buy button
        """
        self.buy_button.configure(cursor='hand2')
        self.style.configure('buy.TLabel', background='#82AE24',
                             foreground='#1E1E1E', font='arial 14 bold')
        self.itemName.set(name)
        descript = "Info: " + descript
        self.itemDesc.set(descript)
        cost = "Cost: $" + str(cost)
        self.itemCost.set(cost)
        self.buy_item_id = item_id


    def highlight(self, i, enter):
        # this loop is needed to prevent all item border frames from becoming highlighted
        for j in range(len(self.border_frames)):
            self.border_frames[j].config(style='a.TFrame')
            self.style.configure('a.TFrame', background='#EBEDF1')
            
        self.border_frames[i].config(style='b.TFrame')
        if enter: # mouse enter
            self.style.configure('b.TFrame', background='#26507D')
        else: # mouse leave
            self.style.configure('b.TFrame', background='#EBEDF1')

        
    def createItems(self):
        item_types = {"component":[0,0,0], # [0,0,0] = frame div id, row num, col num
                      "software":[1,0,0],
                      "hardware":[2,0,0],
                      "food":[3,0,0],
                      "misc":[4,0,0]}
        
        frame_divs = []

        t_row = 1
        for i in range(len(item_types)):
            frame_div = Frame(self.shopFrame, style='c.TFrame')
            frame_div.grid(row=t_row, column=0, sticky='wn')
            frame_divs.append(frame_div)
            t_row += 2
            
        # loops through the list of items that need to be created and shown in the shop
        for i in range(len(self.items)):
            # prep appropriate data for when the user clicks on a item
            t_name = self.items[i].getName()
            t_descript = self.items[i].getDescription()
            t_cost = self.items[i].getCost()

            self.live_items.append(Item(self.items[i].getName(),
                                    self.items[i].getDescription(),
                                    self.items[i].getFile(),
                                    self.items[i].getCost(),
                                    self.items[i].getUses()))


            #create frame border for item data
            divs_id = item_types[self.items[i].getItemType()]
            border_frame = Frame(frame_divs[divs_id[0]], padding=2, cursor='hand2', style='c.TFrame')
            border_frame.grid(row=divs_id[1], column=divs_id[2], padx=7, pady=7, sticky='wn')
            self.style.configure('c.TFrame', background='#EBEDF1')

            # increment columns and rows
            divs_id[2] += 1
            if divs_id[2] >= 5: # max of 5 items per row
               divs_id[2] = 0
               divs_id[1] += 1
               
            
            # user clicks on the frame border
            border_frame.bind('<1>', lambda e, name=t_name, descript=t_descript, cost=t_cost,
                              item_id=i : self.setItemInfo(name, descript, cost, item_id))
            self.border_frames.append(border_frame)
            

            #create frame for item data
            item_frame = Frame(border_frame, style='itemFrame.TFrame', padding=4, cursor='hand2')
            item_frame.grid(sticky='wn')
            self.style.configure('itemFrame.TFrame', background='#EBEDF1')
            
            # user clicks on the frame containing all of the item's info
            item_frame.bind('<1>', lambda e, name=t_name, descript=t_descript, cost=t_cost,
                            item_id=i : self.setItemInfo(name, descript, cost, item_id))
            item_frame.bind('<Enter>', lambda e, _i=i:
                            self.highlight(_i, True))
            item_frame.bind('<Leave>', lambda e, _i=i:
                            self.highlight(_i, False))

            
            #create label to hold the item's name
            new_desc = Label(item_frame, text=self.items[i].getName(), style='name.TLabel',
                             padding=3, cursor='hand2')
            new_desc.grid(row=0, column=0)
            self.style.configure('name.TLabel', font='arial 12 bold', background='#EBEDF1')
            temp_str = self.items[i].getFile()
            new_desc.bind('<1>', lambda e, tstr=temp_str: self.itemSelect.configure(text=tstr))
            # user clicks on the label to hold the item's name
            new_desc.bind('<1>', lambda e, name=t_name, descript=t_descript, cost=t_cost,
                          item_id=i : self.setItemInfo(name, descript, cost, item_id))

            
            #create label to hold the item's image
            img = PhotoImage(file=self.items[i].getFile())
            new_item = Label(item_frame, image=img, style='item.TLabel', cursor='hand2')
            new_item.grid(row=1, column=0)
            new_item.image = img
            self.style.configure('item.TLabel', background='#EBEDF1')
            temp_str = self.items[i].getFile()
            # user clicks on the image of the item
            new_item.bind('<1>', lambda e, name=t_name, descript = t_descript, cost=t_cost,
                          item_id=i : self.setItemInfo(name, descript, cost, item_id))        


            #create label to hold the item's cost
            new_cost = Label(item_frame, text='$'+str(self.items[i].getCost()),
                             style='cost.TLabel', padding=3, cursor='hand2')
            new_cost.grid(row=2, column=0)
            self.style.configure('cost.TLabel', font='arial 14', foreground='green', background='#EBEDF1')
            temp_str = self.items[i].getFile()
            # user clicks on the cost label
            new_cost.bind('<1>', lambda e, name=t_name, descript = t_descript, cost=t_cost,
                          item_id=i : self.setItemInfo(name, descript, cost, item_id))

