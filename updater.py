'''
  Updater

  Dependencies: requests.py   
  -url: http://docs.python-requests.org/en/latest/user/install/#install
                
'''

import requests
import shutil
import os 

from tkinter import *
from tkinter.font import Font, nametofont
from tkinter.ttk import Progressbar, Button
import threading
from tkinter import messagebox  #Must be explicitly imported. Used for placeholders.

     
class Downloader():
    def __init__(self, url):
        self.window = Toplevel()
        self.window.title("Download")
        self.pbar_state = IntVar()
        #self.window.resizable(width=FALSE, height=FALSE)
        self.window.minsize(width=350, height=200)
        self.window.maxsize(width=350, height=200)        
        self.window.protocol("WM_DELETE_WINDOW", self.quit_updater)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=2)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_rowconfigure(4, weight=1)
        self.window.grid_rowconfigure(5, weight=1)
        self.window.grid_rowconfigure(6, weight=1)
        
        self.download_text_label = Label(self.window,
                                         text = "Downloading")

        self.download_progress_label = Label(self.window,
                                         text = "")

        
        default_font = nametofont("TkDefaultFont")
        
        default_font.configure(size=10)

        progress_text_font = Font(family='Helvetica',
                                  size = 8,
                                  weight='bold')
        
        self.download_text_label.configure(font = progress_text_font)
        self.download_text_label.grid(row=1, column=0,
                                      sticky='ew', columnspan=2)
        self.download_progress_label.grid(row=5, column=0, columnspan=2)
        self.download_progress_label.configure(font = progress_text_font)
        self.progress_bar = Progressbar(self.window,
                                            orient = "horizontal",
                                            length = 200,
                                            mode = "indeterminate")
        self.progress_bar.grid(row=3, column=0, columnspan=2)

        self.cancel_button = Button(self.window,
                                 text="Cancel",
                                 command=self.cancel_download)
        
        self.cancel_button.grid(row=6, column=0, columnspan=2)
        
        self.center_window()
        
        self.url = url
        self.bytes_read = 0
        self.max_bytes = 0
        self.local_filename = url.split('/')[-1]
        self.start_download()
        
    def center_window(self):
        self.window.update_idletasks()
        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()
        
        
        x = (self.window.winfo_screenwidth() // 2) - \
            (self.width // 2)
        y = (self.window.winfo_screenheight() // 2) - \
            (self.height // 2)
        
        self.window.geometry('{}x{}+{}+{}'.format(self.width,
                                           self.height,
                                           x, y))
        self.window.update()

    def start_download(self):
        self.download = True
        self.thread = threading.Thread(target=self.download_file)
        self.thread.start()
        self.callback()
        
    def callback(self):
        self.progress_bar.step(5)
        if self.thread.is_alive():
            self.window.after(25, self.callback)
        else:
            if self.download:
                self.finished_downloading()

            else:
                self.download_error()

    def download_error(self):
        self.progress_bar['value'] = 0
        self.download_progress_label.configure(text="Download cancelled")
        self.cleanup()
        
    def finished_downloading(self):
        self.progress_bar.configure(mode = "determinate")
        self.progress_bar['value'] = 100

        
        #Cleanup
        try:
            shutil.copyfile('partial_download', self.local_filename)
            self.cleanup()
            
        except:
            messagebox.showerror("File Error", "Couldn't copy file. Aborting")
                    
    def download_file(self):
        r = requests.get(self.url, stream=True)

        f =  open('partial_download', 'wb')
        for chunk in r.iter_content(chunk_size=1024):
            if self.download:
                if chunk:
                    f.write(chunk)
                    f.flush()
            else:
                break
            
        f.close()
        

    def cleanup(self):
        '''
        Cleans up temp files created during download
        '''
        
        self.cancel_button.config(state='disabled')
        try:
            os.remove('partial_download')
            
        except:
            pass
            #messagebox.showerror("File Error", "Couldn't remove partial download file")

        self.window.destroy()
       
    def cancel_download(self):
        response = messagebox.askyesno("Cancel", "Are you sure?")

        if response:
            print("Download cancelled")
            self.download = False
            self.cleanup()
            self.window.destroy()
            
        else:
            pass

    def quit_updater(self):
        self.download = False
        self.cleanup()
        self.window.destroy()
        

class Updater:
    def __init__(self, current_version, master):
        self.current_version  = current_version
        self.master = master
        
        
    def check_update(self):
        '''
        Checks the repository to see if a program
        update is available for download.
        '''

        url = 'https://github.com/MSU-CS-Software-Engineering/habitgame/raw/Development/Upgrade%20Message'

        #try:
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            current_release_version = float(r.text.split(' ')[2])
            current_program_version = self.current_version
            #Check to see if current_release is newer

            if current_release_version > current_program_version:
                message = "Version "+str(current_release_version)+ \
                          " is available. Download?"

                self.master.withdraw()
                response = messagebox.askokcancel("Version Update",
                                              message)
                if response:
                    self.download_release(current_release_version)
                
                else:
                    pass

            else:
                pass

        else:
            error_message = 'Request error ' + r.status_code

        #except:
        #    messagebox.showwarning("Timeout",
        #                           "Request timed out")


    
    def download_release(self, release_version):
        '''
        Downloads a release if it's available
        '''

        try:
            platform = os.sys.platform

            if platform == 'win32':
                url = 'https://github.com/twilliams1832/Test-repo/releases/download/'+str(release_version)+'/DailyHackInstaller.exe'

            elif platform == 'linux':
                url = 'https://github.com/twilliams1832/Test-repo/releases/download/'+str(release_version)+'/DailyHackInstaller.tar.gz'

            else:
                url = 'https://github.com/twilliams1832/Test-repo/releases/download/'+str(release_version)+'/DailyHackInstaller.dmg'

            release_downloader = Downloader(url)

        except:
            print("Error in downloading release")
            return -1 


if __name__ == "__main__":
    
    import doctest
    doctest.testmod()
    root = Tk()
    root.withdraw()
    software_updater = Updater(1.0)
    root.mainloop()
