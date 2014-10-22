from tkinter import *
from tkinter.ttk import *
from enum import Enum
from engine import Item
import os.path

# simple enum class for determining the Item type
class Type(Enum):
    hardware = 1
    component = 2
    software = 3
    food = 4
    money = 5

# Each item in the store is placed in an Item object
class SetItem():
    def __init__(self, name, file, item_type, description, cost, row, column):
        self.name = name
        self.file = file
        self.item_type = item_type
        self.description = description
        self.cost = cost
        self.row = row
        self.column = column
        
    def getName(self):
        return self.name
    
    def getFile(self):
        return self.file

    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column
    
    def getCost(self):
        return self.cost
    
    def getDescription(self):
        return self.description

    
# this class is used for link the shop class with the GUI class
class MyShop():
    app = None
    my_shop = None

    # called in work_space.py
    def setShop(shop_frm):
        MyShop.my_shop = Shop(shop_frm)

    # called at the end of engine/GUI's constructor function 
    def setApp(app_ref):
        MyShop.app = app_ref

        
class Shop():
    def __init__(self, shop_plugin_frame):
        """
            shop_plugin_frame is a frame reference that will contain the shop frame.
            This prevents adding more columns to the main GUI's column count
        """
        
        # store all items that can be bought in this list
        self.items = []

        # store an engine.Item object for each shop item.
        #Object will be used as parameter for the GUI buy_item function
        self.live_items = []
        
        # used to select self.live_items object
        self.buy_item_id = 0
        
        # component items
        self.items.append(SetItem('Motherboard', os.path.join("assets", "art", "mobo.gif"),
                               Type.component, "motherboard description", 200, 1, 0))
        self.items.append(SetItem('RAM 16gb', os.path.join("assets", "art", "ramred.gif"),
                               Type.component, "ram 16gb description", 150, 1, 1))
        self.items.append(SetItem('RAM 8gb', os.path.join("assets", "art", "ramgreen.gif"),
                               Type.component, "ram 8gb description", 75, 1, 2))
        self.items.append(SetItem('CPU fan', os.path.join("assets", "art", "cpufan.gif"),
                               Type.component, "cpu fan description", 50, 1, 3))
        self.items.append(SetItem('CPU 3.5 Ghz', os.path.join("assets", "art", "cpu.gif"),
                               Type.component, "cpu 3.5 Ghz description", 300, 2, 0))
        self.items.append(SetItem('GPU 2gb', os.path.join("assets", "art", "gpured.gif"),
                               Type.component, "gpu 2gb description", 300, 2, 1))
        self.items.append(SetItem('GPU 1gb', os.path.join("assets", "art", "gpugreen.gif"),
                               Type.component, "gpu 1gb description", 150, 2, 2))

        # software items
        self.items.append(SetItem('Fortify', os.path.join("assets", "art", "fortify.gif"),
                               Type.money, "50% less damage for bad habits and missing habits", 2500, 4, 0))
        self.items.append(SetItem('Fork', os.path.join("assets", "art", "fork.gif"),
                               Type.money, "2x habit reward", 10000, 4, 1))
        self.items.append(SetItem('Smokescreen', os.path.join("assets", "art", "smoke.gif"),
                               Type.money, "restore to full health", 5000, 4, 2))
        self.items.append(SetItem('Penetrate', os.path.join("assets", "art", "penetrate.gif"),
                               Type.money, "2x damage to bosses, receive 1/2 of habit reward", 7500, 4, 3))
        
        # hardware items
        self.items.append(SetItem('Laptop', os.path.join("assets", "art", "laptop.gif"),
                               Type.hardware, "laptop description", 1250, 6, 0))
        self.items.append(SetItem('Desktop', os.path.join("assets", "art", "desktop.gif"),
                               Type.hardware, "desktop description", 2000, 6, 1))
        self.items.append(SetItem('Terminal', os.path.join("assets", "art", "terminal.gif"),
                               Type.hardware, "terminal description", 10000, 6, 2))
        self.items.append(SetItem('Server', os.path.join("assets", "art", "server.gif"),
                               Type.hardware, "server description", 5000, 6, 3))
        self.items.append(SetItem('Desk', os.path.join("assets", "art", "desk.gif"),
                               Type.hardware, "desk description", 500, 7, 0))
        
        # food items
        self.items.append(SetItem('Cake', os.path.join("assets", "art", "cake.gif"),
                               Type.food, "cake description", 15, 9, 0))
        self.items.append(SetItem('Chicken', os.path.join("assets", "art", "chicken.gif"),
                               Type.food, "chicken description", 10, 9, 1))
        self.items.append(SetItem('Pizza', os.path.join("assets", "art", "pizza.gif"),
                               Type.food, "pizza description", 20, 9, 2))
        self.items.append(SetItem('Soda', os.path.join("assets", "art", "soda.gif"),
                               Type.food, "soda description", 30, 9, 3))
        self.items.append(SetItem('Popcorn', os.path.join("assets", "art", "popcorn.gif"),
                               Type.food, "popcorn description", 5, 10, 0))

        # miscellaneous items
        self.items.append(SetItem('Gold coins', os.path.join("assets", "art", "goldcoins.gif"),
                               Type.money, "gold coins description", 50000, 12, 0))
        self.items.append(SetItem('Change', os.path.join("assets", "art", "change.gif"),
                               Type.money, "change description", 50, 12, 1))
        self.items.append(SetItem('Dollars', os.path.join("assets", "art", "dollars.gif"),
                               Type.money, "dollars description", 500, 12, 2))
        self.items.append(SetItem('Money bag', os.path.join("assets", "art", "moneybag.gif"),
                               Type.money, "money bag description", 2000, 12, 3))


        # create a canvas to allow for scrolling of the shop Frame
        self.canvas = Canvas(shop_plugin_frame, highlightthickness=0, background='white')
        self.canvas.grid(sticky='news')
        
        # create the shop frame and place it inside the canvas
        self.shopFrame = Frame(self.canvas, borderwidth=0, style='shopFrame.TFrame', padding=10) 
        self.shopFrame.grid(sticky='news')
        
        self.scrollBar = Scrollbar(shop_plugin_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        
        shop_plugin_frame.grid_columnconfigure(0, weight=1)
        shop_plugin_frame.grid_rowconfigure(0, weight=1)
        
        self.canvas.create_window((0,0), window=self.shopFrame, anchor='nw', tags='self.shopFrame')
        self.scrollBar.grid(row=0, column=1, sticky='ns')
        
        self.shopFrame.bind("<Configure>", self.setupCanvasFrame)

        self.style = Style()
        self.style.configure('shopFrame.TFrame', background='white')


        # shop divider labels
        components = Label(self.shopFrame, text="Components", padding=3)
        components.grid(row=0, column=0, columnspan = 4, sticky='news')
        components.configure(background="#A3BECD", font="arial 16 bold")
        
        software = Label(self.shopFrame, text="Software", padding=3)
        software.grid(row=3, column=0, columnspan = 4, sticky='news')
        software.configure(background="#A3BECD", font="arial 16 bold")
        
        hardware = Label(self.shopFrame, text="Hardware", padding=3)
        hardware.grid(row=5, column=0, columnspan = 4, sticky='news')
        hardware.configure(background="#A3BECD", font="arial 16 bold")
        
        food = Label(self.shopFrame, text="Food", padding=3)
        food.grid(row=8, column=0, columnspan = 4, sticky='news')
        food.configure(background="#A3BECD", font="arial 16 bold")
        
        misc = Label(self.shopFrame, text="Miscellaneous", padding=3)
        misc.grid(row=11, column=0, columnspan = 4, sticky='news')
        misc.configure(background="#A3BECD", font="arial 16 bold")
        
        
        # selected item's name
        self.itemSelect = Label(shop_plugin_frame, text='name', padding=5)
        self.itemSelect.grid(sticky='news', row=1, columnspan=2)
        self.itemSelect.configure(font='arial 14 bold')
        
        # selected item's description
        self.descriptSelect = Label(shop_plugin_frame, text='description', padding=5)
        self.descriptSelect.grid(sticky='news', row=2, columnspan=2)
        self.descriptSelect.configure(font='arial 12 bold')
        
        # selected item's cost
        self.costSelect = Label(shop_plugin_frame, text='cost', padding=5)
        self.costSelect.grid(sticky='news', row=3, columnspan=2)
        self.costSelect.configure(font='arial 12 bold')
        
        
        # create a 'buy' label to act as a button
        buy = Label(shop_plugin_frame, text='Buy', style='buy.TLabel', anchor='center', padding=5)
        buy.grid(sticky='news', row=4, columnspan=2)
        buy.bind('<Enter>', lambda e: self.style.configure('buy.TLabel', background='#0086D3'))
        buy.bind('<Leave>', lambda e: self.style.configure('buy.TLabel', background='#0086BF'))
        buy.bind('<1>', lambda e: self.buyItem()) 
        self.style.configure('buy.TLabel', background='#0086BF', font='arial 14 bold')
        #item_frame.bind('<1>', lambda e, name=t_name, descript=t_descript,
                            #cost = t_cost, : self.setItemInfo(name, descript, cost))
        # populate store with items
        self.createItems()

    def buyItem(self):
        MyShop.app.buy_item(self.live_items[self.buy_item_id])
        
    """
        setItemInfo sets the info to be shown in the item
        information frame, right above the buy button
    """
    def setItemInfo(self, name, descript, cost, item_id):
        name = "Item: " + name
        self.itemSelect.configure(text=name)
        descript = "Info: " + descript
        self.descriptSelect.configure(text=descript)
        cost = "Cost: $" + str(cost)
        self.costSelect.configure(text=cost)
        self.buy_item_id = item_id

    def createItems(self):
        # loops through the list of items that need to be created and shown in the shop
        for i in range(len(self.items)):
            # prep appropriate data for when the user clicks on a item
            t_name = self.items[i].getName()
            
            self.live_items.append(Item(self.items[i].getName(),
                 self.items[i].getFile(),
                 self.items[i].getCost(), 1,
                 self.items[i].getDescription()))
            
            t_descript = self.items[i].getDescription()
            t_cost = self.items[i].getCost()
            
            #create frame for item data
            item_frame = Frame(self.shopFrame, style='itemFrame.TFrame', padding=10)
            item_frame.grid(row=self.items[i].getRow(), column=self.items[i].getColumn(), sticky='wn')
            self.style.configure('itemFrame.TFrame', background='white')
            # user clicks on the frame containing all of the item's info
            item_frame.bind('<1>', lambda e, name=t_name, descript=t_descript,
                            cost=t_cost, item_id=i : self.setItemInfo(name, descript, cost, item_id))

            #create label to hold the item's name
            new_desc = Label(item_frame, text=self.items[i].getName(), style='name.TLabel', padding=3)
            new_desc.grid(row=0, column=0)
            self.style.configure('name.TLabel', font='arial 12 bold', background='white')
            temp_str = self.items[i].getFile()
            new_desc.bind('<1>', lambda e, tstr=temp_str: self.itemSelect.configure(text=tstr))
            # user clicks on the label to hold the item's name
            new_desc.bind('<1>', lambda e, name=t_name, descript=t_descript,
                            cost=t_cost, item_id=i : self.setItemInfo(name, descript, cost, item_id))
            
            #create label to hold the item's image
            img = PhotoImage(file=self.items[i].getFile())
            new_item = Label(item_frame, image=img, style='item.TLabel')
            new_item.grid(row=1, column=0)
            new_item.image = img
            self.style.configure('item.TLabel', background='white')
            temp_str = self.items[i].getFile()
            # user clicks on the image of the item
            new_item.bind('<1>', lambda e, name=t_name, descript = t_descript,
                            cost=t_cost, item_id=i : self.setItemInfo(name, descript, cost, item_id))        

            #create label to hold the item's cost
            new_cost = Label(item_frame, text='$'+str(self.items[i].getCost()), style='cost.TLabel', padding=3)
            new_cost.grid(row=2, column=0)
            self.style.configure('cost.TLabel', font='arial 14', foreground='green', background='white')
            temp_str = self.items[i].getFile()
            # user clicks on the cost label
            new_cost.bind('<1>', lambda e, name=t_name, descript = t_descript,
                            cost=t_cost, item_id=i : self.setItemInfo(name, descript, cost, item_id))
        
    def setupCanvasFrame(self, event):
        # resets the scroll region for the frame inserted into the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
