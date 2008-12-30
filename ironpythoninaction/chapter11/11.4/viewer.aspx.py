
from documentreader import DocumentReader

DOCUMENT_FILE = "doc.xml"
multidoc = None
currentPage = None

def getMultiDoc():
    reader = DocumentReader(Page.MapPath(DOCUMENT_FILE))
    return reader.read()
    
    
def getPage(multidoc, name):
    matches = [page for page in multidoc.pages if page.title == name]
    if matches:
        return matches[0]
    return None
        

def Page_Load(sender, event):
    global multidoc, currentPage
    multidoc = getMultiDoc()
    if not IsPostBack:
        currentPage = multidoc.pages[0].title
        

def pageLink_Click(sender, event):
    global currentPage
    currentPage = sender.Text
    

def Page_PreRender(sender, event):
    pageRepeater.DataSource = multidoc.pages
    pageRepeater.DataBind()
    selectedPage = getPage(multidoc, currentPage)
    pageTitle.Text = selectedPage.title
    pageContent.Text = selectedPage.text
