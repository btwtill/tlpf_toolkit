# USER TOOLKIT v.1.0
*Tim Coleman - tim.coleman.3d@gmail.com*

Welcome to this User's Toolkit. 


##
##Installation
- Download the `user_toolkit.zip` file and unzip it.  
- Inside the `user_toolkit` folder that was unzipped, there will be another `user_toolkit` folder.  Copy and paste that folder into your `<USER>/Documents/maya/scripts/` directory.   
- Launch Maya. 
- Once in Maya, open the Script Editor and run the following code to see if the toolkit was installed correctly.
#

    import user_toolkit
    user_toolkit.run_test()
You should see a "True" or a installation successful message if it was successful.

##
## Utility Script Library
Contain various Python scripts with functions to aid various tasks in Maya.



##
## Custom Shelf
Custom Maya tool shelf for quick access to often used utility functions and tools.
#### To Load Custom Maya Tool shelf
    from user_toolkit.shelves import shelf_user_utils
    reload(shelf_user_utils)
    shelf_user_utils.load(name="user_utils")


#### Automatically load shelf at Maya startup
Add these lines to your `<USER>/Documents/maya/scripts/userSetup.py` file

    import maya.utils
    
    # Load Custom User Shelf at Maya startup
    from user_toolkit.shelves import shelf_user_utils
    
    def load_user_shelf():
    	shelf_user_utils.load(name="user_utils")
    	
    maya.utils.executeDeferred("load_user_shelf()")


##
## Custom Marking Menu
Custom Maya Marking Menu for quick access to often used utility functions and tools.  Use RMB + CTL + ALT to invoke marking menu in Maya.
#### To Load Custom Marking menu
    from user_toolkit.marking_menu import user_marking_menu
    reload(user_marking_menu)
    user_marking_menu.markingMenu()
##



