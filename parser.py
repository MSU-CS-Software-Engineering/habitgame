#rough first version of the parsing functions.
#need to finish parsing tasks.

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

    def __init__(self, filename):

        self.doc = xml.dom.minidom.parse(filename)
        
data = parser('character.xml')
