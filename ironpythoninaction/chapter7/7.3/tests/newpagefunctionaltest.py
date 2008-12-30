import loadassemblies

from tests.functionaltest import FunctionalTest

from System.Threading import Thread
from System.Windows.Forms import Form, SendKeys
        

class NewPageTest(FunctionalTest):

    def clickNewPageButton(self):
        button = self.mainForm.toolBar.Items[3]
        executor = self.executeAsynchronously(lambda: button.PerformClick())
        Thread.CurrentThread.Join(200)
        return executor
    
    
    def testNewPageDialog(self):
        # * Harold opens MultiDoc
        # * He clicks on the 'New Page' toolbar button
        executor = self.clickNewPageButton()
        
        # * A dialog called 'Name Tab' appears
        dialog = self.invokeOnGUIThread(lambda: Form.ActiveForm)
        title = self.invokeOnGUIThread(lambda: dialog.Text)
        
        self.assertEquals(title, "Name Tab", "Incorrect dialog name")
        
        # * Harold changes his mind, so he selects cancel
        self.invokeOnGUIThread(lambda: dialog.CancelButton.PerformClick())
        executor.join()
        
        # * No new tab appears
        def GetNumberOfPages():
            return len(self.mainForm.tabControl.TabPages)
        numPages = self.invokeOnGUIThread(GetNumberOfPages)
        self.assertEquals(numPages, 1, "Wrong number of tabPages")
        
        # * Our capricious user clicks the button again
        executor = self.clickNewPageButton()
        
        # * The dialog appears again
        dialog = self.invokeOnGUIThread(lambda: Form.ActiveForm)
        
        # * This time he enters a name 'My New Page'
        def TypeName():
            SendKeys.SendWait('My New Page')
        self.invokeOnGUIThread(TypeName)
        
        # * He clicks on OK
        self.invokeOnGUIThread(lambda: dialog.AcceptButton.PerformClick())
        
        # * There are now two tabs
        numPages = self.invokeOnGUIThread(GetNumberOfPages)
        self.assertEquals(numPages, 2, "Wrong number of tabPages")
        
        # * The second one is called 'My New Page'
        def GetSecondTabTitle():
            secondTab = self.mainForm.tabControl.TabPages[1]
            return secondTab.Text
        
        secondTabTitle = self.invokeOnGUIThread(GetSecondTabTitle)
        self.assertEquals(secondTabTitle, "My New Page",
                          "Wrong title on new page")
        
        # * Harold is ecstatic


if __name__ == '__main__':
    from tests.testutils import MakeSuite, RunTests
    suite = MakeSuite(NewPageTest)
    results = RunTests(suite, verbosity=2)
    
