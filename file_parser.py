"""

TODO: add functionality to parse items, habits and dailies in a later sprint.

.

This class handles parsing the XML character data file. To initially parse
the file into a useable form, call

data = parser(filepath)

tasks = parse_hacks() will return a list of dicts to represent all the data
in the tasks.

>>> data = parser('character.xml')
>>> tasks = data.parse_hacks()
>>> sorted(tasks[0].keys())
['description', 'due', 'index', 'title']
>>> name = data.parse_name()
>>> name
'Krugg'
>>> level = data.parse_level()
>>> level
2
>>> token = data.parse_token()
>>> token
'xoH35mr0iRwAAAAAAAAAI0OZOexRWxqEKabFZRlf6m2WY3j8xkLEcwAEpV297oXv'
>>> exp = data.parse_exp()
>>> exp
120
>>> cash = data.parse_cash()
>>> cash
42

"""

import xml.dom.minidom


class file_parser:


    #This list is used to check parsed values for conversion
    #purposes (everything is parsed in as a string initially)
    integer_types = ['ID', 'cash', 'level', 'exp']
    float_types = ['version']

    def parse_simple(self, tag):
        """
        This function is used to parse the enclosed text in simple
        tags with no children.
        """
        self.nodes = self.doc.getElementsByTagName(tag)

        if len(self.nodes) == 0:
            return 0
        
        if self.nodes[0].nodeName in self.integer_types:
            return int(self.nodes[0].firstChild.data)

        elif self.nodes[0].nodeName in self.float_types:
            return float(self.nodes[0].firstChild.data)

        else:
            return self.nodes[0].firstChild.data


    def parse_firstname(self):
        return self.parse_simple('firstname')

    def parse_lastname(self):
        return self.parse_simple('lastname')

    def parse_birthday(self):
        return self.parse_simple('birthday')
    
    def parse_name(self):
        return self.parse_simple('username')
    
    def parse_token(self):
        return self.parse_simple('token')

    def parse_version(self):
        return self.parse_simple('version')
    
    def parse_exp(self):
        return self.parse_simple('exp')

    def parse_level(self):
        return self.parse_simple('level')

    def parse_cash(self):
        return self.parse_simple('cash')

    def parse_boss(self):
        return self.parse_simple('boss')

    def parse_hacks(self):
        """
        Returns a list of dictionaries, each dict is a separate hack.
        The dictionary attribute names are determined by the tag name used
        in the XML.

        Ex: to get the title of the first hack, you could just
        do hacks[0]['title']
        """

        self.hack_list = self.doc.getElementsByTagName('hack')

        hacks = list()
        
        for hack in self.hack_list:
            hack_dict = {}
            
            for node in hack.childNodes:
                if node.nodeType != node.TEXT_NODE:
                    tag_type = node.nodeName
                    if len(node.childNodes) == 0:
                        inner = ''
                    else:
                        inner = node.childNodes[0].data

                    if tag_type in self.integer_types:
                        inner = int(inner)
                        
                    hack_dict[tag_type] = inner

            hacks.append(hack_dict)
                
        return hacks

    def parse_items(self):
        """
        Returns list of dictionaries for items
        """

        self.item_list = self.doc.getElementsByTagName('item')
        
        items = list()
        
        for item in self.item_list:
            item_dict = {}
            
            for node in item.childNodes:
                if node.nodeType != node.TEXT_NODE:
                    tag_type = node.nodeName
                    inner = node.childNodes[0].data

                    if tag_type in self.integer_types:
                        inner = int(inner)
                        
                    item_dict[tag_type] = inner

            items.append(item_dict)
                
        return items


    def replace_text(self, node, newText):
        if node.firstChild.nodeType != node.TEXT_NODE:
            raise Exception("node doesn't contain text")

        node.firstChild.replaceWholeText(newText)

    def create_list_node(self, doc, hack_data):
        '''
        Returns a hack XMLNode element
        '''

        h_type = hack_data['h_type']
        title = hack_data['title']
        desc = hack_data['desc']
        _id = hack_data['ID']
        value = hack_data['value']
        exp = hack_data['exp']
        
        node = doc.createElement('hack')
        h_type_node = doc.createElement('h_type')
        title_node = doc.createElement('title')
        desc_node = doc.createElement('desc')
        id_node = doc.createElement('ID')
        value_node = doc.createElement('value')
        exp_node = doc.createElement('exp')

        h_type_node_text = doc.createTextNode(h_type)
        title_node_text = doc.createTextNode(title)
        desc_node_text = doc.createTextNode(desc)
        id_node_text = doc.createTextNode(str(_id))
        value_node_text = doc.createTextNode(str(value))
        exp_node_text = doc.createTextNode(str(exp))

        h_type_node.appendChild(h_type_node_text)
        title_node.appendChild(title_node_text)
        desc_node.appendChild(desc_node_text)
        id_node.appendChild(id_node_text)
        value_node.appendChild(value_node_text)
        exp_node.appendChild(exp_node_text)

        node.appendChild(h_type_node)
        node.appendChild(title_node)
        node.appendChild(desc_node)
        node.appendChild(id_node)
        node.appendChild(value_node)
        node.appendChild(exp_node)

        return node
            
    def update_file(self, char, savefile):

        #placeholder, this will handle saving character data to
        #the file I'm thinking we'll want to pass everything in
        #as a single list and structure the XML data depending
        #on whether it's a single item or a list

        #Recreate the dom
        newdoc = xml.dom.minidom.Document()
        
        #print(self.doc.toprettyxml(indent="", encoding='utf-8'))

        #Local variables from character
        
        char_fname = char['firstname']
        char_lname = char['lastname']
        char_birthday = char['birthday']
        char_token = char['token']
        char_version = str(char['version'])
        char_name = char['name']
        char_cash = str(char['cash'])
        char_level = str(char['level'])
        char_exp = str(char['exp'])
        char_boss = char['boss']
        char_hacks = char['hacks']
        char_items = char['items']

        #Create XML Node Elements
        root_element = newdoc.createElement('data')
        token_element = newdoc.createElement('token')
        version_element = newdoc.createElement('version')
        firstname_element = newdoc.createElement('firstname')
        lastname_element = newdoc.createElement('lastname')
        username_element = newdoc.createElement('username')
        birthday_element = newdoc.createElement('birthday')
        cash_element = newdoc.createElement('cash')
        exp_element = newdoc.createElement('exp')
        boss_element = newdoc.createElement('boss')
        level_element = newdoc.createElement('level')
        hacks_element = newdoc.createElement('hacks')
        items_element = newdoc.createElement('items')
           
        #Create text nodes for elements
        token_text = newdoc.createTextNode(char_token)
        version_text = newdoc.createTextNode(char_version)
        firstname_text = newdoc.createTextNode(char_fname)
        lastname_text = newdoc.createTextNode(char_lname)
        username_text = newdoc.createTextNode(char_name)
        birthday_text = newdoc.createTextNode(char_birthday)
        cash_text = newdoc.createTextNode(char_cash)
        exp_text = newdoc.createTextNode(char_exp)
        boss_text = newdoc.createTextNode(char_boss)
        level_text = newdoc.createTextNode(char_level)
            
        #Append text nodes to elements
        token_element.appendChild(token_text)
        version_element.appendChild(version_text)
        firstname_element.appendChild(firstname_text)
        lastname_element.appendChild(lastname_text)
        username_element.appendChild(username_text)
        birthday_element.appendChild(birthday_text)
        cash_element.appendChild(cash_text)
        boss_element.appendChild(boss_text)
        exp_element.appendChild(exp_text)
        level_element.appendChild(level_text)
        
        #Fill hacks and items
        for hack in char_hacks:
            node = self.create_list_node(newdoc, hack)
            hacks_element.appendChild(node)
        
        for item in char_items:
            node = newdoc.createElement('item')
            title_element = newdoc.createElement('title')
            description_element = newdoc.createElement('desc')
            ID_element = newdoc.createElement('ID')
            image_element = newdoc.createElement('image')
            value_element = newdoc.createElement('value')
            uses_element = newdoc.createElement('uses')
            item_type_element = newdoc.createElement('item_type')
            effect_element = newdoc.createElement('effect')
            active_element = newdoc.createElement('active')
            
            title_text_node = newdoc.createTextNode(item['title'])
            description_text_node = newdoc.createTextNode(item['desc'])
            ID_text_node = newdoc.createTextNode(str(item['ID']))
            image_text_node = newdoc.createTextNode(item['image'])
            value_text_node = newdoc.createTextNode(str(item['value']))
            uses_text_node = newdoc.createTextNode(str(item['uses']))
            item_type_text_node = newdoc.createTextNode(str(item['item_type']))
            effect_text_node = newdoc.createTextNode(str(item['effect']))
            active_text_node = newdoc.createTextNode(str(item['active']))
            
            title_element.appendChild(title_text_node)
            description_element.appendChild(description_text_node)
            ID_element.appendChild(ID_text_node)
            image_element.appendChild(image_text_node)
            value_element.appendChild(value_text_node)
            uses_element.appendChild(uses_text_node)
            item_type_element.appendChild(item_type_text_node)
            effect_element.appendChild(effect_text_node)
            active_element.appendChild(active_text_node)
            
            node.appendChild(title_element)
            node.appendChild(description_element)
            node.appendChild(ID_element)
            node.appendChild(image_element)
            node.appendChild(value_element)
            node.appendChild(uses_element)
            node.appendChild(item_type_element)
            node.appendChild(effect_element)
            node.appendChild(active_element)
            
            items_element.appendChild(node)
        
        #Append elements to root element
        root_element.appendChild(token_element)
        root_element.appendChild(version_element)
        root_element.appendChild(firstname_element)
        root_element.appendChild(lastname_element)
        root_element.appendChild(username_element)
        root_element.appendChild(birthday_element)
        root_element.appendChild(cash_element)
        root_element.appendChild(exp_element)
        root_element.appendChild(level_element)
        root_element.appendChild(boss_element)
        root_element.appendChild(hacks_element)
        root_element.appendChild(items_element)
        newdoc.appendChild(root_element)
        
        #print(name_node.toprettyxml())
        #print(cash_node.toprettyxml())
        #print(level_node.toprettyxml())
        #print(exp_node.toprettyxml())
        #print(hacks_node.toprettyxml())
        #print(items_node.toprettyxml())

        #Write XMLDocument to file
        try:
            file = open(savefile, 'wb')
            file.write(newdoc.toprettyxml(indent="   ", encoding="utf-8"))
            file.close()
            
        except:
            print("Couldn't save data to file")
            
        return
    

    def __init__(self, filename):
        try:
            self.doc = xml.dom.minidom.parse(filename)

        except FileNotFoundError:
            self.doc = xml.dom.minidom.Document()

#unit tests, aww yiss
if __name__ == "__main__":
    
    import doctest
    doctest.testmod()
    
    data = parser('character.xml')
    tasks = data.parse_hacks()
