from datetime import date, timedelta #For Timestamps
import time
from math import *
class Character:
    """
      Class for Habit character profile

      Variables:
        name: Name of character       (string)
        cash: Total currency          (int)
        exp: Total experience points  (int)
        level: Current level          (int)
        Attack Multiplier: Damage modifier to bosses: (float)
        hacks: Current hacks          (list of Hack objects)
        items: Owned (soft|hard)ware  (list of Item objects)
    """
    def __init__(self, name, parent):
        self.parent = parent
        self.hack_index = 0
        self.name = name
        self.cash = 0
        self.exp = 0
        self.level = 1
        self.hacks = {}
        self.items = []
        self.effects = {}
        self.equipped = {}

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
                          'items': None }

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
        hack_limit = 4
        if 'RAM' in self.equipped:
            hack_limit = self.equipped['RAM'].effect
        if len(self.hacks) < hack_limit:
            if hack.ID == -1:
                hack.ID = self.hack_index
            self.hacks[hack.ID] = hack
            self.hack_index = max(self.hacks.keys()) + 1
            return True
        
        return False

    def edit_hack(self, hack_ID, hack):
        try:
            self.remove_hack(hack_ID)
            hack.ID = hack_ID
            self.add_hack(hack)
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

    def complete_hack(self, hack_ID, current_date = 'P_DATE'):
        if current_date == 'P_DATE':
            current_date = self.parent.current_date
            
        hack = self.get_hack(hack_ID)
        
        value_mult = 1
        exp_mult = 1
        if 'motherboard' in self.equipped:
            exp_mult *= self.equipped['motherboard'].effect
        if 'GPU' in self.equipped:
            value_mult *= self.equipped['GPU'].effect
        if 'fork' in self.effects:
            value_mult *= self.effects['fork'].effect
        if 'penetrate' in self.effects:
            value_mult /= self.effects['penetrate'].effect   
 
        if hack.h_type == "daily":
            if hack.timestamp < self.parent.current_date:
                self.hacks[hack_ID].timestamp = self.parent.current_date

            else:
                #self.remove_hack(hack_ID)
                return False

        elif hack.h_type == "task":
            self.remove_hack(hack_ID)

        if int(hack.value) > 0:
            self.exp += ceil(float(hack.exp) * exp_mult)

        self.cash += ceil(float(hack.value) * value_mult)

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

    def use_item(self, item):
        self.items[item.ID].uses = str(int(self.items[item.ID].uses) - 1)
        if self.items[item.ID].uses == '0':
            self.remove_item(item.ID)
        if item.duration != 0:
            item.duration = (item.duration * 60 * 60 * 24) + time.time()
            self.effects[item.item_type] = item
        if item.item_type == 'money':
                self.exp += item.effect
        
    def equip_item(self, item):
        self.equipped[item.item_type] = item

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

    def modify_health(self, value_change):
        self.health += value_change

    def set_attack_multiplier(self, new_mult):
        self.attack_multiplier = new_mult
        

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
    def __init__(self, h_type, title, desc, value, timestamp, exp = 100 ):
        self.h_type = h_type
        self.title = title
        self.description = desc
        self.ID = -1
        self.timestamp = timestamp
        #self.timestamp = date.today() - timedelta(hours=24)

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
    def __init__(self, name, desc, image, value, uses, item_type, active, effect, duration, component):
        self.name = name
        self.ID = 0
        self.description = desc
        self.image = image
        self.value = value
        self.uses = uses
        self.item_type = item_type
        self.active = active
        self.effect = effect
        self.duration = duration
        self.component = component

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
                      'active':self.active, 
                      'duration':self.duration,
                      'component':self.component}
        
        return item_dict
