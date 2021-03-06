import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import Bitmap, Color, Size
from System.IO import Directory, Path, StreamWriter
from System.Windows.Forms import (
    Application, DialogResult, DockStyle, Form,
    Keys, MenuStrip, MessageBox, MessageBoxButtons, 
    MessageBoxIcon,
    ScrollBars, SaveFileDialog, TabAlignment, 
    TabControl, TabPage, TextBox, 
    ToolStripItemDisplayStyle, ToolStrip,
    ToolStripButton, ToolStripGripStyle,
    ToolStripMenuItem
)

executablePath = __file__
if executablePath is None:
    executablePath = Application.ExecutablePath
executableDirectory = Path.GetDirectoryName(executablePath)


class Document(object):
    def __init__(self, fileName=None):
        self.fileName = fileName
        self.pages = []
        self.addPage()
            
    def addPage(self, title='New Page'):
        page = Page(title) 
        self.pages.append(page)

    def __getitem__(self, index):
        return self.pages[index]

    def __setitem__(self, index, page):
        self.pages[index] = page

    def __delitem__(self, index):
        del self.pages[index]


class Page(object):
    def __init__(self, title):
        self.title = title
        self.text = ''


class TabController(object):

    def __init__(self, tabControl, document):
        self.tabControl = tabControl
        self.document = document
        
        for page in document:
            self.addTabPage(page.title, page.text)
        
        self.index = self.tabControl.SelectedIndex
        if self.index == -1:
            self.index = self.tabControl.SelectedIndex = 0
        self.tabControl.SelectedIndexChanged += self.maintainIndex
        
        
    def addTabPage(self, label, text):
        tabPage = TabPage()
        tabPage.Text = label

        textBox = TextBox()
        textBox.Multiline = True
        textBox.Dock = DockStyle.Fill
        textBox.ScrollBars = ScrollBars.Vertical
        textBox.AcceptsReturn = True
        textBox.AcceptsTab = True
        textBox.WordWrap = True
        textBox.Text = text

        tabPage.Controls.Add(textBox)
        
        self.tabControl.TabPages.Add(tabPage)


    def maintainIndex(self, sender, event):
        self.updateDocument()
        self.index = self.tabControl.SelectedIndex


    def updateDocument(self):
        index = self.index
        tabPage =  self.tabControl.TabPages[index]
        textBox = tabPage.Controls[0]
        self.document[index].text = textBox.Text


filter = 'Text files (*.txt)|*.txt|All files (*.*)|*.*'

class SaveCommand(object):
    
    title = "Save Document"
    
    def __init__(self, document, tabController):
        self.document = document
        self.tabController = tabController
        self.saveDialog = SaveFileDialog()
        self.saveDialog.Filter = filter
        self.saveDialog.Title = self.title
    
    
    def execute(self):
        fileName = self.document.fileName
        text = self.getText()
        
        directory = Path.GetDirectoryName(fileName)
        directoryExists = Directory.Exists(directory)
        if fileName is None or not directoryExists:

            self.promptAndSave(text)
        else:
            self.saveFile(fileName, text)


    def getText(self):
        self.tabController.updateDocument()
        return self.document[0].text
        
        
    def promptAndSave(self, text):
        saveDialog = self.saveDialog
        if saveDialog.ShowDialog() == DialogResult.OK:
            fileName = saveDialog.FileName
            if self.saveFile(fileName, text):
                self.document.fileName = fileName
        
        
    def saveFile(self, fileName, text):
            try:
                writer = StreamWriter(fileName)
                writer.Write(text)
                writer.Close()
                return True
            except IOError, e:
                name = Path.GetFileName(fileName)
                MessageBox.Show(
                    'Could not write file "%s"\r\nThe error was:\r\n%s' %
                        (name, str(e)),
                    "Error Saving File",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                )
                return False


class SaveAsCommand(SaveCommand):
    
    title = "Save Document As"

    def execute(self):
        fileName = self.document.fileName
        text = self.getText()
        if fileName is not None:    
            name = Path.GetFileName(fileName)
            directory = Path.GetDirectoryName(fileName) 
            self.saveDialog.FileName = name
            if Directory.Exists(directory):
                self.saveDialog.InitialDirectory = directory
        
        self.promptAndSave(text)


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
