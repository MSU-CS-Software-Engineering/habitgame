from tkinter  import *
from tkinter.ttk import *
from enum import Enum

# simple enum class for determining the Item type
class Type(Enum):
    hardware = 1
    component = 2
    software = 3
    food = 4
    money = 5

# Each item in the store is placed in an Item object
class Item():
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
    
class Shop():
    def __init__(self, shop_plugin_frame):
        """
            shop_plugin_frame is a frame reference that will contain the shop frame.
            This prevents adding more columns to the main GUI's column count
        """
        
        # store all items that can be bought in this list
        self.items = []
        
        # component items
        self.items.append(Item('motherboard', 'assets\\art\\mobo.png', Type.component, "motherboard description", 200, 0, 0))
        self.items.append(Item('ram 16gb', 'assets\\art\\ramred.png', Type.component, "ram 16gb description", 150, 0, 1))
        self.items.append(Item('ram 8gb', 'assets\\art\\ramgreen.png', Type.component, "ram 8gb description", 75, 0, 2))
        self.items.append(Item('cpu fan', 'assets\\art\\cpufan.png', Type.component, "cpu fan description", 50, 0, 3))
        self.items.append(Item('cpu 3.5 Ghz', 'assets\\art\\cpu.png', Type.component, "cpu 3.5 Ghz description", 300, 1, 0))
        self.items.append(Item('gpu 2gb', 'assets\\art\\gpured.png', Type.component, "gpu 2gb description", 300, 1, 1))
        self.items.append(Item('gpu 1gb', 'assets\\art\\gpugreen.png', Type.component, "gpu 1gb description", 150, 1, 2))

        # hardware items
        self.items.append(Item('laptop', 'assets\\art\\laptop.png', Type.hardware, "laptop description", 1250, 2, 0))
        self.items.append(Item('desktop', 'assets\\art\\desktop.png', Type.hardware, "desktop description", 2000, 2, 1))
        self.items.append(Item('terminal', 'assets\\art\\terminal.png', Type.hardware, "terminal description", 10000, 2, 2))
        self.items.append(Item('server', 'assets\\art\\server.png', Type.hardware, "server description", 5000, 2, 3))
        self.items.append(Item('desk', 'assets\\art\\desk.png', Type.hardware, "desk description", 500, 3, 0))
        
        # food items
        self.items.append(Item('cake', 'assets\\art\\cake.png', Type.food, "cake description", 15, 4, 0))
        self.items.append(Item('chicken', 'assets\\art\\chicken.png', Type.food, "chicken description", 10, 4, 1))
        self.items.append(Item('pizza', 'assets\\art\\pizza.png', Type.food, "pizza description", 20, 4, 2))
        self.items.append(Item('soda', 'assets\\art\\soda.png', Type.food, "soda description", 30, 4, 3))
        self.items.append(Item('popcorn', 'assets\\art\\popcorn.png', Type.food, "popcorn description", 5, 5, 0))

        # miscellaneous items
        self.items.append(Item('gold coins', 'assets\\art\\goldcoins.png', Type.money, "gold coins description", 50000, 6, 0))
        self.items.append(Item('change', 'assets\\art\\change.png', Type.money, "change description", 50, 6, 1))
        self.items.append(Item('dollars', 'assets\\art\\dollars.png', Type.money, "dollars description", 500, 6, 2))
        self.items.append(Item('money bag', 'assets\\art\\moneybag.png', Type.money, "money bag description", 2000, 6, 3))

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


        # selected item's name
        self.itemSelect = Label(shop_plugin_frame, text='name', padding=5)
        self.itemSelect.grid(sticky='news', row=1, columnspan=2)
        self.itemSelect.configure(font='arial 12')
        
        # selected item's description
        self.descriptSelect = Label(shop_plugin_frame, text='description', padding=5)
        self.descriptSelect.grid(sticky='news', row=2, columnspan=2)
        self.descriptSelect.configure(font='arial 12')
        
        # selected item's cost
        self.costSelect = Label(shop_plugin_frame, text='cost', padding=5)
        self.costSelect.grid(sticky='news', row=3, columnspan=2)
        self.costSelect.configure(font='arial 12')
        
        # create a 'buy' label to act as a button
        buy = Label(shop_plugin_frame, text='Buy', style='buy.TLabel', anchor='center', padding=5)
        buy.grid(sticky='news', row=4, columnspan=2)
        buy.bind('<Enter>', lambda e: self.style.configure('buy.TLabel', background='#0086D3'))
        buy.bind('<Leave>', lambda e: self.style.configure('buy.TLabel', background='#0086BF'))
        self.style.configure('buy.TLabel', background='#0086BF', font='arial 12 bold')
        
        self.createItems()

    
    """
        setItemInfo sets the info to be shown in the item
        information frame, right above the buy button
    """
    def setItemInfo(self, name, descript, cost):
        self.itemSelect.configure(text=name)
        self.descriptSelect.configure(text=descript)
        self.costSelect.configure(text=cost)

    def createItems(self):
        # loops through the list of items that need to be created and shown in the shop
        for row in range(len(self.items)):
            # prep appropriate data for when the user clicks on a item
            t_name = self.items[row].getName()
            t_descript = self.items[row].getDescription()
            t_cost = self.items[row].getCost()
            
            #create frame for item data
            item_frame = Frame(self.shopFrame, style='itemFrame.TFrame')
            item_frame.grid(row=self.items[row].getRow()+1, column=self.items[row].getColumn())
            self.style.configure('itemFrame.TFrame', background='white')
            # user clicks on the frame containing all of the item's info
            item_frame.bind('<1>', lambda e, name=t_name, descript = t_descript,
                            cost = t_cost, : self.setItemInfo(name, descript, cost))
            
            #create label to hold the item's image
            img = PhotoImage(file=self.items[row].getFile())
            new_item = Label(item_frame, image=img, style='item.TLabel')
            new_item.grid(row=0, column=0)
            new_item.image = img
            self.style.configure('item.TLabel', background='white')
            temp_str = self.items[row].getFile()
            # user clicks on the image of the item
            new_item.bind('<1>', lambda e, name=t_name, descript = t_descript,
                            cost = t_cost, : self.setItemInfo(name, descript, cost))        

            #create label to hold the item's cost
            new_cost = Label(item_frame, text='$'+str(self.items[row].getCost()), style='cost.TLabel')
            new_cost.grid(row=1, column=0)
            self.style.configure('cost.TLabel', font='arial 14', foreground='green', background='white')
            temp_str = self.items[row].getFile()
            # user clicks on the cost label
            new_cost.bind('<1>', lambda e, name=t_name, descript = t_descript,
                            cost = t_cost, : self.setItemInfo(name, descript, cost))
            
            #create label to hold the item's name
            new_desc = Label(item_frame, text=self.items[row].getName(), style='name.TLabel')
            new_desc.grid(row=2, column=0)
            self.style.configure('name.TLabel', font='arial 12', background='white')
            temp_str = self.items[row].getFile()
            new_desc.bind('<1>', lambda e, tstr=temp_str: self.itemSelect.configure(text=tstr))
            # user clicks on the label to hold the item's name
            new_desc.bind('<1>', lambda e, name=t_name, descript = t_descript,
                            cost = t_cost, : self.setItemInfo(name, descript, cost))
            
    
    def setupCanvasFrame(self, event):
        # resets the scroll region for the frame inserted into the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
