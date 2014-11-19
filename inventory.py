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
                 value, item_type, active, row, column, item_ref):
        self.name = name
        self.file = file
        self.description = description
        self.effect = effect
        self.uses = uses
        self.value = value
        self.item_type = item_type
        self.row = row
        self.column = column
        self.item_ref = item_ref
        self.active = active
        
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

    def getItemType(self):
        return self.item_type
    
    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column

    def getItemRef(self):
        return self.item_ref

    def getActive(self):
        return self.active

    """
    setter methods
    """
    
    def setUses(self, uses):
        self.uses = uses

    def setActive(self, active):
        self.active = active
        
    def setRow(self, row):
        self.row = row

    def setColumn(self, col):
        self.column = col
    

class MyInventory():
    """
    this class is used for linking the Inventory class with the GUI
    class before creating the Inventory class object
    """
    
    api = None # reference to GUI class object
    items_frame = None # reference to GUI class items in use frame
    my_inventory = None # Inventory class object stored here

    # default active item limits
    max_software = 5
    max_hardware = 3 
    max_components = 2

    # current number of items active 
    software_count = 0
    hardware_count = 0
    components_count = 0

    # store each active item info here
    software = []
    software_items = []
    
    hardware = []
    hardware_items = []
    
    components = []
    component_items = []
    
    # called in work_space.py
    def setInventory(inventory_frame):
        MyInventory.my_inventory = Inventory(inventory_frame)

    # called at the end of engine/GUI's constructor function 
    def setApi(api_ref, items_frame_ref):
        MyInventory.api = api_ref
        MyInventory.items_frame = items_frame_ref
        MyInventory.makeItemSlots()
        MyInventory.my_inventory.initInventory(MyInventory.api.get_character_items())
  
    def makeItemSlots():
        style = Style()
        for i in range(MyInventory.max_software):
            software_frame = Frame(MyInventory.items_frame, width=25, height=25, style='item.TFrame')
            software_frame.grid(row=1, column=i+1, sticky=W, pady=4, padx=5)
            style.configure('item.TFrame', background='#AEAEAE')
            MyInventory.software.append(software_frame)
            MyInventory.software_items.append([None, None])

        for i in range(MyInventory.max_hardware):
            hardware_frame = Frame(MyInventory.items_frame, width=25, height=25, style='item.TFrame')
            hardware_frame.grid(row=2, column=i+1, sticky=W, pady=4, padx=5)
            style.configure('item.TFrame', background='#AEAEAE')
            MyInventory.hardware.append(hardware_frame)
            MyInventory.hardware_items.append([None, None])
            
        for i in range(MyInventory.max_components):
            component_frame = Frame(MyInventory.items_frame, width=25, height=25, style='item.TFrame')
            component_frame.grid(row=3, column=i+1, sticky=W, pady=4, padx=5)
            style.configure('item.TFrame', background='#AEAEAE')
            MyInventory.components.append(component_frame)
            MyInventory.component_items.append([None, None])
   
    def addSoftware(item):
        if MyInventory.software_count < MyInventory.max_software:
            i = MyInventory.software_count
            
            software_label = Label(MyInventory.software[MyInventory.software_count], text=item.name)
            software_label.grid(sticky=W)
            software_label.configure(font='arial 14', background='red', foreground='black')
            
            software_label.bind('<1>', lambda e, _id=i: MyInventory.removeSoftware(_id, item))
            MyInventory.software_items[MyInventory.software_count] = [software_label, item]
        
            MyInventory.software_count += 1
            return True
        else:
            return False # software slots full

    def resetSoftware(item, i):
        software_label = Label(MyInventory.software[i-1], text=item.name)
        software_label.grid(sticky=W)
        software_label.configure(font='arial 14', background='red', foreground='black')
            
        software_label.bind('<1>', lambda e, _id=i-1: MyInventory.removeSoftware(_id, item))
        MyInventory.software_items[i-1] = [software_label, item]
        
    def removeSoftware(_id, item):
        if MyInventory.software_items[_id][0] != None:
            MyInventory.software_items[_id][0].destroy()
            MyInventory.software_items[_id][0] = None
            MyInventory.my_inventory.addItem(MyInventory.software_items[_id][1])
            
            for i in range(_id+1, MyInventory.max_software, 1):
                if MyInventory.software_items[i][0] != None:
                    MyInventory.resetSoftware(MyInventory.software_items[i][1], i)
                    MyInventory.software_items[i][0].destroy()
                    MyInventory.software_items[i][0] = None
                    
            if MyInventory.software_count > 0:
                MyInventory.software_count -= 1
                
            MyInventory.api.remove_effect(item)

    def addHardware(item):
        if MyInventory.hardware_count < MyInventory.max_hardware:
            i = MyInventory.hardware_count
            
            hardware_label = Label(MyInventory.hardware[MyInventory.hardware_count], text=item.name)
            hardware_label.grid(sticky=W)
            hardware_label.configure(font='arial 14', background='yellow', foreground='black')
            
            hardware_label.bind('<1>', lambda e, _id=i: MyInventory.removeHardware(_id, item))
            MyInventory.hardware_items[MyInventory.hardware_count] = [hardware_label, item]
        
            MyInventory.hardware_count += 1
            return True
        else:
            return False # software slots full

    def resetHardware(item, i):
        hardware_label = Label(MyInventory.hardware[i-1], text=item.name)
        hardware_label.grid(sticky=W)
        hardware_label.configure(font='arial 14', background='yellow', foreground='black')
            
        hardware_label.bind('<1>', lambda e, _id=i-1: MyInventory.removeHardware(_id, item))
        MyInventory.hardware_items[i-1] = [hardware_label, item]
        
    def removeHardware(_id, item):
        if MyInventory.hardware_items[_id][0] != None:
            MyInventory.hardware_items[_id][0].destroy()
            MyInventory.hardware_items[_id][0] = None
            MyInventory.my_inventory.addItem(MyInventory.hardware_items[_id][1])

            for i in range(_id+1, MyInventory.max_hardware, 1):
                if MyInventory.hardware_items[i][0] != None:
                    MyInventory.resetHardware(MyInventory.hardware_items[i][1], i)
                    MyInventory.hardware_items[i][0].destroy()
                    MyInventory.hardware_items[i][0] = None
                    
            if MyInventory.hardware_count > 0:
                MyInventory.hardware_count -= 1
                
            MyInventory.api.unequipe_item(item)
    
    def addComponent(item):
        if MyInventory.components_count < MyInventory.max_components:
            i = MyInventory.components_count
            
            component_label = Label(MyInventory.components[MyInventory.components_count], text=item.name)
            component_label.grid(sticky=W)
            component_label.configure(font='arial 14', background='blue', foreground='black')
            
            component_label.bind('<1>', lambda e, _id=i: MyInventory.removeComponent(_id))
            MyInventory.component_items[MyInventory.components_count] = [component_label, item]
        
            MyInventory.components_count += 1
            return True
        else:
            return False # software slots full

    def resetComponent(item, i):
        component_label = Label(MyInventory.components[i-1], text=item.name)
        component_label.grid(sticky=W)
        component_label.configure(font='arial 14', background='blue', foreground='black')
            
        component_label.bind('<1>', lambda e, _id=i-1: MyInventory.removeComponent(_id))
        MyInventory.component_items[i-1] = [component_label, item]
        
    def removeComponent(_id):
        if MyInventory.component_items[_id][0] != None:
            MyInventory.component_items[_id][0].destroy()
            MyInventory.component_items[_id][0] = None
            MyInventory.my_inventory.addItem(MyInventory.component_items[_id][1])
            
            for i in range(_id+1, MyInventory.max_components, 1):
                if MyInventory.component_items[i][0] != None:
                    MyInventory.resetComponent(MyInventory.component_items[i][1], i)
                    MyInventory.component_items[i][0].destroy()
                    MyInventory.component_items[i][0] = None
                    
            if MyInventory.components_count > 0:
                MyInventory.components_count -= 1
                
            MyInventory.api.unequipe_item(item)
 
class Inventory():
    def __init__(self, inventory_plugin_frame):
        self.frame = inventory_plugin_frame
        self.canvas_color = '#EBEDF1'
        
        self.items = [] # store all of the player's Item objects here
        
        self.selceted_item_id = None
        self.selected_item_ref = None
        self.item_set = False

        # used for visually updating the use count under each item object/image
        self.uses_labels = []
        
        
    def initInventory(self, char_items):
        row, col = 0, 0
        for item in char_items:
            # item does not need to be added to the inventory since it's active
            if item.active == 'True': # item.active is a string
                item_type = item.item_type
                # add to active item frame
                if item_type == 'software':
                    MyInventory.addSoftware(item)
                elif item_type == 'hardware':
                    MyInventory.addHardware(item)
                elif item_type == 'component':
                    MyInventory.addComponent(item)
            else:
                self.items.append([SetInventoryItem(item.name, item.image, item.description, item.effect,
                                                    item.uses, item.value, item.item_type, item.active,
                                                    row, col, item), None])

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
                                                item.uses, item.value, item.item_type, item.active,
                                                0, 0, item), None])
            self.makeItemFrame(0)
        else:
            # this function is called when a new item is purchased
            col = self.items[len(self.items)-1][0].getColumn() + 1
            row = self.items[len(self.items)-1][0].getRow()
            
            if col == 5: # max of 5 items in a row
                col = 0
                row += 1
                    
            self.items.append([SetInventoryItem(item.name, item.image, item.description, item.effect,
                                                item.uses, item.value, item.item_type, item.active,
                                                row, col, item), None])
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

        # Important step. This refer ence is used to visually delete the item from the inventory
        self.items[i][1] = border_frame
        
        # user clicks on the frame border
        border_frame.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                          self.selectItem(item_id, item_ref))
        border_frame.bind('<Enter>', lambda e, name=t_name, descript = t_descript, cost=t_cost :
                          self.setItemInfo(name, descript, self.items[i][0].getUses(), cost))


        # create frame for item data
        item_frame = Frame(border_frame, style='itemFrame.TFrame', padding=9, cursor='hand2')
        item_frame.grid(sticky='wn')
        self.style.configure('itemFrame.TFrame', background=self.canvas_color)
        
        # user clicks on the frame containing all of the item's info
        item_frame.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                        self.selectItem(item_id, item_ref))
        item_frame.bind('<Enter>', lambda e, name=t_name, descript = t_descript, cost=t_cost :
                        self.setItemInfo(name, descript, self.items[i][0].getUses(), cost))
        item_frame.bind('<Enter>', lambda e, _i=i: self.highlight(_i, True))
        item_frame.bind('<Leave>', lambda e, _i=i: self.highlight(_i, False))
        

        # create label to hold the item's image
        img = PhotoImage(file=self.items[i][0].getFile())
        new_item = Label(item_frame, padding=10, image=img, style='item.TLabel', cursor='hand2')
        new_item.grid(row=1, column=0)
        new_item.image = img
        self.style.configure('item.TLabel', background=self.canvas_color)
        
        # user clicks on the image of the item
        new_item.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                      self.selectItem(item_id, item_ref))
        new_item.bind('<Enter>', lambda e, name=t_name, descript = t_descript, cost=t_cost :
                      self.setItemInfo(name, descript, self.items[i][0].getUses(), cost))

        # create dynamic label for displaying the number of uses remaining for the given item
        str_uses = StringVar()
        str_uses.set("uses: " + str(self.items[i][0].getUses()))
        uses_label = Label(item_frame, textvariable=str_uses, anchor=CENTER, foreground='#646464',
                     background=self.canvas_color, font='arial 10 bold italic')
        uses_label.grid(row=2, column=0, sticky='news')
        uses_label.bind('<1>', lambda e, item_id=i, item_ref=self.items[i][0].getItemRef():
                        self.selectItem(item_id, item_ref))
        self.uses_labels.append([str_uses, uses_label])
        
    def remove_selected_item(self):
        """
        remove the item from the panel on the
        right side of the inventory
        """
        self.selectedItem.image = None
        self.selectedItem.destroy()
        self.selectedItemFrame.destroy()

        
    def remove_item_from_inventory(self, item_id):
        """
        remove the selected item from the inventory
        on both sell and use commands
        """
        self.remove_selected_item()
        self.items[item_id][1].destroy()
        self.items[item_id][1] = None
        self.reposition()
        self.item_set = False

        
    def selectItem(self, item_id, item):
        """
        called when the user clicks on an item in the
        inventory panel. The item is prepped for the
        item manager panel on the right side of the GUI
        """
        # currently selected item is reset when the user selects a new item
        if self.item_set:
            self.remove_selected_item()

        # make sure the item has not been deleted or used
        if self.items[item_id][1] != None:
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
                MyInventory.api.sell_item(item)
                self.remove_item_from_inventory(item_id)
                
                self.selceted_item_id = None
                self.selected_item_ref = None
                self.resetItemInfo()

        
    def useItem(self, item_id, item):
        if item_id != None:
            if self.items[item_id][1] != None:
                not_full = True
                item_type = item.component

                if item_type == 'software':
                    if item.item_type != 'smokescreen':
                        item.active = True
                        not_full = MyInventory.addSoftware(item)
                elif item_type == 'hardware':
                    item.active = True
                    not_full = MyInventory.addHardware(item)
                elif item_type == 'component':
                    item.active = True
                    not_full = MyInventory.addComponent(item)

                # item slot not full, so add the item to the active items area of the GUI
                if not_full:   
                    new_uses = int(self.items[item_id][0].getUses()) - 1
                    self.items[item_id][0].setUses(str(new_uses))
                    self.uses_labels[item_id][0].set("uses: " + self.items[item_id][0].getUses())
                    
                    MyInventory.api.use_item(item)
                    self.remove_item_from_inventory(item_id)
                        
                    self.selceted_item_id = None
                    self.selected_item_ref = None
                    self.remove_selected_item()
                    self.resetItemInfo()
                else:
                    item.active = False


    def resetItemInfo(self):
        self.nameSelect.configure(text='name')
        self.descriptSelect.configure(text='description')
        self.useSelect.configure(text='uses')
        self.costSelect.configure(text='cost')

        
    def setItemInfo(self, name, descript, uses, cost):
        """
        setItemInfo sets the info to be shown in the item
        information frame, right above the buy button
        """
        name = "Name: " + name
        self.nameSelect.configure(text=name)
        descript = "Info: " + descript
        self.descriptSelect.configure(text=descript)
        uses = "Uses: " + str(uses)
        self.useSelect.configure(text=uses)
        cost = "Cost: $" + str(cost)
        self.costSelect.configure(text=cost)


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
                self.uses_labels[i][1].configure(foreground='#323232')
            else: # mouse leave
                self.style.configure('b.TFrame', background=self.canvas_color)
                self.uses_labels[i][1].configure(foreground='#646464')

                
    def makeCanvas(self):
        # create a canvas to allow for scrolling of the shop Frame
        self.inv_canvas = Canvas(self.frame, highlightthickness=0, borderwidth=0, background=self.canvas_color)
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
                                 foreground='white', background='#0F5A71')
        self.useButton.bind('<1>', lambda e: self.useItem(self.selceted_item_id, self.selected_item_ref))
        self.useButton.bind('<Enter>', lambda e: self.useButton.configure(background='#1795B9'))
        self.useButton.bind('<Leave>', lambda e: self.useButton.configure(background='#0F5A71'))

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

        # selected item's number of uses
        self.useSelect = Label(item_info_div, text='uses', padding='10 5 5 5')
        self.useSelect.grid(sticky='news', row=2, columnspan=2)
        self.useSelect.configure(font='arial 12 bold', foreground='black', background=panel_color_bg)
        
        # selected item's description
        self.descriptSelect = Label(item_info_div, text='description', wraplength=370, padding='10 5 5 5')
        self.descriptSelect.grid(sticky='news', row=3, columnspan=2)
        self.descriptSelect.configure(font='arial 12 bold', foreground='black', background=panel_color_bg)
        self.descriptSelect.grid_columnconfigure(1, weight=1)

