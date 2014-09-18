"""
This class handles authorization and sync for the dropbox storage. How to use:
When we start the program, instantiate the class and assign it to a variable (we
need to have a copy of the dropbox client to pass later).
  
client = db()
  
client.dropbox_start() will start the process. If there's already a token in a
local file, it simply created the dropbox client.
  
client.sync_files(file_name) will sync between local and remote files.
"""
   
import dropbox
import webbrowser
import os.path
import time


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

               
    def dropbox_start(self):
        """
        starts the dropbox process, then control will be passed back to the login window
        """

        self.file_name = 'character.xml'
        key = 'q5r7dogatg3ruh0'
        secret = 'ch340x6gxyqk8ie'
        self.client = ''
     
        # check to see if there's an xml file already. if so, no need to go through the whole flow 
        if os.path.isfile(self.file_name):
               
            #TODO: use XML parsing instead of reading the file line by line
               
            file = open(self.file_name)
            line = file.readline()
            access_token = line.strip()
     
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

        

    def dropbox_finish(self, code):
        """
        Call this function to finish the dropbox flow and create a dropbox clients
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
            file.write(access_token)
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
           
    """def dropbox_auth(self):
        
        Processes tokens and logins to set the client class var to a dropbox client.
        the client object gives control of the user's dropbox and contains methods to
        save/push files, get user info, etc. When this is finished executing, it ensures
        that there is a file both locally and on db, and performs an initial sync of data.
        
           
        file_name = 'character.xml'
        key = 'q5r7dogatg3ruh0'
        secret = 'ch340x6gxyqk8ie'
     
     
        # check to see if there's an xml file already. if so, no need to go through the whole flow 
        if os.path.isfile(file_name):
               
            #TODO: use XML parsing instead of reading the file line by line
               
            file = open(file_name)
            line = file.readline()
            access_token = line.strip()
     
            client = dropbox.client.DropboxClient(access_token)
       
            # if there's a local file but no remote, push the local to db
            # this shouldn't really ever happen, but just in case.
            if not client.search('//', file_name):
                file = open(file_name, 'r')
                client.put_file('//' + file_name, file)
                file.close()
            else:
                # if there's a local AND and db file, sync to use the most recent.
                self.sync_files(file_name)
               
        else:
            # no local file, get access_token from website instead
               
            flow = dropbox.client.DropboxOAuth2FlowNoRedirect(key, secret)
            authorize_url = flow.start()
              
            web = webbrowser.open(authorize_url, new=2, autoraise=True)
            
            access_token, user_id = flow.finish(code)
            self.client = dropbox.client.DropboxClient(access_token)
            print(access_token)
       
            # if db is empty too, new user w/ new install. create local xml file and push to db
            if not client.search('//', file_name):
                file = open(file_name, 'wb')
                # TODO: file creation function goes here, placeholder write
                # init_file(file)
                file.write(access_token)
                file.close()
       
                # for some reason open(file_name, 'r+') (read AND write) wouldn't work, so I had to
                # open and close separately for the read and writes.
                   
                file = open(file_name, 'r')
                client.put_file('//' + file_name, file)
                file.close()
            else:
                # file on db, so this is an existing user w/ a new install
                file = open(file_name, 'wb')
                with client.get_file('//' + file_name) as db_file:
                    file.write(db_file.read())
                file.close()
                """
    
