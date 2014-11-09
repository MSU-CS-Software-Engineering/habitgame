# MyInventory.setInventory(self.tab_inventory)

from tkinter import *
from tkinter.ttk import *
from hack_classes import Item
import os.path

class SetInventoryItem():
    """
    Store inventory item info, grid position, and character item reference
    """
    
    def __init__(self, name, file, description, effect, uses,
                 value, row, column, item_ref):
        self.name = name
        self.file = file
        self.description = description
        self.effect = effect
        self.uses = uses
        self.value = value
        self.row = row
        self.column = column
        self.item_ref = item_ref
        
    """"
    getter methods
    """
    
    def getName(self):
        return self.name

    def getFile(self):
        return self.file
    
    def getDescription(self):
        return self.description

    def getEffect(self):
        return self.effect

    def getUses(self):
        return self.uses

    def getValue(self):
        return self.value
    
    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column

    def getItemRef(self):
        return self.item_ref

    """
    setter methods
    """
    
    def setRow(self, row):
        self.row = row

    def setColumn(self, col):
        self.column = col
    

class MyInventory():
    """
    this class is used for link the Inventory class with the GUI class
    """
    
    api = None # reference to GUI class object
    my_inventory = None # Inventory class object stored here
    
    # called in work_space.py
    def setInventory(inventory_frame):
        MyInventory.my_inventory = Inventory(inventory_frame)

    # called at the end of engine/GUI's constructor function 
    def setApi(api_ref):
        MyInventory.api = api_ref
        MyInventory.my_inventory.setupInventory(MyInventory.api.get_character_items())

        
class Inventory():
    def __init__(self, inventory_plugin_frame):
        self.frame = inventory_plugin_frame
        
        self.items = [] # store all of the player's Item objects here
        #self.border_frames = [] # used for highlighting an item when the mouse hovers an item
        
        self.tool_tip = None
        self.character_items = None

        
    def setupInventory(self, char_items):
        row, col = 0, 0
        for item in char_items:
            self.items.append([SetInventoryItem(item.name, item.image, item.description, item.effect,
                                               item.uses, item.value, row, col, item), None])
            col += 1
            if col == 5: # max of 5 items in a row
                col = 0
                row += 1
   
        self.makeCanvas()
        self.createItems()


    def createItems(self):
        # loops through the list of items that need to be created and shown in the shop
        for i in range(len(self.items)):
            self.makeItemFrame(i)


    def addItem(self, item):
        if len(self.items) == 0:
            self.items.append([SetInventoryItem(item.name, item.image, item.description, item.effect,
                                           item.uses, item.value, 0, 0, item), None])
            self.makeItemFrame(0)
        else:
            # this function is called when a new item is purchased
            col = self.items[len(self.items)-1][0].getColumn() + 1
            row = self.items[len(self.items)-1][0].getRow()
        
            if col == 5: # max of 5 items in a row
                col = 0
                row += 1
                
            self.items.append([SetInventoryItem(item.name, item.image, item.description, item.effect,
                                           item.uses, item.value, row, col, item), None])
        
            self.makeItemFrame(len(self.items)-1)
            self.reposition()

        
    def makeItemFrame(self, i):
        # prep appropriate data for when the user clicks on a item
        t_name = self.items[i][0].getName()
        t_descript = self.items[i][0].getDescription()
        t_cost = self.items[i][0].getValue()


        # create frame border for item
        border_frame = Frame(self.inventoryFrame, padding=2, cursor='hand2', style='c.TFrame')
        border_frame.grid(row=self.items[i][0].getRow(), column=self.items[i][0].getColumn(),
                          padx=7, pady=7, sticky='wn')
        self.style.configure('c.TFrame', background='#EBEDF1')
        self.items[i][1] = border_frame
        
        # user clicks on the frame border
        border_frame.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                          self.setOptions(item_id, item_ref))
        border_frame.bind('<Enter>', lambda e, name=t_name, descript=t_descript, cost=t_cost,
                          item_id=i : self.setItemInfo(name, descript, cost, item_id,
                                                       self.items[i][0].getItemRef()))


        # create frame for item data
        item_frame = Frame(border_frame, style='itemFrame.TFrame', padding=4, cursor='hand2')
        item_frame.grid(sticky='wn')
        self.style.configure('itemFrame.TFrame', background='#EBEDF1')
        
        # user clicks on the frame containing all of the item's info
        item_frame.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                        self.setOptions(item_id, item_ref))
        item_frame.bind('<Enter>', lambda e, name=t_name, descript=t_descript, cost=t_cost,
                        item_id=i : self.setItemInfo(name, descript, cost, item_id,
                                                     self.items[i][0].getItemRef()))
        item_frame.bind('<Enter>', lambda e, _i=i: self.highlight(_i, True))
        item_frame.bind('<Leave>', lambda e, _i=i: self.highlight(_i, False))


        # create label to hold the item's image
        img = PhotoImage(file=self.items[i][0].getFile())
        new_item = Label(item_frame, padding=15, image=img, style='item.TLabel', cursor='hand2')
        new_item.grid(row=1, column=0)
        new_item.image = img
        self.style.configure('item.TLabel', background='#EBEDF1')
        
        # user clicks on the image of the item
        new_item.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                      self.setOptions(item_id, item_ref))
        new_item.bind('<Enter>', lambda e, name=t_name, descript = t_descript, cost=t_cost,
                      item_id=i : self.setItemInfo(name, descript, cost, item_id,
                                                   self.items[i][0].getItemRef()))


    def setOptions(self, item_id, item):
        print('yes')
        if self.items[item_id][1] != None:
            MyInventory.api.sell_item(item.ID)

            self.items[item_id][1].destroy()
            self.items[item_id][1] = None
        
            self.reposition()

        
    def setItemInfo(self, name, descript, cost, item_id, item):
        """
        setItemInfo sets the info to be shown in the item
        information frame, right above the buy button
        """
        self.itemSelect.configure(text=name)
        descript = "Info: " + descript
        self.descriptSelect.configure(text=descript)
        cost = "Cost: $" + str(cost)
        self.costSelect.configure(text=cost)
        self.buy_item_id = item_id


    def reposition(self):
        """
        repositions all items in the inventory once a item is removed or added
        """
        # self.inv_canvas.winfo_width()
        # self.items[i][1].winfo_width()
        _row, _col = 0, 0
        for i in range(len(self.items)):
            if self.items[i][1] != None:
                self.items[i][0].setRow(_row)
                self.items[i][0].setColumn(_col)
                self.items[i][1].grid(row=_row, column=_col)
                
                _col += 1
                if _col == 5:
                    _col = 0
                    _row += 1


    def highlight(self, i, enter):
        # this loop is needed to prevent all item border frames from becoming highlighted
        for j in range(len(self.items)):
            if self.items[j][1] != None:
                self.items[j][1].config(style='a.TFrame')
                self.style.configure('a.TFrame', background='#EBEDF1')

        if self.items[i][1] != None:
            self.items[i][1].config(style='b.TFrame')
            if enter: # mouse enter
                self.style.configure('b.TFrame', background='#26507D')
            else: # mouse leave
                self.style.configure('b.TFrame', background='#EBEDF1')
                
        
    def makeCanvas(self):
        # create a canvas to allow for scrolling of the shop Frame
        self.inv_canvas = Canvas(self.frame, highlightthickness=0, background='#EBEDF1')
        self.inv_canvas.grid(row=3, column=0, sticky='news')

        # create the shop frame and place it inside the canvas
        self.inventoryFrame = Frame(self.inv_canvas, borderwidth=0, style='inventoryFrame.TFrame', padding=10) 
        self.inventoryFrame.grid(sticky='news')
        
        self.scrollBar = Scrollbar(self.frame, orient="vertical", command=self.inv_canvas.yview)
        self.inv_canvas.configure(yscrollcommand=self.scrollBar.set)
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        
        self.inv_canvas.create_window((0,0), window=self.inventoryFrame,
                                      anchor='nw', tags='self.inventoryFrame')
        self.scrollBar.grid(row=0, column=1, rowspan=4, sticky='ns')
        
        def setupCanvasFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            self.inv_canvas.configure(scrollregion=self.inv_canvas.bbox("all"))
            
        self.inventoryFrame.bind("<Configure>", setupCanvasFrame)

        self.style = Style()
        self.style.configure('inventoryFrame.TFrame', background='#EBEDF1')

        def scroll_m(event):
            """ allows for mouse wheel scrolling """
            try:
                self.inv_canvas.yview_scroll(-1 * int(event.delta/120), "units")
            except:
                pass

        self.inv_canvas.bind("<MouseWheel>", lambda e: scroll_m(e))
        self.inv_canvas.bind("<Configure>", lambda e: self.reposition())
        
        # selected item's name
        self.itemSelect = Label(self.frame, text='name', padding='10 5 5 5')
        self.itemSelect.grid(sticky='news', row=0)
        self.itemSelect.configure(font='arial 14 bold', foreground='#FFD237', background='#1E1E1E')
        
        # selected item's description
        self.descriptSelect = Label(self.frame, text='description', padding='10 5 5 5')
        self.descriptSelect.grid(sticky='news', row=1)
        self.descriptSelect.configure(font='arial 12 bold', foreground='white', background='#444444')
        
        # selected item's cost
        self.costSelect = Label(self.frame, text='cost', padding='10 5 5 5')
        self.costSelect.grid(sticky='news', row=2)
        self.costSelect.configure(font='arial 12 bold', foreground='white', background='#444444')
