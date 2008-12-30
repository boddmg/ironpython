import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Xml')
clr.AddReference('RenameTabDialog')

from System.Drawing import Bitmap, Color, Size
from System.IO import Path
from System.Windows.Forms import (
    Application, DockStyle, Form,
    Keys, MenuStrip, 
    TabAlignment, TabControl, 
    ToolStripItemDisplayStyle, ToolStrip,
    ToolStripButton, ToolStripGripStyle,
    ToolStripMenuItem
)

from model import Document, Page
from opencommand import OpenCommand
from savecommands import SaveCommand, SaveAsCommand
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

        
    def initialiseCommands(self):
        tabC = self.tabController
        self.saveCommand = SaveCommand(tabC)
        self.saveAsCommand = SaveAsCommand(tabC)
        self.openCommand = OpenCommand(self)


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
        
        fileMenu.DropDownItems.Add(openMenuItem)
        fileMenu.DropDownItems.Add(saveMenuItem)
        fileMenu.DropDownItems.Add(saveAsMenuItem)
        
        menuStrip.Items.Add(fileMenu)
        self.Controls.Add(menuStrip)
        
        
    def addToolbarItem(self, name, clickHandler, iconFile):
        button = ToolStripButton()
        button.Image = Bitmap(Path.Combine(self.iconPath, iconFile))
        button.ImageTransparentColor = Color.Magenta
        button.ToolTipText = name
        button.DisplayStyle = ToolStripItemDisplayStyle.Image
        button.Click += clickHandler
        
        self.toolBar.Items.Add(button)
    
    
    def initialiseToolbar(self):
        self.iconPath = Path.Combine(executableDirectory, 'icons')
        self.toolBar = ToolStrip()
        self.toolBar.Dock = DockStyle.Top
        self.toolBar.GripStyle = ToolStripGripStyle.Hidden
        
        self.addToolbarItem('Open', 
                            lambda sender, event: self.openCommand.execute(), 
                            'open_document_16.ico')
        self.addToolbarItem('Save', 
                            lambda sender, event: self.saveCommand.execute(), 
                            'save_16.ico')
        self.Controls.Add(self.toolBar)
        
        
    def _setDocument(self, document):
        self._document = document
        for observer in self.observers:
            observer.document = document
    
    document = property(lambda self: self._document, _setDocument)

Application.EnableVisualStyles()
Application.Run(MainForm())
