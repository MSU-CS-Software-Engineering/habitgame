from datetime import date, timedelta #For Timestamps

class Character:
    """
      Class for Habit character profile

      Variables:
        name: Name of character       (string)
        cash: Total currency          (int)
        exp: Total experience points  (int)
        level: Current level          (int)
        habits: Current habits        (list of Habit objects)
        tasks:                        (list of Task objects)
        dailies:                      (list of Daily objects)
        items: Owned (soft|hard)ware  (list of Item objects)
    """
    def __init__(self, name):
        self.hack_index = 0
        self.name = name
        self.cash = 0
        self.exp = 0
        self.level = 1
        self.hacks = {}
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
                          'hacks': None,
                          'items': None}

        hacks_list = []
        items_list = []
        
        for hack in self.hacks.values():
            hacks_list.append(hack.serialize())

        for item in self.items:
            items_list.append(item.serialize())

        character_dict['hacks'] = hacks_list
        character_dict['items'] = items_list
        
        return character_dict

    def add_hack(self, hack):
        if hack.ID == -1:
            hack.ID = self.hack_index
        self.hacks[hack.ID] = hack
        self.hack_index = max(self.hacks.keys()) + 1
        return hack.ID

    def edit_hack(self, hack_ID, hack):
        try:
            self.remove_hack(hack_ID)
            hack.ID = hack_ID
            self.add_hack(hack)
            return True
        except:
            print("Edit failed!")
            return False

    def remove_hack(self, hack_ID):
        try:
            del self.hacks[hack_ID]
            return True
        except:
            print("Invalid hack id!")
            return False

    def complete_hack(self, hack_ID):
        hack = self.get_hack(hack_ID)

        if hack.h_type == "daily":
            if hack.timestamp < date.today():
                self.hacks[hack_id].timestamp = date.today()
            else:
                return False

        elif hack.h_type == "task":
            self.remove_hack(hack_ID)

        if int(hack.value) > 0:
            self.exp += int(hack.exp)

        self.cash += int(hack.value)
        
        if hack.h_type == "habit":
            return False

        return True

    def get_hack(self, hack_ID):
        try:
            hack = self.hacks[hack_ID]
            return hack
        except:
            print("Error: Invalid hack id")

    def show_hacks(self):
        for hack in self.hacks:
            self.show_hack(hack.ID)

    def add_item(self, item):
        if len(self.items) != 0:
            item.ID = len(self.items)
        
        self.items.append(item)
        return item.ID

    def remove_item(self, item_ID):
        try:
            item_id = self.items.pop(item_ID).ID
            self.set_item_IDs()
            return item_id
        except:
            print("Invalid item id!")
            return False

    def get_item(self, item_ID):
        try:
            item = self.items[item_ID]
            return self.items[item_ID]
        except:
            print("Error: Invalid item ID")
            
    def get_all_items(self):
        return self.items
    
    def set_item_IDs(self):
        for item in enumerate(self.items):
            item[1].ID = item[0]
 
    def show_items(self):
        for item in self.items:
            self.show_item(item.ID)

class Hack:
    """
      Class for Individual Hacks (Habits, dailies, and goals)

      Variables:
        h_type: Type of hack (habit, daily, goal)    (string)
        title: Name of hack                          (string)
        description: Short description of hack       (string) 
        ID: Number to hold index in                  (int)
        timestamp: Last-accessed date                (date)
        value: Cash reward/penalty                   (int)
        exp: Experience point value                  (int)
    """
    def __init__(self, h_type, title, desc, value, exp = 100 ):
        self.h_type = h_type
        self.title = title
        self.description = desc
        self.ID = -1
        self.timestamp = date.today() - timedelta(hours=24)
        self.value = value
        self.exp = exp    #Temporarily defaults to 100.

    def serialize(self):
        """
        Serializes class properties to a dictionary 
        which can be converted to a string
        """
        hack_dict = {
                      'h_type':self.h_type,
                      'title':self.title,
                      'desc':self.description,
                      'ID'  :self.ID,
                      'timestamp':str(self.timestamp),
                      'value':self.value,
                      'exp':self.exp
                     }
        
        return hack_dict
    
    def get_hack_type(self):
        return self.h_type
    
class Item:
    """
      Class for purchasable software/hardware

      Variables:
        name: Name of item                                (string)
        ID: Number to hold index in itemlist              (int)
        description: Text about what the item does        (string)
        image: Name of accompanying image                 (string)
        value: Currency value of item                     (int)
        uses: Uses before item expires [-1 for infinite]  (int)
        item_type: 'hardware', 'component', 'software'    (string)
        active: Is the item in use or not                 (bool)
        effect: Special function that the item performs   (function)
    """
    def __init__(self, name, desc, image, value, uses, item_type, active, effect = None):
        self.name = name
        self.ID = 0
        self.description = desc
        self.image = image
        self.value = value
        self.uses = uses
        self.item_type = item_type
        self.active = active
        self.effect = effect

    def serialize(self):
        """
        Serializes class properties to a dictionary
        which can be converted to a string
        """
        item_dict = {'title':self.name,
                      'ID':self.ID,
                     'desc':self.description,
                      'image':self.image,
                      'value':self.value,
                      'uses':self.uses,
                      'item_type':self.item_type,
                      'effect':self.effect,
                      'active':self.active}
        
        return item_dict
