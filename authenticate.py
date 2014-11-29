"""

This class handles authorization and sync for the dropbox storage. How to use:
When we start the program, instantiate the class and assign it to a variable (we
need to have a copy of the dropbox client to sync files).
  
db = db()
  
The __init__ function below starts the authentication process. If there is a local
character data file it will simply make the client from the data inside with no
login window necessary. If there is no local file, it opens the dropbox site and
our login page to finish the process of authentication.
  
db.sync_files(file_name) will sync between local and remote files.

"""

import xml.dom.minidom
import dropbox
import webbrowser
import os.path
import time
from tkinter import *
from tkinter import ttk


class db:
    def set_code(self, new_code):
        self.code = new_code

    
    def sync_files(self, file_name='character.xml'):
        """
        Call this function and it will compare the local file
        with the copy on the user's dropbox. it replaces the older file with the
        contents of the newer.
        """
           
        local_modified = time.gmtime(os.path.getmtime(self.file_name))
       
        dropbox_file = self.client.metadata('//' + self.file_name)
        db_modified = time.strptime(dropbox_file.get('modified')[:-5] + 'GMT', '%a, %d %b %Y %H:%M:%S %Z')
       
        print('local modified: ', local_modified)
        print('dpbox modified: ', db_modified)
      
        # To this point, the timestamps are in python time_struct form. this if-statement
        # converts them to seconds since the unix epoch and subtracts them to find the newest.
        if time.mktime(local_modified) - time.mktime(db_modified) > 0:
            print('local file is more recent, updating dropbox file')
       
            self.client.file_delete('//' + self.file_name)
            file = open(self.file_name)
            self.client.put_file('//' + self.file_name, file)
        elif time.mktime(local_modified) - time.mktime(db_modified) < 0:
            print('dropbox file is more recent, overwriting local file')
       
            out = open(self.file_name, 'wb')
            with self.client.get_file('//' + self.file_name) as f:
                out.write(f.read())
        else:
            print('The 2 files have the same timestamp, no sync required')

    def getNodeText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
    
    def dropbox_start(self):
        """
        starts the dropbox process; control will be passed
        to the login window if necessary
        """

        self.file_name = 'character.xml'
        key = 'q5r7dogatg3ruh0'
        secret = 'ch340x6gxyqk8ie'
        self.client = ''
     
        # check to see if there's an xml file already. if so, no need to go through the whole flow 
        if os.path.isfile(self.file_name):
               
            #DONE: use XML parsing instead of reading the file line by line
               
            file = open(self.file_name)
            file_string = file.read()
            character_xml_data = xml.dom.minidom.parseString(file_string)
            token_node = character_xml_data.getElementsByTagName("token")[0]
            access_token = self.getNodeText(token_node.childNodes)
            
            self.client = dropbox.client.DropboxClient(access_token)
       
            # if there's a local file but no remote, push the local to db
            # this shouldn't really ever happen, but just in case.
            if not self.client.search('//', self.file_name):
                file = open(self.file_name, 'r')
                self.client.put_file('//' + self.file_name, file)
                file.close()
            else:
                # if there's a local AND and db file, sync to use the most recent.
                self.sync_files(self.file_name)
               
        else:
            # no local file, get access_token from website instead
               
            self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(key, secret)
            authorize_url = self.flow.start()
              
            web = webbrowser.open(authorize_url, new=2, autoraise=True)
            
            self.login_window()
        

    def dropbox_finish(self, code, firstname, lastname, username, birthday):
        """
        Call this function to finish the dropbox flow and create a dropbox client
        (after the user pastes their authorization code in the login screen).
        """
        
        access_token, user_id = self.flow.finish(code)
        self.client = dropbox.client.DropboxClient(access_token)
        print(access_token)
   
        # if db is empty too, new user w/ new install. create local xml file and push to db
        if not self.client.search('//', self.file_name):
            file = open(self.file_name, 'wb')
            # TODO: file creation function goes here, placeholder write
            # init_file(file)

            newdoc = xml.dom.minidom.Document()

            #Create XML Node Elements
            root_element = newdoc.createElement('data')
            token_element = newdoc.createElement('token')
            firstname_element = newdoc.createElement('firstname')
            lastname_element = newdoc.createElement('lastname')
            username_element = newdoc.createElement('username')
            birthday_element = newdoc.createElement('birthday')

            #Create text nodes for elements
            token_text = newdoc.createTextNode(access_token)
            firstname_text = newdoc.createTextNode(firstname)
            lastname_text = newdoc.createTextNode(lastname)
            username_text = newdoc.createTextNode(username)
            birthday_text = newdoc.createTextNode(birthday)

            #Append text nodes to elements
            token_element.appendChild(token_text)
            firstname_element.appendChild(firstname_text)
            lastname_element.appendChild(lastname_text)
            username_element.appendChild(username_text)
            birthday_element.appendChild(birthday_text)
            
            #Append elements to root element
            root_element.appendChild(token_element)
            root_element.appendChild(firstname_element)
            root_element.appendChild(lastname_element)
            root_element.appendChild(username_element)
            root_element.appendChild(birthday_element)
            newdoc.appendChild(root_element)
            
            self.data_document = newdoc
            file.write(self.data_document.toprettyxml(indent="   ", encoding="utf-8"))
            
            file.close()
   
            # for some reason open(file_name, 'r+') (read AND write) wouldn't work, so I had to
            # open and close separately for the read and writes.
               
            file = open(self.file_name, 'r')
            self.client.put_file('//' + self.file_name, file)
            file.close()
            
        else:
            # file on db, so this is an existing user w/ a new install
            file = open(self.file_name, 'wb')
            with self.client.get_file('//' + self.file_name) as db_file:
                file.write(db_file.read())
            file.close()


    def finish_flow(self):
        """
        This function is tied to our 'submit' button. it takes the value that the
        user input and passes it to the dropbox_finish() function,
        then it destroys the window when that's finished.
        """

        birthday_string = "-".join((self.birthdate_month.get(), self.birthdate_day.get(), self.birthdate_year.get()))
        
        self.dropbox_finish(self.auth_code.get(), self.fname.get(), self.lname.get(), self.character_name.get(), birthday_string)
        self.root.destroy()

    
    def login_window(self):

        """
        This function contains all the tkinter code to create the login window
        """

        self.root = Tk()
        self.root.title("User Information")
        self.root.resizable(0,0)
        self.root.protocol("WM_DELETE_WINDOW", lambda : None)

        self.main_window = ttk.Frame(self.root, padding = "3 3 12 12")
        self.main_window.grid(column=0, row=0, stick = 'nesw')
        self.main_window.columnconfigure(0, weight =1)
        self.main_window.rowconfigure(0, weight= 1)
         
         
        #First name entry label, entry area, and entry variable
        self.fname = StringVar()
        self.f_name = ttk.Entry(self.main_window, width = 25, textvariable = self.fname)
        self.f_name.grid(row = 0, column = 1,columnspan = 3, sticky='e')
         
        self.f_name_label = ttk.Label(self.main_window, text = "First Name:", padding = 5)
        self.f_name_label.grid(row=0, column=0, sticky='w')
         
        #Last name entry label, entry area, and entry variable
        self.lname = StringVar()
        self.l_name = ttk.Entry(self.main_window, width = 25, textvariable = self.lname)
        self.l_name.grid(row = 1, column = 1,columnspan = 3, sticky='e')
         
        self.l_name_label = ttk.Label(self.main_window, text = "Last Name:", padding = 5)
        self.l_name_label.grid(row=1, column=0, sticky='w')
         
        #Character name entry label, entry area, and entry variable
        self.character_name = StringVar()
        self.character_name_entry = ttk.Entry(self.main_window, width = 25, textvariable = self.character_name)
        self.character_name_entry.grid(row = 2, column = 1, columnspan = 3, sticky='e')
         
        self.character_name_label = ttk.Label(self.main_window, text = "Character (username):", padding = 5)
        self.character_name_label.grid(row=2, column=0, sticky='w')
         
         
        #Birthdate entry label, entry area, and entry variable                                        
        self.birthdate_month = StringVar()
        self.birthdate_month_entry = ttk.Entry(self.main_window, width = 2,
                                          textvariable = self.birthdate_month)
        self.birthdate_month_entry.grid(row = 3, column = 1, sticky = 'e')
         
        self.birthdate_day = StringVar()
        self.birthdate_day_entry = ttk.Entry(self.main_window, width = 2,
                                        textvariable = self.birthdate_day)
        self.birthdate_day_entry.grid(row = 3, column = 2)
         
        self.birthdate_year = StringVar()
        self.birthdate_year_entry = ttk.Entry(self.main_window, width = 2,
                                         textvariable = self.birthdate_year)
        self.birthdate_year_entry.grid(row = 3, column = 3, sticky = 'w')
         
        self.birthdate_label = ttk.Label(self.main_window, text = "Birthdate:", padding = 5)
        self.birthdate_label.grid(row = 3, column = 0, sticky='w')
         
        #Area for dropbox connection information.
        self.dropbox_frame = ttk.LabelFrame(self.main_window,
                                       text = "Connect to DropBox Here",
                                       height = 150, width = 300, padding = 10)
        self.dropbox_frame.grid(row = 4, column = 0, columnspan = 4)
          
        self.line1 = '1. Go to your browser, a new tab should have opened:'
        self.db_line1 = ttk.Label(self.dropbox_frame, text = self.line1, padding = 3)
        self.db_line1.grid(row = 0, column = 0, sticky='w')
         
        self.line2 = '2. Click "Allow" (you may be asked to log in first)'
        self.db_line2 = ttk.Label(self.dropbox_frame, text = self.line2, padding = 3)
        self.db_line2.grid(row = 1, column = 0, sticky='w')
         
        self.line3 = '3. Copy the authorization code and paste below.'
        self.db_line3 = ttk.Label(self.dropbox_frame, text = self.line3, padding = 3)
        self.db_line3.grid(row = 2, column = 0, sticky='w')
         
        self.auth_code = StringVar()
        self.code = ttk.Entry(self.dropbox_frame, width = 35, textvariable = self.auth_code)
        self.code.grid(row = 3, column = 0)
              
        self.submit_button = Button(self.dropbox_frame, text = 'Submit', command = self.finish_flow)
        self.submit_button.grid(row = 4, column = 0)
          
        self.root.mainloop()

    def __init__(self):

        """
        This runs the dropbox setup function when a db object is first initialized.
        """
        self.data_document = ''
        self.dropbox_start()
        
        
