import clr
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")

import os
import re

from System.Diagnostics import Process
from System.IO import File, MemoryStream
from System.Text import Encoding
from System.Windows.Markup import XamlReader

from System.Windows import LogicalTreeHelper

from System.Windows import (
   Application, Window,
   CornerRadius, Thickness
)

from System.Windows.Controls import (
   TabControl, TabItem, Border,
   FlowDocumentPageViewer,
   FlowDocumentReader,
   FlowDocumentScrollViewer
)

from System.Windows.Media import Brushes

document_location = re.compile(r'<%\sdocument_location\s%>', re.IGNORECASE)


class FlowDocumentExample(Window):
   def __init__(self):
      tabcontrol = TabControl()
      
      xaml = self.getXAML()
      for Control in (FlowDocumentReader, FlowDocumentPageViewer, FlowDocumentScrollViewer):   
         item = self.getTabItem(Control, xaml)
         tabcontrol.Items.Add(item)
         
      self.Content = tabcontrol
      self.Width = 800
      self.Height = 900
      self.Title = 'WPF FlowDocument Example'
      
      
   def handleImageLocations(self, rawXAML, documentDirectory):
      if not documentDirectory.endswith('\\'):
         documentDirectory += ' \\'
      return re.sub(document_location, documentDirectory, rawXAML)
   
   
   def getXAML(self):
      documentDirectory = os.path.abspath(os.path.dirname(__file__))
      filename = os.path.join(documentDirectory, "FlowDocument.xaml")
      rawXAML = File.ReadAllText(filename)
      return self.handleImageLocations(rawXAML, documentDirectory)


   def getTabItem(self, Control, xaml):
      bytes = Encoding.UTF8.GetBytes(xaml)
      stream = MemoryStream(bytes)
      name = Control.__name__
      
      viewer = Control()
      flowDocument = XamlReader.Load(stream)
      self.processObjectTree(flowDocument)
      viewer.Document = flowDocument
      
      border = Border()
      border.BorderThickness = Thickness(5)
      border.CornerRadius = CornerRadius(10)
      border.BorderBrush = Brushes.Blue
      border.Background = Brushes.AntiqueWhite
      border.Padding = Thickness(5)
      border.Child = viewer
      
      item = TabItem()
      item.Content = border
      item.Header = name
      return item


   def processObjectTree(self, tree):
      def OnClick(sender, event):
         uri = sender.NavigateUri
         Process.Start(uri.AbsoluteUri)
      
      for link in FindChildren(tree, 'Hyperlink'):
         link.Click += OnClick


def FindChildren(child, name):
   if child.__class__.__name__ == name:
      yield child
   for item in LogicalTreeHelper.GetChildren(child):
      if isinstance(item, basestring):
         continue
      for entry in FindChildren(item, name):
         yield entry


window = FlowDocumentExample()

app = Application()
app.Run(window)
