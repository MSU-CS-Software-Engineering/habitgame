"""

TODO: add functionality to parse items, habits and dailies in a later sprint.



This class handles parsing the XML character data file. To initially parse
the file into a useable form, call

data = parser(filepath)

tasks = parse_tasks() will return a list of dicts to represent all the data
in the tasks.

>>> data = parser('character.xml')
>>> tasks = data.parse_tasks()
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
    integer_types = ['index', 'cash', 'level', 'exp']


    def parse_simple(self, tag):
        """
        This function is used to parse the enclosed text in simple
        tags with no children.
        """
        self.nodes = self.doc.getElementsByTagName(tag)

        if self.nodes[0].nodeName in self.integer_types:
            return int(self.nodes[0].firstChild.data)
        
        return self.nodes[0].firstChild.data


    def parse_name(self):
        return self.parse_simple('name')
    
    def parse_token(self):
        return self.parse_simple('token')

    def parse_exp(self):
        return self.parse_simple('exp')

    def parse_level(self):
        return self.parse_simple('level')

    def parse_cash(self):
        return self.parse_simple('cash')


    def parse_tasks(self):
        """
        Returns a list of dictionaries, each dict is a separate task.
        The dictionary attribute names are determined by the tag name used
        in the XML.

        Ex: to get the title of the first task, you could just
        do tasks[0]['title']
        """

        self.task_list = self.doc.getElementsByTagName('task')

        tasks = list()
        
        for task in self.task_list:
            task_dict = {}
            
            for node in task.childNodes:
                if node.nodeType != node.TEXT_NODE:
                    tag_type = node.nodeName
                    inner = node.childNodes[0].data

                    if tag_type in self.integer_types:
                        inner = int(inner)
                        
                    task_dict[tag_type] = inner

            tasks.append(task_dict)
                
        return tasks


    def update_file(self, char):

        #placeholder, this will handle saving character data to the file
        #I'm thinking we'll want to pass everything in as a single list
        #and structure the XML data depending on whether it's a single item or
        #a list 
        return
    

    def __init__(self, filename):

        self.doc = xml.dom.minidom.parse(filename)
        

#unit tests, aww yiss
if __name__ == "__main__":
    
    import doctest
    doctest.testmod()
    
    data = parser('character.xml')
    tasks = data.parse_tasks()
