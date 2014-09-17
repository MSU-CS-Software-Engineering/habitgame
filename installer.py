from tkinter import *
from tkinter import ttk
import math
import tkinter.filedialog as fdialog 
import os
import shutil
import threading
import subprocess
import getpass
import time

root_directory_name = 'Habit'

class Installer_GUI:
    '''Installer_GUI class. Sets the min and maxsize of master, 
    or parent widget, which should be root. The installer window 
    has two frames: directional_panel and main_content_frame.

    Directional panel contains directional buttons, such as
    next, back, cancel and finish

    Main content frame contains main content from the different
    GUI pages, which are stored in the list variable 'self.pages'

    The different stages of installation GUI are displayed
    as different frames, refered to as 'pages'

    Class Variables:
    self.height = Window height of the Installer GUI
    self.width = Window width of Installer GUI
    self.current_page = Variable to hold the current_page value in 
    the sequence of page transitions
    self.number_of_pages = total number of page frames 
    self.pages = list that holds all the installers page frames
    self.license_accept = Variable to hold the state of the 
    license accept radiobuttons 
    self.EULA_string = The End-user license agreement string thats
    read from the file EULA.txt in the root directory
    self.installation_directory = Directory where Habit and install
    files will be installed
    self.home_directory(NOT IMPLEMENTED)
    self.install_progress = Control variable to update the installers
    progress bar
    self.installing = boolean variable to determine the state of the 
    file copying process
    self.directory_selection_entry = Entry widget used to hold and display
    the user-defined installation directory
    self.placeholder = Accessory to the directional panel to maintain the frames
    grid geometry
    self.buttonplaceholder = Another accessory that maintains the directional
    panel's grid geometry when the 'Back' button is removed
    self.installation_ready_text = Text widget used on the Installation Ready
    page. Acts as a final confirmation check for the user's directory choice
    self.progress_label = Label widget that displays the current task of the 
    installer
    self.progress_bar = Progress bar widget that shows the progress of the 
    installer
    self.run_postinstall_checkbox = Checkbox on the final page of the installer
    which indicates if the installer should run the recently installed program
    self.run_postiinstall = Boolean variable that holds the state of the 
    run_postinstall_checkbox
    self.executable_name = Final installation name to the habit executable
    '''

    def __init__(self, master, title):
        '''Instantiates an instance of the Installer_GUI class'''
        self.height = 360
        self.width = 500
        self.parent = master
        self.current_page = 1
        self.number_of_pages = 6
        self.pages = []
        self.platform = self.set_platform()
        self.license_accept = IntVar()
        self.installation_directory = self.config_install_dir()
        self.root_path = self.get_root_path()
        self.EULA_string = self.load_EULA()
        self.home_directory = ''
        self.installing = False
        self.run_postinstall = IntVar()
        self.executable_name = self.set_executable_name()
        
        #Local variables
        button_height = 1
        button_width = 9

        #Set parent window title
        self.parent.title(title)
        
        #Set parent window exit handler
        self.parent.protocol("WM_DELETE_WINDOW", self.exit_handler)

        master.minsize(width=self.width, height=self.height)
        master.maxsize(width=self.width, height=self.height)        
        self.mainframe = Frame(master)
        self.mainframe.grid()

        #Set installer window icon
        icon_address = self.root_path+'setup.ico'
        master.iconbitmap(icon_address)
        
        #Main Content Frame
        #The installer's different pages will be displayed in this frame
        self.main_content_frame = Frame(self.mainframe, width=self.width, 
                                        height=315, bd=1, bg='white', 
                                        relief='groove')
        self.main_content_frame.grid(row=0, column=0, sticky=N+S+W+E)
 
        #Directional Panel
        self.directional_panel = Frame(self.mainframe, width=self.width, 
                                       height=45, bd=1, relief='groove')
        self.directional_panel.grid(row=1, column=0, sticky=S+W+E)
        
        #Placeholder
        self.placeholder = Frame(self.directional_panel, width=270, height=45)
        self.placeholder.grid(sticky='w', row=0, column=0)
        
        #Button Placeholder
        self.buttonplaceholder = Frame(self.directional_panel, width=68,
                                       height=45)
        self.buttonplaceholder.grid(sticky='w', row=0, column=1)

        #Add directional buttons
        #Back button
        self.back_button = ttk.Button(self.directional_panel, text="< Back", 
                                  command=lambda: self.change_page(-1), 
                                  width=button_width)
        
        #Next button
        self.next_button = ttk.Button(self.directional_panel, text="Next >",
                                  command=lambda: self.change_page(1), 
                                  width=button_width)
        
        #Cancel button
        self.cancel_button = ttk.Button(self.directional_panel, text="Cancel",                                    command=lambda: self.change_page(0), 
                                    width=button_width)
        
        self.back_button.grid(row=0, column=1, padx=2, pady=7, sticky='E')
        self.next_button.grid(row=0, column=2, padx=2, pady=7, sticky='E')
        self.cancel_button.grid(row=0, column=3, padx=6, pady=7, sticky='E')
        
        
        #============INSTALLER PAGES=============================
        #Intro Page-----------------------------------------------
        #Intro page is split into two frames. The left one is a 
        #placeholder for an image; the right one holds the text
        #content
        new_page_frame = Frame(self.main_content_frame, 
                               width=500, height=315, bg='white')
    
        image_frame = Frame(new_page_frame, width=176,
                            height=315, bg="blue")
        text_frame = Frame(new_page_frame, width=334,
                           height=315, bg="white")
        
        image_frame.grid(row=0, column=0, sticky=W+E+N+S)
        text_frame.grid(row=0, column=1, sticky=W+E+N+S, padx=(10,0))
        
        label_1_string = "\nWelcome to the Habit Setup \nWizard"
        label_2_string = "\nThis will install Habit on your computer."
        label_3_string = "\nClick Next to continue, or Cancel to exit Setup."
        label_1 = Label(text_frame, font=('Helvetica', 16,'bold'),
                        text=label_1_string, bg='white', justify='left'
                       ).grid(row=0, column=0, padx=(10,10), sticky='w')
        label_2 = Label(text_frame, text=label_2_string, bg='white'
                       ).grid(row=1, column=0, padx=(10,10), sticky='w')
        label_3 = Label(text_frame, text=label_3_string, bg='white'
                       ).grid(row=2, column=0, padx=(10,10), sticky='w')
        
        self.pages.append(new_page_frame)
        #----------------------------------------------------------
        #License Agreement-----------------------------------------
        license_page_frame = Frame(self.main_content_frame, 
                               width=500, height=315)
        
        license_page_frame.columnconfigure(0, weight=1)
        title_label_string = 'License Agreement'
        caption_label_string = '    Please read the following important information before continuing'
        header_frame = self.create_page_header(license_page_frame, title_label_string,
                                          caption_label_string)
        header_frame.grid(row=0,column=0,sticky=N+W+E)
        page_content_frame = Frame(license_page_frame, width=self.width, 
                                   height=self.height - 105)
        page_content_frame.grid(row=1, column=0, sticky=N+S, padx=(25,25), pady=(5,23))
        page_content_frame_label_string = "Please read the following License Agreement. You must accept the terms of this \nagreement before continung with the installation."

        page_content_frame_label = Label(page_content_frame, text=page_content_frame_label_string, justify=LEFT).grid(column=0,sticky=W) 
        
        #EULA Text Area
        eula_text_area = Text(page_content_frame, font=('Helvetica', 8), width=70, height=10)
        eula_text_area.grid(row=1, column=0, sticky=W)
        eula_scrollbar = ttk.Scrollbar(page_content_frame, command=eula_text_area.yview)
        eula_text_area.insert(END, self.EULA_string)
        eula_text_area.config(yscrollcommand=eula_scrollbar.set, state=DISABLED)
        #print(self.EULA_string)
        eula_scrollbar.grid(row=1, column=1, sticky=N+S+W)

        #Radio buttons
        self.button_accept = ttk.Radiobutton(page_content_frame, 
                                        text="I accept the agreement", 
                                        variable=self.license_accept, 
                                        value=1,
                                        command=lambda : self.radio_button_changes(1)
                                        )
        self.button_accept.grid(column=0, sticky=W, pady=(5,0))
        
        self.button_not_accept = ttk.Radiobutton(page_content_frame, 
                                            text="I do not accept the agreement", 
                                            variable=self.license_accept, 
                                            value=0,
                                            command=lambda : self.radio_button_changes(0)
                                            )
        self.button_not_accept.grid(column=0, sticky=W)
        self.button_not_accept.invoke()

        self.pages.append(license_page_frame)

        #----------------------------------------------------------
        #Select Destination Location-------------------------------
        destination_page_frame = Frame(self.main_content_frame, 
                               width=500, height=315)
        
        destination_page_frame.columnconfigure(0, weight=1)
        title_label_string = 'Select Destination Location'
        caption_label_string = '    Where should Habit be installed?'
        header_frame = self.create_page_header(destination_page_frame, 
                                               title_label_string,
                                               caption_label_string)
        header_frame.grid(row=0,column=0,sticky=N+W+E)
        page_content_frame = Frame(destination_page_frame, width=self.width, 
                                   height=self.height - 105)
        page_content_frame.grid(row=1, column=0, sticky=N+S, padx=(25,25), pady=(5,23))
        page_content_frame_label_string = "Setup will install Habit into the following folder"

        page_content_frame_label = Label(page_content_frame, text=page_content_frame_label_string, justify=LEFT).grid(row=0, column=0,sticky=W)
        
        entry_label_string = "To continue, click Next. If you would like to select a different folder, click Browse."
        entry_label = Label(page_content_frame, text=entry_label_string)
        entry_label.grid(row=1, column=0, columnspan=2, sticky=W, pady=(8,0))

        self.directory_selection_entry = Entry(page_content_frame, width=55)
        self.directory_selection_entry.grid(row=2, column=0, sticky=W)
        self.directory_selection_entry.insert(0, self.installation_directory)
        
        browse_button = ttk.Button(page_content_frame, 
                                   text="Browse...",
                                   command=self.get_file_dialog)

        browse_button.grid(row=2, column=1, sticky=W)
        placholder = Frame(destination_page_frame, width=self.width, 
                           height=152).grid(row=3, column=0)
        self.pages.append(destination_page_frame)
        #----------------------------------------------------------
        #Ready to Install------------------------------------------
        ready_page_frame = Frame(self.main_content_frame, 
                               width=500, height=315)
        
        ready_page_frame.columnconfigure(0, weight=1)
        title_label_string = 'Ready to Install'
        caption_label_string = '    Setup is now ready to begin installing Habit on your computer'
        header_frame = self.create_page_header(ready_page_frame, 
                                               title_label_string,
                                               caption_label_string)
        header_frame.grid(row=0,column=0,sticky=N+W+E)
        page_content_frame = Frame(ready_page_frame, width=self.width, 
                                   height=self.height - 105)
        page_content_frame.grid(row=1, column=0, sticky=N+S, padx=(25,25), pady=(5,23))
        page_content_frame_label_string = "Click Install to continue with the installation, or click Back if you want to review or \nchange any settings"

        page_content_frame_label = Label(page_content_frame, text=page_content_frame_label_string, justify=LEFT).grid(row=0, column=0,sticky=W)
        
        self.installation_ready_text = Text(page_content_frame,
                                            font=('Helvetica', 8), 
                                            width=70, height=10,
                                            )
        self.installation_ready_text.grid(row=2,column=0)
        placeholder_frame = Frame(ready_page_frame, width=self.width, height=34)
        placeholder_frame.grid(row=3, column=0, pady=(5, 8))

        self.pages.append(ready_page_frame)
        
        #----------------------------------------------------------
        #Progress Page---------------------------------------------
        progress_page_frame = Frame(self.main_content_frame, 
                               width=500, height=315)
        
        progress_page_frame.columnconfigure(0, weight=1)
        title_label_string = 'Installing'
        caption_label_string = '    Please wait while setup installs Habit to your computer'
        header_frame = self.create_page_header(progress_page_frame, 
                                               title_label_string,
                                               caption_label_string)
        header_frame.grid(row=0,column=0,sticky=N+W+E)
        page_content_frame = Frame(progress_page_frame, width=self.width, 
                                   height=self.height - 105)
        page_content_frame.grid(row=1, column=0, sticky=N+S, padx=(25,25))
        page_content_frame_label_string = "Executing..."

        page_content_frame_label = Label(page_content_frame, text=page_content_frame_label_string, justify=LEFT).grid(row=0, column=0, sticky=N+W)
        
        self.progress_label = Label(page_content_frame, font=('Helvetica', 8), 
                                    text='Loading...', justify=LEFT)
        self.progress_label.grid(row=1, column=0, sticky=N+W)
        self.progress_bar = ttk.Progressbar(page_content_frame, 
                                            orient="horizontal",
                                            length=450,
                                            mode="determinate",
                                            )
        self.progress_bar.grid(row=2, column=0, sticky=N+W, pady=(3,10))

        placeholder_frame = Frame(page_content_frame, width=self.width, height=174)
        placeholder_frame.grid(row=3, column=0, pady=(5, 0))

        self.pages.append(progress_page_frame)

        #Final Page------------------------------------------------
        final_page_frame = Frame(self.main_content_frame, 
                               width=500, height=315, bg='white')
    
        image_frame = Frame(final_page_frame, width=176,
                            height=315, bg="blue")
        text_frame = Frame(final_page_frame, width=334,
                           height=315, bg="white")
        
        image_frame.grid(row=0, column=0, sticky=W+E+N+S)
        text_frame.grid(row=0, column=1, sticky=W+E+N+S, padx=(10,0))
        
        label_1_string = "\nCompleting the Habit Setup \nWizard"
        label_2_string = "\nSetup has finshed installing Habit on your computer"
        label_3_string = "\nClick Finish to continue to exit Setup."
        label_1 = Label(text_frame, font=('Helvetica', 16,'bold'),
                        text=label_1_string, bg='white', justify='left'
                       ).grid(row=0, column=0, padx=(10,10), sticky='w')
        label_2 = Label(text_frame, text=label_2_string, bg='white'
                       ).grid(row=1, column=0, padx=(10,10), sticky='w')
        label_3 = Label(text_frame, text=label_3_string, bg='white'
                       ).grid(row=2, column=0, padx=(10,10), sticky='w')
        run_postinstall_string = "Run Habit!"

        self.run_postinstall_checkbox = ttk.Checkbutton(text_frame, 
                                                        text=run_postinstall_string, 
                                                        variable=self.run_postinstall
                                                        )
        self.run_postinstall_checkbox.grid(row=3, column=0, pady=(10,10), 
                                           sticky='w')
                                                        
        self.pages.append(final_page_frame)
        
        #Back button isn't visible on first page
        self.back_button.grid_remove()
        #Call function to set GUI window in center of screen
        self.centerWindow()
        #Setup page 1 in main_content_frame
        self.pages[0].grid(row=0, column=0, sticky=N+S+W+E)
    
    def place_files(self):
        '''Places asset files for the habit game. The placement
        instructions are stored in a file called 'install_instructions'
        Placement process is as follows:
        1. Set self.installing to True
        2. Make 'habit' directory in self.installation_directory
        3. Read in asset folder name(MUST BE FIRST LINE IN FILE)
        4. Make directories indicated in install_instructions
        5. Place files from assets into directories

        Progress Bar Process:
        1. Get maximum number of files(number_of_directories + number_of_files)
        2. Set self.progress_bar.maximum to max number of files
        3. Call progress_bar.step after every iteration
        '''
        #Start time
        start_time = time.time()
        #Set self.installing to True
        self.installing = True

        #Create installation directory if it doesn't exist
        if not os.path.exists(self.installation_directory):
            os.makedirs(self.installation_directory)
        
        f = open(self.root_path+'install_instructions.txt', 'r')
        
        #Get name of asset folder
        asset_folder = f.readline().split("=")[1].rstrip()
        asset_folder_path = os.path.abspath(self.root_path + asset_folder)
        
        #Get number of directories to install
        number_of_directories = int(f.readline().split("=")[1].rstrip())
        
        #Get number of files in asset folder
        number_of_files = int(f.readline().split("=")[1].rstrip())
        
        #Step size of the progress bar. (One is added for the root directory)
        steps = math.floor(100/(number_of_directories + number_of_files + 1))
        self.progress_bar.config(maximum = 120)

        #print('Steps:', steps)
        
        #Dictionary to hold directory paths 
        directories = {}
        
        #Make directories from install_instructions
        for i in range(number_of_directories):
            current_directory_name = f.readline().rstrip()
            current_directory = self.installation_directory + '//' + \
                current_directory_name + '//'
            directories[current_directory_name] = os.path.dirname(current_directory)
            if not os.path.exists(directories[current_directory_name]):
                self.progress_label.config(text='Creating directory '+ directories[current_directory_name])
                os.makedirs(directories[current_directory_name])
                #Update progress bar
            self.progress_bar.step(steps)
        
        #Copy files from assets to directories
        cont = True
        for files in range(number_of_files):
                record = f.readline()
                current_file_name = record.split(":")[0].rstrip()
                current_file_directory = record.split(":")[1].rstrip()
                current_file_source = os.path.abspath(asset_folder_path+'//'+current_file_name)

                if current_file_directory == 'root':
                    current_file_destination = self.installation_directory +'//'+ current_file_name
                    print('Root:',current_file_destination, current_file_name)
                else:
                    current_file_destination = os.path.abspath(directories[current_file_directory] +'//'+ current_file_name)

                self.progress_label.config(text='Copying file '+current_file_source)
                #Copy file from source to destination
                shutil.copy(current_file_source, current_file_destination)
                #Update progress par
                self.progress_bar.step(steps)
                print(steps)
        

        if time.time() - start_time < .5:
            for i in range(20):
                self.progress_bar.step(1)
                time.sleep(.05)

        #Done copying installation files
        self.done_installing()


    def load_EULA(self):
        '''Loads EULA from file and returns it as a string'''
        EULA_string = ''
        with open(self.root_path + 'EULA.txt', 'r') as myfile:
            EULA_string = myfile.read()
        return EULA_string


    def create_page_header(self, parent, title, caption):
        '''Creates page headers for a descriptive display
        of each page'''
        header_frame = Frame(parent, width=self.width,
                            height=55, bg='white')
        
        title_label = Label(header_frame, font=('Helvetica', 8,'bold'),
                        text=title, bg='white', justify='left'
                       ).grid(row=0, column=0, padx=(10,10), pady=(10,0),sticky='w')
        caption_label = Label(header_frame, font=('Helvetica', 8),
                        text=caption, bg='white', justify='left'
                       ).grid(row=1, column=0, padx=(10,10), pady=(0,10),sticky='w')
        return header_frame

    def centerWindow(self):
        '''Centers the installer window in the center of the
        screen based on the computer screen dimensions'''
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - self.width)/2
        y = (sh - self.height)/2

        self.parent.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
    
    def check_page(self):
        '''Checks the current page and performs tasks
        based on the state'''
        if self.current_page == 1:
            self.next_button.config(state=NORMAL)
        
        elif self.current_page == 2:
            if self.license_accept.get() == 0:
                self.next_button.config(state=DISABLED)
        
        elif self.current_page < 4:
            self.next_button['text'] = 'Next >'
        
        elif self.current_page == 4:
            #Set ready to install text 
            self.next_button['text'] = 'Install'
            self.set_ready_install_text()
        
        elif self.current_page == 5:
            self.back_button.grid_remove()
            self.cancel_button.grid_remove()
            self.next_button.config(state=DISABLED)
            #Create thread to carry out file placement tasks
            t = threading.Thread(target=self.place_files)
            t.start()
        
        else:
            self.back_button.grid_remove()
            self.next_button.config(command=self.complete_installation)
                      
        
    def done_installing(self):
        '''Carries out the cleanup tasks post-install'''
        self.installing = False
        self.next_button.config(text='Finish', state=NORMAL)
        self.back_button.grid_remove()

    def change_page(self, direction):
        '''Method to change the pages after each directional button
        press'''
        if direction < 0:
            if self.current_page == 2:
                self.back_button.grid_remove()
                self.buttonplaceholder.grid()
            if self.current_page > 1:
                #Remove current page from main_content_frame
                self.pages[self.current_page - 1].grid_remove()
                self.current_page -= 1
            #Set main_content_frame based on current page
            self.pages[self.current_page - 1].grid(row=0, column=0)
            #Check the current page
            self.check_page()
        
        elif direction > 0 and self.current_page < 8:
                self.back_button.grid()
                self.buttonplaceholder.grid_remove()
                #Remove current page from main_content_frame
                self.pages[self.current_page - 1].grid_remove()
                self.current_page +=1
                #Set main_content_frame based on current page
                self.pages[self.current_page - 1].grid(row=0, column=0)
                #Check the current page
                self.check_page()
        else:
            self.exit_handler()
        

        print("Current Page:", self.current_page)

    def radio_button_changes(self, accept_state):
        '''Sets the state of the next button depending
        on the state of the radio button(Prevents
        further progress without license agreement'''
        if accept_state == 0 and self.current_page > 1:
            self.next_button.config(state=DISABLED)
        else:
            self.next_button.config(state=NORMAL)

    def config_install_dir(self):
        '''Sets the default install directory based on Operating System'''
        directory = ''
        #Windows platform
        if self.platform == 'win32':
            directory = 'C:\\Program Files\\habit'
        #Mac OS X and Linux
        else:
            directory = '/usr/bin/habit'
        return os.path.abspath(directory)

    def set_ready_install_text(self):
        '''Configures and sets the text of the installation_ready_text box'''
        self.installation_ready_text.config(state=NORMAL)
        line_1 = 'Destination location:'
        line_2 = ' '*3 + self.installation_directory

        #Clear installation ready text before inserting updated information
        self.installation_ready_text.delete(1.0, END)
        self.installation_ready_text.insert(END, line_1 + '\n' + line_2)
        self.installation_ready_text.config(state=DISABLED)

    def get_file_dialog(self):
        '''Displays a file dialog for the user to select
        an install directory. If the user presses cancel, 
        the value is set to the default(subject to change)'''
        #Use a dialog to get user-input on directory 
        result = fdialog.askdirectory(parent=self.parent, title='Browse for folder')    

        #If user cancels out of file dialog, path will be empty
        if len(result) > 0:
            self.installation_directory = os.path.abspath(result)

        else:
            self.installation_directory = self.config_install_dir()[:-5]
        
        self.installation_directory+='\habit'
        self.installation_directory = os.path.abspath(self.installation_directory)
        
        #Set directory entry text to self.directory
        self.directory_selection_entry.delete(0, END)
        self.directory_selection_entry.insert(0, self.installation_directory)
        print(self.installation_directory)
    
    def set_platform(self):
        '''Sets self.platform to the platform of the current system'''
        return os.sys.platform

    def get_root_path(self):
        '''Returns the root path of the installer. On Windows, 
        its the current user's desktop. On UNIX systems, its 
        the home directory f the current user.'''
        
        root_path = ''
        #Windows platform
        if self.platform == 'win32':
            path_string = 'C:\\Users\\'+getpass.getuser()+'\\Desktop\\Test\\'
            root_path = os.path.abspath(path_string) + '\\'
        #Mac OS X and Linux
        else:
            root_path = os.path.abspath('') + '/'
        return root_path

    def complete_installation(self):
        if self.run_postinstall.get() == 1:
            print('Running...')
            self.run_executable()
        else:
            print('Dont run!')
        #Call exit handler
        self.exit_handler()

    def set_executable_name(self):
        '''Sets the executable name'''
        if self.platform == "win32":
            return "habit.exe"
        elif self.platform == "linux":
            return "habit"
        else:
            return "habit.app"

    def run_executable(self):
        '''Runs the executable in a platform-specific protocol. Until
        executables are made, the installer will just invoke:
        >python habit.py, or whatever the main executable is titled
        
        executable_path = os.path.abspath(self.installation_directory + 
                                          '\\' + self.executable_name)
        print(executable_path)

        if self.platform == "win32":
            subprocess.Popen([executable_path])

        elif self.platform == "linux":
            subprocess.Popen(['xdg-open', executable_path])
                             
        else:
            subprocess.Popen(['open', executable_path])
        '''
        exec_path = os.path.abspath(self.installation_directory + '\\' + 'landing_page.py')
        #print(os.path.abspath(self.installation_directory + '\\' + 'landing_page.py'))
        
        if self.platform == "win32":
            subprocess.Popen([os.sys.executable, exec_path])
        else:
            #Active Tcl uses python3.3; tile not present in python3.4 tkinter package
            subprocess.Popen(['python3.3', exec_path])

    def exit_handler(self):
        '''Exit handler to control exit events on the root window'''
        if not self.installing:
            self.parent.destroy()
            self.parent.quit()
  
root = Tk()
app = Installer_GUI(root, "Habit Installer")
root.mainloop()



