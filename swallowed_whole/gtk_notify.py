import clr

clr.AddReference("gtk-sharp")
clr.AddReference("gdk-sharp")

import os
import Gtk
import Gdk
from System.IO import FileSystemWatcher

this_dir = os.path.dirname(os.path.abspath(__file__))
MSG = 'Change Type: %s\n\nFull Path: %s'


class Main(object):

    def __init__(self):
        self.init_notify_icon()
        
        watcher = FileSystemWatcher()
        watcher.Path = this_dir
            
        watcher.Changed += self.show_notification
        watcher.Created += self.show_notification
        watcher.Deleted += self.show_notification
        watcher.EnableRaisingEvents = True

    def init_notify_icon(self):
        self.window = Gtk.Window('Directory watcher')
        self.window.Hide()
        
        icon = Gdk.Pixbuf("test.ico")
        self.notify_icon = Gtk.StatusIcon(icon)
        self.notify_icon.Visible = True
        self.notify_icon.PopupMenu += self.show_context_menu
        self.notify_icon.Tooltip = 'Directory watcher'
        
    def show_context_menu(self, sender, event):
        context_menu = Gtk.Menu()
        exit_menu_item = Gtk.MenuItem("Exit")
        exit_menu_item.Activated += self.on_exit
        context_menu.Add(exit_menu_item)
        context_menu.ShowAll()
        context_menu.Popup()

    def show_notification(self, sender, event):
        def show_dialog(*args):
            dialog = Gtk.MessageDialog(
                self.window, Gtk.DialogFlags.Modal,
                Gtk.MessageType.Warning, Gtk.ButtonsType.None,
                MSG % (event.ChangeType, event.FullPath)
            )
            dialog.Run()
            dialog.Destroy()
        Gtk.Application.Invoke(show_dialog)

    def on_exit(self, sender, event):
        self.notify_icon.Visible = False
        Gtk.Application.Quit()    
   
        
if __name__ == "__main__":
    Gtk.Application.Init()
    main = Main()
    Gtk.Application.Run()
