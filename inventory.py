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
        MyInventory.my_inventory.initInventory(MyInventory.api.get_character_items())

        
class Inventory():
    def __init__(self, inventory_plugin_frame):
        self.frame = inventory_plugin_frame
        self.canvas_color = '#EBEDF1'
        
        self.items = [] # store all of the player's Item objects here
        
        self.selceted_item_id = None
        self.selected_item_ref = None
        self.item_set = False
        
    def initInventory(self, char_items):
        row, col = 0, 0
        for item in char_items:
            self.items.append([SetInventoryItem(item.name, item.image, item.description, item.effect,
                                                item.uses, item.value, row, col, item), None])
            col += 1
            if col == 5: # max of 5 items in a row
                col = 0
                row += 1
   
        self.makeLayout()
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
        self.style.configure('c.TFrame', background=self.canvas_color)
        self.items[i][1] = border_frame
        
        # user clicks on the frame border
        border_frame.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                          self.selectItem(item_id, item_ref))
        border_frame.bind('<Enter>', lambda e, name=t_name, descript=t_descript, cost=t_cost,
                          item_id=i : self.setItemInfo(name, descript, cost, item_id,
                                                       self.items[i][0].getItemRef()))


        # create frame for item data
        item_frame = Frame(border_frame, style='itemFrame.TFrame', padding=4, cursor='hand2')
        item_frame.grid(sticky='wn')
        self.style.configure('itemFrame.TFrame', background=self.canvas_color)
        
        # user clicks on the frame containing all of the item's info
        item_frame.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                        self.selectItem(item_id, item_ref))
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
        self.style.configure('item.TLabel', background=self.canvas_color)
        
        # user clicks on the image of the item
        new_item.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                      self.selectItem(item_id, item_ref))
        new_item.bind('<Enter>', lambda e, name=t_name, descript = t_descript, cost=t_cost,
                      item_id=i : self.setItemInfo(name, descript, cost, item_id,
                                                   self.items[i][0].getItemRef()))


    def remove_selected_item(self):
        """
        remove the item from the panel on the right side of the inventory
        """
        self.selectedItem.image = None
        self.selectedItem.destroy()
        self.selectedItemFrame.destroy()

        
    def remove_item_from_inventory(self, item_id):
        self.remove_selected_item()
        self.items[item_id][1].destroy()
        self.items[item_id][1] = None
        self.reposition()
        self.item_set = False

        
    def selectItem(self, item_id, item):
        """
        called when the user clicks on an item in the inventory panel.
        The item is prepped for the item manager panel on the right side of the GUI
        """
        # currently selected item is reset when the user selects a new item
        if self.item_set and self.selected_item_ref != item:
            self.remove_selected_item()

        # make sure the item has not been deleted or used
        if self.items[item_id][1] != None and self.selected_item_ref != item:
            # selected item info goes in this frame
            self.selectedItemFrame = Frame(self.item_info_frame, borderwidth=0, style='select.TFrame')
            self.selectedItemFrame.grid(row=2, columnspan=2, sticky='news')
            self.selectedItemFrame.grid_columnconfigure(1, weight=1)
            self.style.configure('select.TFrame', background='#B4B4B4')

            # selected item stored here
            self.selectedItem = Label(self.selectedItemFrame, padding='10 5 5 5')
            self.selectedItem.grid(row=0, columnspan=2, sticky='news')
            self.selectedItem.grid_columnconfigure(1, weight=1)
            img = PhotoImage(file=self.items[item_id][0].getFile())
            self.selectedItem.configure(text='  Item ID: ' + str(item_id), image=img,
                                        compound = 'left', font='arial 12 bold italic',
                                        foreground='black', background='#FCE081', padding='10 5 5 5')
            self.selectedItem.image = img

            self.selceted_item_id = item_id
            self.selected_item_ref = item

            self.item_set = True

            
    def sellItem(self, item_id, item):
        if item_id != None:  
            if self.items[item_id][1] != None:
                MyInventory.api.sell_item(item.ID)
                self.remove_item_from_inventory(item_id)

        
    def useItem(self, item_id, item):
        if item_id != None:
            if self.items[item_id][1] != None:
                MyInventory.api.use_item(item.ID)
                self.remove_item_from_inventory(item_id)

            
    def setItemInfo(self, name, descript, cost, item_id, item):
        """
        setItemInfo sets the info to be shown in the item
        information frame, right above the buy button
        """
        self.nameSelect.configure(text=name)
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
                self.style.configure('a.TFrame', background=self.canvas_color)

        if self.items[i][1] != None:
            self.items[i][1].config(style='b.TFrame')
            if enter: # mouse enter
                self.style.configure('b.TFrame', background='#26507D')
            else: # mouse leave
                self.style.configure('b.TFrame', background=self.canvas_color)

                
    def makeCanvas(self):
        # create a canvas to allow for scrolling of the shop Frame
        self.inv_canvas = Canvas(self.frame, highlightthickness=0, background=self.canvas_color)
        self.inv_canvas.grid(row=1, column=0, sticky='news')

        # create the inventory frame and place it inside the canvas
        self.inventoryFrame = Frame(self.inv_canvas, borderwidth=0,
                                    style='inventoryFrame.TFrame', padding=10) 
        self.inventoryFrame.grid(sticky='news')
        
        self.scrollBarY = Scrollbar(self.frame, orient="vertical", command=self.inv_canvas.yview)
        self.scrollBarX = Scrollbar(self.frame, orient="horizontal", command=self.inv_canvas.xview)
        self.inv_canvas.configure(yscrollcommand=self.scrollBarY.set,
                                  xscrollcommand=self.scrollBarX.set)
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        self.inv_canvas.create_window((0,0), window=self.inventoryFrame,
                                      anchor='nw', tags='self.inventoryFrame')
        self.scrollBarY.grid(row=1, column=1, rowspan=2, sticky='ns')
        self.scrollBarX.grid(row=3, column=0, columnspan=1, sticky='we')
        
        def setupCanvasFrame(event):
            # resets the scroll region for the frame inserted into the canvas
            self.inv_canvas.configure(scrollregion=self.inv_canvas.bbox("all"))
            
        self.inventoryFrame.bind("<Configure>", setupCanvasFrame)

        self.style = Style()
        self.style.configure('inventoryFrame.TFrame', background=self.canvas_color)

        def scroll_m(event):
            """ allows for mouse wheel scrolling """
            try:
                self.inv_canvas.yview_scroll(-1 * int(event.delta/120), "units")
            except:
                pass

        self.inv_canvas.bind("<MouseWheel>", lambda e: scroll_m(e))


    def makeLayout(self):
        # Inventory title
        self.invTitle = Label(self.frame, text='My Inventory', padding='10 5 5 5')
        self.invTitle.grid(sticky='news', row=0, columnspan=3)
        self.invTitle.configure(font='arial 14 bold', foreground='#FFD237', background='#1E1E1E')
        
        self.makeCanvas()
        
        self.item_info_frame = Frame(self.frame, borderwidth=0)
        self.item_info_frame.grid(row=1, column=2, rowspan=3, sticky='news')
        self.item_info_frame.grid_columnconfigure(2, weight=1)
        self.item_info_frame.grid_rowconfigure(3, weight=1)
        
        # inventory panel title
        self.panelTitle = Label(self.item_info_frame, text='Item Manager',
                                anchor=CENTER, width=32, padding='10 5 5 5')
        self.panelTitle.grid(sticky='news', row=0, columnspan=2)
        self.panelTitle.configure(font='arial 16 bold italic', foreground='#F5F5F5', background='#282828')

        # sell item button
        self.sellButton = Label(self.item_info_frame, text='sell', padding='10 5 5 5', cursor='hand2')
        self.sellButton.grid(sticky='news', row=1, column=0)
        self.sellButton.configure(font='arial 14 bold', anchor=CENTER,
                                  foreground='white', background='#3E710F')
        self.sellButton.bind('<1>', lambda e: self.sellItem(self.selceted_item_id, self.selected_item_ref))
        self.sellButton.bind('<Enter>', lambda e: self.sellButton.configure(background='#5CA916'))
        self.sellButton.bind('<Leave>', lambda e: self.sellButton.configure(background='#3E710F'))
                             
        # use item button
        self.useButton = Label(self.item_info_frame, text='use', padding='10 5 5 5', cursor='hand2')
        self.useButton.grid(sticky='news', row=1, column=1)
        self.useButton.configure(font='arial 14 bold', anchor=CENTER,
                                 foreground='white', background='#710F0F')
        self.useButton.bind('<1>', lambda e: self.useItem(self.selceted_item_id, self.selected_item_ref))
        self.useButton.bind('<Enter>', lambda e: self.useButton.configure(background='#C61A1A'))
        self.useButton.bind('<Leave>', lambda e: self.useButton.configure(background='#710F0F'))

        panel_color_bg = '#E8E2D0'
        
        item_info_div = Frame(self.item_info_frame, borderwidth=0, style='Info.TFrame')
        item_info_div.grid(row=3, columnspan=2, sticky='news')
        self.style.configure('Info.TFrame', background=panel_color_bg)

        # item's name
        self.nameSelect = Label(item_info_div, text='name', width=30, padding='10 10 5 5')
        self.nameSelect.grid(sticky='news', row=0, columnspan=2)
        self.nameSelect.configure(font='arial 12 bold', foreground='black', background=panel_color_bg)
        
        # selected item's cost
        self.costSelect = Label(item_info_div, text='cost', padding='10 5 5 5')
        self.costSelect.grid(sticky='news', row=1, columnspan=2)
        self.costSelect.configure(font='arial 12 bold', foreground='black', background=panel_color_bg)
        
        # selected item's description
        self.descriptSelect = Label(item_info_div, text='description', wraplength=370, padding='10 5 5 5')
        self.descriptSelect.grid(sticky='news', row=2, columnspan=2)
        self.descriptSelect.configure(font='arial 12 bold', foreground='black', background=panel_color_bg)
        self.descriptSelect.grid_columnconfigure(1, weight=1)

