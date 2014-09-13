
"""
This module handles authorization for the dropbox storage.
"""

import dropbox
import webbrowser
import os.path

def dropbox_auth():
    """
    Returns a dropbox client object. the client object gives control of the user's
    dropbox and contains methods to save/push files, get user info, etc.
    """
    
    fname = 'character.xml'
    key = 'q5r7dogatg3ruh0'
    secret = 'ch340x6gxyqk8ie'

    # check to see if there's an xml file already. if so, no need to go through the whole flow 
    if os.path.isfile(fname):

        #TODO: use XML parsing instead
        print 'Placeholder code, currently using the hardcoded auth token.'

        access_token = 'xoH35mr0iRwAAAAAAAAAI0OZOexRWxqEKabFZRlf6m2WY3j8xkLEcwAEpV297oXv'
        client = dropbox.client.DropboxClient(access_token)
        
    else:
        # get access_token from website instead
        
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(key, secret)
        authorize_url = flow.start()
    
        print '1. Go to your browser, a new tab should have opened: '
        web = webbrowser.open(authorize_url, new=2, autoraise=True)
        print '2. Click "Allow" (you might have to log in first)'
        print '3. Copy the authorization code.'
        code = raw_input("Enter the authorization code here: ").strip()

        access_token, user_id = flow.finish(code)
        client = dropbox.client.DropboxClient(access_token)

    #TODO: write sync function and call here. the sync facilities provided by dropbox
    #appear to only work with mobile devices.
        
    #sync_files()

    return client
