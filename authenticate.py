
"""
This module handles authorization and sync for the dropbox storage.
"""
 
import dropbox
import webbrowser
import os.path
import time
 
 
def sync_files(client, file_name):
    """
    Pass this function a dropbox client and it will compare the local file
    with the copy on the user's dropbox. it replaces the older file with the
    contents of the newer.
    """
     
    local_modified = time.gmtime(os.path.getmtime(file_name))
 
    dropbox_file = client.metadata('//' + file_name)
    db_modified = time.strptime(dropbox_file.get('modified')[:-5] + 'GMT', '%a, %d %b %Y %H:%M:%S %Z')
 
    print 'local modified: %s' % local_modified
    print 'dpbox modified: %s' % db_modified
 
    # to this point, the timestamps are in python time_struct form. this if-statement
    # converts them to seconds since the unix epoch and subtracts them to find the newest.
    if time.mktime(local_modified) - time.mktime(db_modified) > 0:
        print 'local file is more recent, updating dropbox file'
 
        client.file_delete('//' + file_name)
        file = open(file_name)
        client.put_file('//' + file_name, file)
    else:
        print 'dropbox file is more recent, overwriting local file'
 
        out = open(file_name, 'wb')
        with client.get_file('//' + file_name) as f:
            out.write(f.read())
         
     
def dropbox_auth():
    """
    Returns a dropbox client object. the client object gives control of the user's
    dropbox and contains methods to save/push files, get user info, etc. When this
    is finished executing, it ensures that there is a file both locally and on db,
    and performs an initial sync of data.
    """
     
    file_name = 'character.xml'
    key = 'q5r7dogatg3ruh0'
    secret = 'ch340x6gxyqk8ie'
 
    # check to see if there's an xml file already. if so, no need to go through the whole flow 
    if os.path.isfile(file_name):
         
        #TODO: use XML parsing instead of reading the file normally
         
        file = open(file_name)
        line = file.readline()
        access_token = line.strip()
        #access_token = 'xoH35mr0iRwAAAAAAAAAI0OZOexRWxqEKabFZRlf6m2WY3j8xkLEcwAEpV297oXv'
        client = dropbox.client.DropboxClient(access_token)
 
        # if there's a local file but no remote, push the local to db
        # this shouldn't really ever happen, but just in case.
        if not client.search('//', file_name):
            file = open(file_name, 'r')
            client.put_file('//' + file_name, file)
            file.close()
        else:
            # if there's a local AND and db file, sync to use the most recent.
            sync_files(client, file_name)
         
    else:
        # no local file, get access_token from website instead
         
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(key, secret)
        authorize_url = flow.start()
     
        print '1. Go to your browser, a new tab should have opened: '
        web = webbrowser.open(authorize_url, new=2, autoraise=True)
        print '2. Click "Allow" (you might have to log in first)'
        print '3. Copy the authorization code.'
        code = raw_input("Enter the authorization code here: ").strip()
 
        access_token, user_id = flow.finish(code)
        client = dropbox.client.DropboxClient(access_token)
        print access_token
 
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
 
    return client
