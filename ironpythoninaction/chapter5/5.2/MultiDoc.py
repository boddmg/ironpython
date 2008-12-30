import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Xml')

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

from savecommands import SaveCommand, SaveAsCommand
from model import Document, Page
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

        doc = self.document = Document()
        self.tabController = TabController(tab, doc)
        
        self.initialiseCommands()
        self.initialiseToolbar()
        self.initialiseMenus()

        
    def initialiseCommands(self):
        tabC = self.tabController
        doc = self.document
        self.saveCommand = SaveCommand(doc, tabC)
        self.saveAsCommand = SaveAsCommand(doc, tabC)


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
        
        self.addToolbarItem('Save', 
                            lambda sender, event: self.saveCommand.execute(),
                            'save_16.ico')
        self.Controls.Add(self.toolBar)
        

Application.EnableVisualStyles()
Application.Run(MainForm())
