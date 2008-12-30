
class PageState(object):
    pass
     
self = PageState()
self.document = None
self.currentPage = None
self.editing = False


from System.Web.UI import Pair
import pickle

def ScriptLoadViewState(state):
    self.document, self.currentPage, self.editing = pickle.loads(state.Second)
    return state.First


def ScriptSaveViewState(baseState):
    state = Pair()
    state.First = baseState
    state.Second = pickle.dumps((self.document, self.currentPage, self.editing))
    return state
    

from documentreader import DocumentReader
from documentwriter import DocumentWriter

DOCUMENT_FILE = "doc.xml"

def getDocument():
    reader = DocumentReader(Page.MapPath(DOCUMENT_FILE))
    return reader.read()
    
    
def saveDocument(document):
    writer = DocumentWriter(Page.MapPath(DOCUMENT_FILE))
    writer.write(document)
    
    
def getPage(document, name):
    matches = [page for page in document.pages if page.title == name]
    if matches:
        return matches[0]
    return None
    

def Page_Load(sender, event):
    if not IsPostBack:
        self.document = getDocument()
        self.currentPage = None
        self.editing = False


def Page_PreRender(sender, event):
    pageRepeater.DataSource = self.document.pages
    pageRepeater.DataBind()
    viewPanel.Visible = self.currentPage and not self.editing
    editPanel.Visible = self.editing
    
    if self.currentPage:
        selectedPage = getPage(self.document, self.currentPage)
        pageTitle.Text = pageTitleTextBox.Text = selectedPage.title
        pageContent.Text = pageContentTextBox.Text = selectedPage.text
        

def pageLink_Click(sender, event):
    self.currentPage = sender.Text


def pageTitleTextBox_TextChanged(sender, event):
    selectedPage = getPage(self.document, self.currentPage)
    selectedPage.title = self.currentPage = pageTitleTextBox.Text
 

def pageContentTextBox_TextChanged(sender, event):
    selectedPage = getPage(self.document, self.currentPage)
    selectedPage.text = pageContentTextBox.Text
    
    
def editButton_Click(sender, event):
    self.editing = True


def cancelButton_Click(sender, event):
    self.editing = False
    # throw away any changes that have been made
    self.document = getDocument() 


def saveButton_Click(sender, event):
    saveDocument(self.document)
    self.editing = False