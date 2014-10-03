#rough WIP, currently returns the tasks as a regular list (not a dict)

import xml.dom.minidom


class parser:

    def get_text(self, nodelist):
        self.text = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                self.text.append(node.data)
        return self.text
        

    def parse_name(self):
        
        self.name_nodes = self.doc.getElementsByTagName('name')
        return self.name_nodes[0].firstChild.data
    
    def parse_token(self):

        self.token = self.doc.getElementsByTagName('token')
        return self.token[0].firstChild.data

    def parse_tasks(self):

        self.task_list = self.doc.getElementsByTagName('task')
        tasks = list()
        
        for task in self.task_list:
            for node in task.childNodes:
                #print(node.data)
                tasks.append(node.data)
                
        return tasks

    def __init__(self, filename):

        self.doc = xml.dom.minidom.parse(filename)
        

if __name__ == "__main__":
    
    data = parser('character.xml')
    tasks = data.parse_tasks()
