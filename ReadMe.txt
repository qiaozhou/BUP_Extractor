BUPextractor
https://github.com/qiaozhou/BUP_Extractor

WARNING in no way we can be responsible of a misusage or any loss that could happen during your experience with this tool, there is no warranty and must be use only as an educational purpose.

Summary:
	This tool is intended to help you to recover files.
	You can't recover McAfee quarantined files because your subscription is over, or because you don't find anything under McAfee user interface.

1- Copy quarantined files, and sort it to reduce
	Notes: folder which contains your files depends on your OS
	under windows XP:
	C:\documents and settings\all users\application data\mcafee\virusscan\quarantine
	under windows 7:
	C:\programdata\mcafee\virusscan\quarantine

	it's recommended that user first copy/backup files (sorted by size iis a good idea) to avoid any loss,
   a copy/backup divided by group of 100 BUP files per folder  would avoid long slow down to run this tool (files with biggest size are usualy those you are looking for).

2- Start this tool, click on menu File\Open Folder and select the folder with BUP files
	Note: Organize folders with 100 BUP files, it can help a lots to go forward step by step in your recovery.

3- A list of file appear with original file location, Tick the checkbox of files you want to recover.
	Note: you can select multiple lines with the cursor then click on Tick or UnTick to apply the action on group of files.
	Even better you can use filter to see only the files you are looking for, you can either tick 1 by 1 or using a selection to go faster.
	Ctrl+ A  select all visible lines when the widget got the focus.

4- Click on Restore, it will recover all ticked files to the destination folder.

	Note: if McAfee or other antivirus is still running, restored files potentialy will be quarantined again!
	You must first Disable,Stop or Remove your antivirus, but you may be in danger! Usage of a VMware/VirtualBox or any virtual PC to operate the recovery would be more safe if you are not sure about what you are doing.

Note: if you met some trouble to remove McAfee you can use their own removal tool
http://download.mcafee.com/products/licensed/cust_support_patches/MCPR.exe


In few words to understand what does BUPextractor tools:
The process done to extract files from Quarantine (.BUP) files:

     Using Windows Explorer, create a temporary folder. In this example: C:\SAVE-BUP
     Download the 7-Zip file compression utility from http://www.7-zip.org/.
     Install the 7-Zip utility and extract the following two files from the .BUP file to C:\SAVE-BUP
 
     Details
         File_0  To decrypt files contained in .BUP files:
        Download the XOR utility from http://www.softpedia.com/get/Programming/Other-Programming-Files/Xor.shtml.
        Extract xor.zip to C:\SAVE-BUP.
        Click Start, Run, type cmd, and press ENTER.
        Type cd  \SAVE-BUP and press ENTER.
        Type xor.exe  File_0 file_0.xor  0X6A and press ENTER.
        Type xor.exe  Details Details.txt  0X6A and press ENTER.
        NOTE: 0x6A is the encryption key used.
        Rename File_0.xor to the original name found in the Details file.
