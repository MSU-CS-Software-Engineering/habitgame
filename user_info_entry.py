#User Information entry form
#This still needs to be styled and needs to look better, but the basics are here
#needs a def to push/pull user information to text file
from tkinter import *
from tkinter import ttk
import authenticate

def finish_flow():

    db.dropbox_finish(auth_code.get())
    root.destroy()

db = authenticate.db()
db.dropbox_start()

if not db.client:
    """
    For the first sprint, we want to skip the login window if
    there is already a character file present.
    """

    root = Tk()
    root.title("User Information")

    main_window = ttk.Frame(root, padding = "3 3 12 12")
    main_window.grid(column=0, row=0, stick = 'nesw')
    main_window.columnconfigure(0, weight =1)
    main_window.rowconfigure(0, weight= 1)
     
     
    #First name entry label, entry area, and entry variable
    fname = StringVar()
    f_name = ttk.Entry(main_window, width = 25, textvariable = fname)
    f_name.grid(row = 0, column = 1,columnspan = 3, sticky='e')
     
    f_name_label = ttk.Label(main_window, text = "First Name:", padding = 5)
    f_name_label.grid(row=0, column=0, sticky='w')
     
    #Last name entry label, entry area, and entry variable
    lname = StringVar()
    l_name = ttk.Entry(main_window, width = 25, textvariable = lname)
    l_name.grid(row = 1, column = 1,columnspan = 3, sticky='e')
     
    l_name_label = ttk.Label(main_window, text = "Last Name:", padding = 5)
    l_name_label.grid(row=1, column=0, sticky='w')
     
    #Character name entry label, entry area, and entry variable
    character_name = StringVar()
    character_name_entry = ttk.Entry(main_window, width = 25, textvariable = character_name)
    character_name_entry.grid(row = 2, column = 1, columnspan = 3, sticky='e')
     
    character_name_label = ttk.Label(main_window, text = "Character (username):", padding = 5)
    character_name_label.grid(row=2, column=0, sticky='w')
     
     
    #Birthdate entry label, entry area, and entry variable                                        
    birthdate_month = StringVar()
    birthdate_month_entry = ttk.Entry(main_window, width = 2,
                                      textvariable = birthdate_month)
    birthdate_month_entry.grid(row = 3, column = 1, sticky = 'e')
     
    birthdate_day = StringVar()
    birthdate_day_entry = ttk.Entry(main_window, width = 2,
                                    textvariable = birthdate_day)
    birthdate_day_entry.grid(row = 3, column = 2)
     
    birthdate_year = StringVar()
    birthdate_year_entry = ttk.Entry(main_window, width = 2,
                                     textvariable = birthdate_year)
    birthdate_year_entry.grid(row = 3, column = 3, sticky = 'w')
     
    birthdate_label = ttk.Label(main_window, text = "Birthdate:", padding = 5)
    birthdate_label.grid(row = 3, column = 0, sticky='w')
     
    #Area for dropbox connection information.
    dropbox_frame = ttk.LabelFrame(main_window,
                                   text = "Connect to DropBox Here",
                                   height = 150, width = 300, padding = 10)
    dropbox_frame.grid(row = 4, column = 0, columnspan = 4)
      
    line1 = '1. Go to your browser, a new tab should have opened:'
    db_line1 = ttk.Label(dropbox_frame, text = line1, padding = 3)
    db_line1.grid(row = 0, column = 0, sticky='w')
     
    line2 = '2. Click "Allow" (you may be asked to log in first)'
    db_line2 = ttk.Label(dropbox_frame, text = line2, padding = 3)
    db_line2.grid(row = 1, column = 0, sticky='w')
     
    line3 = '3. Copy the authorization code and paste below.'
    db_line3 = ttk.Label(dropbox_frame, text = line3, padding = 3)
    db_line3.grid(row = 2, column = 0, sticky='w')
     
    auth_code = StringVar()
    code = ttk.Entry(dropbox_frame, width = 35, textvariable = auth_code)
    code.grid(row = 3, column = 0)
          
    submit_button = Button(dropbox_frame, text = 'Submit', command = finish_flow)
    submit_button.grid(row = 4, column = 0)
      
    root.mainloop()

else:

    # put main window here?
    print('skipping login window, a local file is already present')
