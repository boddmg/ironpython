from System.Windows.Forms import (
    DockStyle, ScrollBars, 
    TabPage, TextBox
)


class TabController(object):

    def __init__(self, tabControl):
        self.tabControl = tabControl
        self._document = None
        
        
    def _setDocument(self, document):
        if self._document is not None:
            self.tabControl.SelectedIndexChanged -= self.maintainIndex
            
        self._document = document
        self.tabControl.TabPages.Clear()
        for page in document:
            self.addTabPage(page.title, page.text)
            
        self.index = self.tabControl.SelectedIndex
        if self.index == -1:
            self.index = self.tabControl.SelectedIndex = 0
        self.tabControl.SelectedIndexChanged += self.maintainIndex
        
    document = property(lambda self: self._document, _setDocument)
    
    
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
        if not self.hasPages:
            return
        if self.index < len(self.tabControl.TabPages):
            self.updateDocument()
        self.index = self.tabControl.SelectedIndex
        
        
    def updateDocument(self):
        if not self.hasPages:
            return
        index = self.index
        tabPage =  self.tabControl.TabPages[index]
        textBox = tabPage.Controls[0]
        self.document[index].text = textBox.Text


    def deletePage(self):
        if not self.hasPages:
            return
        index = self.tabControl.SelectedIndex
        del self.document[index]
        tabPage = self.tabControl.SelectedTab
        self.tabControl.TabPages.Remove(tabPage)
        
    hasPages = property(lambda self: self.tabControl.SelectedIndex != -1)
    
    
    def _getCurrentPageTitle(self):
        if not self.hasPages:
            return None
        index = self.tabControl.SelectedIndex
        return self.document[index].title
    
    
    def _setCurrentPageTitle(self, title):
        if not self.hasPages:
            return
        index = self.tabControl.SelectedIndex
        page = self.document[index]
        page.title = title
        self.tabControl.SelectedTab.Text = title
        
    currentPageTitle = property(_getCurrentPageTitle, _setCurrentPageTitle)
    
    
    def newPage(self, title):
        self.document.addPage(title)
        self.addTabPage(title, "")
        newPageIndex = len(self.tabControl.TabPages) - 1
        self.tabControl.SelectedIndex = newPageIndex
    