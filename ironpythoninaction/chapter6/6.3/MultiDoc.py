import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Xml')
clr.AddReference('RenameTabDialog')

from System.Drawing import Color, Size
from System.IO import File, Path
from System.Runtime.Serialization.Formatters.Binary import BinaryFormatter
from System.Windows.Forms import (
    Application, DockStyle, Form,
    Keys, MenuStrip, 
    TabAlignment, TabControl, 
    ToolStripItemDisplayStyle, ToolStrip,
    ToolStripButton, ToolStripGripStyle,
    ToolStripMenuItem
)

from model import Document, Page
from newdocumentcommand import NewDocumentCommand
from opencommand import OpenCommand
from savecommands import SaveCommand, SaveAsCommand
from tabcommands import NewPageCommand, RemoveCommand, RenameCommand
from tabcontroller import TabController


executablePath = __file__
if executablePath is None:
    executablePath = Application.ExecutablePath
executableDirectory = Path.GetDirectoryName(executablePath)


class MainForm(Form):
    def __init__(self):
        Form.__init__(self)
        self.Text = 'MultiDoc Editor'
        self.MinimumSize = Size(150, 150)
        self.iconPath = Path.Combine(executableDirectory, 'icons')
        self.Icon = self.loadImage('copy_clipboard_16.dat')
        
        tab = self.tabControl = TabControl()
        self.tabControl.Dock = DockStyle.Fill
        self.tabControl.Alignment = TabAlignment.Bottom
        self.Controls.Add(self.tabControl)

        self.tabController = TabController(tab)
        
        self.initialiseCommands()
        self.initialiseToolbar()
        self.initialiseMenus()
        self.initialiseObservers()
        self.document = Document()

    def loadImage(self, filename):
        path  = Path.Combine(self.iconPath, filename)
        stream = File.OpenRead(path)
        image = BinaryFormatter().Deserialize(stream)
        stream.Close()
        return image
        
        
    def initialiseCommands(self):
        tabC = self.tabController
        self.saveCommand = SaveCommand(tabC)
        self.saveAsCommand = SaveAsCommand(tabC)
        self.openCommand = OpenCommand(self)
        self.newPageCommand = NewPageCommand(tabC)
        self.removeCommand = RemoveCommand(tabC)
        self.renameCommand = RenameCommand(tabC)
        self.newDocumentCommand = NewDocumentCommand(tabC)


    def initialiseObservers(self):
        self.observers = [
            self.saveCommand,
            self.saveAsCommand,
            self.tabController
        ]


    def createMenuItem(self, text, handler=None, keys=None):
        menuItem = ToolStripMenuItem()
        menuItem.Text = text

        if keys:
            menuItem.ShortcutKeys = keys
        if handler:
            menuItem.Click += handler
        return menuItem


    def initialiseMenus(self):
        menuStrip = MenuStrip()
        menuStrip.Dock = DockStyle.Top

        fileMenu = self.createMenuItem('&File')
        
        openKeys = Keys.Control | Keys.O
        openMenuItem  = self.createMenuItem(
            '&Open...', 
            lambda sender, event: self.openCommand.execute(),
            keys=openKeys
        )
        
        newKeys = Keys.Control | Keys.N
        newMenuItem  = self.createMenuItem(
            '&New', 
            lambda sender, event: self.newDocumentCommand.execute(),
            keys=newKeys
        )
        
        saveKeys = Keys.Control | Keys.S
        saveMenuItem  = self.createMenuItem(
            '&Save...', 
            lambda sender, event: self.saveCommand.execute(),
            keys=saveKeys
        )

        saveAsKeys = Keys.Control | Keys.Shift | Keys.S
        saveAsMenuItem  = self.createMenuItem(
            'S&ave As...', 
            lambda sender, event: self.saveAsCommand.execute(),
            keys=saveAsKeys
        )
        
        fileMenu.DropDownItems.Add(newMenuItem)
        fileMenu.DropDownItems.Add(openMenuItem)
        fileMenu.DropDownItems.Add(saveMenuItem)
        fileMenu.DropDownItems.Add(saveAsMenuItem)
        
        editMenu = self.createMenuItem('&Edit')
        
        newPageItem  = self.createMenuItem(
            '&New Page...', 
            lambda sender, event: self.newPageCommand.execute()
        )
        renamePageItem  = self.createMenuItem(
            '&Rename Page...', 
            lambda sender, event: self.renameCommand.execute()
        )
        removePageItem  = self.createMenuItem(
            'Remove &Page...', 
            lambda sender, event: self.removeCommand.execute()
        )

        editMenu.DropDownItems.Add(newPageItem)
        editMenu.DropDownItems.Add(renamePageItem)
        editMenu.DropDownItems.Add(removePageItem)

        menuStrip.Items.Add(fileMenu)
        menuStrip.Items.Add(editMenu)
        self.Controls.Add(menuStrip)
        
        
    def addToolbarItem(self, name, clickHandler, iconFile):
        button = ToolStripButton()
        button.Image = self.loadImage(iconFile)
        button.ImageTransparentColor = Color.Magenta
        button.ToolTipText = name
        button.DisplayStyle = ToolStripItemDisplayStyle.Image
        button.Click += clickHandler
        
        self.toolBar.Items.Add(button)
    
    
    def initialiseToolbar(self):
        self.toolBar = ToolStrip()
        self.toolBar.Dock = DockStyle.Top
        self.toolBar.GripStyle = ToolStripGripStyle.Hidden
        
        self.addToolbarItem('New', 
                            lambda sender, event: self.newDocumentCommand.execute(), 
                            'new_document_16.dat')
        self.addToolbarItem('Open', 
                            lambda sender, event: self.openCommand.execute(), 
                            'open_document_16.dat')
        self.addToolbarItem('Save', 
                            lambda sender, event: self.saveCommand.execute(), 
                            'save_16.dat')
        self.addToolbarItem('New Page', 
                            lambda sender, event: self.newPageCommand.execute(), 
                            'plus.dat')
        self.addToolbarItem('Remove Page', 
                            lambda sender, event: self.removeCommand.execute(), 
                            'delete_x_16.dat')
        self.Controls.Add(self.toolBar)
        
        
    def _setDocument(self, document):
        self._document = document
        for observer in self.observers:
            observer.document = document
    
    document = property(lambda self: self._document, _setDocument)


Application.EnableVisualStyles()
Application.Run(MainForm())
