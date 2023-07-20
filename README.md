# ISO_COMBINER

## Purpose
Combines game files in format of .iso on Windows machines. Launch the application to select and combine as many iso files as you want. This will work for multiple game files at the same time.

## Prerequistes and important information
1. This only works on Windows machines
2. The program creates copies of .iso files in order to combine them and save them on your machine. Please ensure you have enough memory available on your machine to succesfully combine the .iso files.
3. All .iso files from the same game must have the same GAMEID in the file name.

Example of files from the same game:
```
GAME1.part0.iso and GAME1.part1.iso 
```
Example of files from another game:
```
GAME1_RATS_R_COOL.part0.iso and GAME1_RATS_R_COOL.part1.iso 
```
If all of these files are selected, the end result of combining would be: 
```
GAME1.COMBINED.iso and GAME1_RATS_R_COOL.COMBINED.iso
```

## Instructions for running ISO_COMBINER application
These instructions explain the process to run the ISO_Combiner.exe application.

1. Download the ISO_Combiner.exe file from this repo. Use the latest version available for best results.

2. Launch the application on your windows machine. A window should pop up with instructions.

3. Click the "Browse" button to select the .iso files that you want to combine. The selected file paths will be displayed in the window. Use the "Clear" button to remove unwanted paths from the window.

4. Click the "Combine" button to combine the selected files. Only files from the same games will be combined together (see #3 under Prerequisites and important information for details)

5. The resulting combined .iso files will automatically be loaded into the path of the first file selected for each game.

6. After loading, a message box will display a success/failure message confirming if the .iso files have been combined successfully.

*NOTE: If the new combined ".iso" has "0 bytes" or is not displaying in your file explorer properly, please refresh or close and reopen your file explorer. If the ".iso" is on your Desktop, right click and select the "refresh" button.*

*NOTE: If there are any errors or if you attempt to combine less than two ".iso" files, an error message will be displayed.*


### Special thanks to my amazing wife for contributing to and cleaning up the code
