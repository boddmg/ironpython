import clr

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Drawing import Icon
from System.Windows.Forms import (
    Application, ContextMenu, 
    MenuItem, NotifyIcon, ToolTipIcon
)

from System.IO import FileSystemWatcher

import os

this_dir = os.path.dirname(
    os.path.abspath(__file__)
)
    
class Main(object):

    def __init__(self):
        self.init_notify_icon()
        
        watcher = FileSystemWatcher()
        watcher.Path = this_dir
        def handle(w, a): 
            self.notify_icon.ShowBalloonTip(
                10, str(a.ChangeType), 
                a.FullPath, ToolTipIcon.Warning
            )
            
        watcher.Changed += handle
        watcher.Created += handle
        watcher.Deleted += handle
        watcher.EnableRaisingEvents = True


    def init_notify_icon(self):
        self.notify_icon = NotifyIcon()
        self.notify_icon.Icon = Icon("test.ico")
        self.notify_icon.Visible = True
        self.notify_icon.ContextMenu = self.init_context_menu()

    
    def onTick(self, sender, event):
        self.notify_icon.BalloonTipTitle = "Hello, I'm IronPython"
        self.notify_icon.BalloonTipText = "Who are you?"
        self.notify_icon.ShowBalloonTip(1000)

        
    def init_context_menu(self):
        context_menu = ContextMenu()
        exit_menu_item = MenuItem("Exit")
        exit_menu_item.Click += self.on_exit
        context_menu.MenuItems.Add(exit_menu_item)
        return context_menu
        

    def on_exit(self, sender, event):
        self.notify_icon.Visible = False
        Application.Exit()     
   
        
if __name__ == "__main__":
    main = Main()
    Application.Run()
