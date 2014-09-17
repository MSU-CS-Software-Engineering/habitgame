README.txt

To properly setup installer.py:
1. Make a directory on your Desktop called 'Install' to hold the installation 
   files. This is what the installer will look for(See note for customization)
2. Copy installer.py, setup.ico, EULA.txt into your created directory
3. Create a directory inside of your newly created directory for
   an assets_folder. Name is customizable
4. Copy 'landing_page.py' from GitHub to the assets_folder
5. Make a text file called 'install_instructions.txt'
6. Here's how to configure install_instructions.txt
   a.) Line 1 of the file MUST be the string: asset_folder=foldername,
	   where foldername is user defined. This folder is where all of your installation
	   files will be stored before being copied to the destination directory 
   b.) Line 2 of the file MUST be the string: num_directories=number,
	   where number is the number of directories that will be created in the destination
	   directory during installation
   c.) Line 3 of the file MUST be the string: num_files=number, where number
	   is the number of files in the asset_folder that will be copied during
	   installation
   d.) The next |num_directories| of lines MUST be the names of the directories
       that will be created during installation
   e.) The next |num_files| of lines MUST be the names of the files in the asset_folder
	   that will be copied during installation
   ----The file lines MUST be in the following format:
       filename:destination_directory
	   destination_directory MUST be in the list of directories and filename must be the 
	   name of a valid file in the asset_folder
	   If destination_directory is 'root'(without quotations), then the file which just be 
	   installed in the default destination directory, chosen during install

**Note**
To use a different original directory to hold the install files, 
change the path_string variable in def get_root_path() in the installer_gui 
class. It defaults to the user's desktop on Windows, but you can customize
this for your own testing purposes.The string has the following format:
	'C:\\Users\\Johnny\\Desktop\\Install\\'
 	   
After setup is properly configured, run python installer.py. If you're on a mac, I've had
bugs with python3.4 and some Tk elements(notably anything belonging to ttk), so python3.3 
should work

Ex. $>python3.3 installer.py

Make sure to integrate the landing page, you have an asset_folder created with landing_page.py 
in it. This is will ensure proper functionality.

**Note**
Mac compatibility has some bugs(repairs pending)
	   
========SAMPLE========
asset_folder=assets
num_directories=3
num_files=12 
config
character_data
savedata
habit.exe:config
body.png:character_data
head.png:character_data
banner.png:config
logo.png:config
1.png:character_data
landing_page.py:root
2.png:character_data
3.png:character_data
config.txt:config
local.xml:savedata
cloud.xml:savedata