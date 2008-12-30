import clr
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("windowsbase")

import os

from System import Uri, UriKind

from System.Windows import (
   Application, Window, Thickness,
   HorizontalAlignment, VerticalAlignment,
   SizeToContent, Point, TextWrapping,
   TextAlignment, CornerRadius,
   HorizontalAlignment, VerticalAlignment
)

from System.Windows.Documents import (
   Bold, Hyperlink, Italic, Run
)

from System.Windows.Ink import DrawingAttributes
from System.Windows.Input import Cursors

from System.Windows.Controls import (
   Grid, ColumnDefinition, RowDefinition,
   CheckBox, ComboBox, ComboBoxItem, Label,
   Expander, TextBlock, Button, StackPanel,
   InkCanvas, ScrollBarVisibility, ScrollViewer,
   Image, Border, ToolTip
)

from System.Windows.Media import (
   Brushes, Colors, GradientStop, 
   LinearGradientBrush
)

from System.Windows.Shapes import Rectangle
from System.Windows.Media.Effects import DropShadowBitmapEffect
from System.Windows.Media.Imaging import BitmapImage


def SetGridChild(grid, child, col, row, tooltip):
   if hasattr(child, 'FontSize'):
      child.FontSize = 16
   child.Margin = Thickness(15)
   child.Cursor = Cursors.Hand
   child.ToolTip = ToolTip(Content=tooltip)
   grid.SetColumn(child, col)
   grid.SetRow(child, row)
   grid.Children.Add(child)
   
   
def GetLinearGradientBrush():
   brush = LinearGradientBrush()
   brush.StartPoint = Point(0,0)
   brush.EndPoint = Point(1,1)
   stops = [
      (Colors.Yellow, 0.0),
      (Colors.Tomato, 0.25),
      (Colors.DeepSkyBlue, 0.75),
      (Colors.LimeGreen, 1.0)
   ]
   for color, stop in stops:
      brush.GradientStops.Add(GradientStop(color, stop))
   return brush


class ControlsExample(Window):
   def __init__(self):
      grid = self.getGrid()
      grid.Background = GetLinearGradientBrush()
      self.createControls(grid)
      
      border = Border()
      border.BorderThickness = Thickness(5)
      border.CornerRadius = CornerRadius(10)
      border.BorderBrush = Brushes.Blue
      border.Background = Brushes.Yellow
      border.Padding = Thickness(5)
      border.Child = grid
      self.Content = border
      
      self.Title = 'Windows Presentation Foundation Controls Example'
      self.SizeToContent = SizeToContent.Height
      self.Width = 800
      
      
   def getGrid(self):
      grid = Grid()
      grid.ShowGridLines = True
      
      # 3x3 grid
      for i in range(3):
         grid.ColumnDefinitions.Add(ColumnDefinition())
         grid.RowDefinitions.Add(RowDefinition())
      
      label = Label()
      label.Margin = Thickness(15)
      label.FontSize = 16
      label.Content = "Nothing Yet..."
      label.HorizontalAlignment = HorizontalAlignment.Center
      self.label = label
      
      grid.SetColumnSpan(self.label, 3)
      grid.SetRow(self.label, 0)
      grid.Children.Add(self.label)
      
      return grid

   
   def createControls(self, grid):
      self.createComboAndCheck(grid)
      self.createImage(grid)
      self.createExpander(grid)
      self.createInkCanvas(grid)
      self.createScrollViewer(grid)
      self.createTextBlockAndHyperlink(grid)
      
    
   def createComboAndCheck(self, grid):
      panel = StackPanel()
      
      label = Label()
      label.Content = "CheckBox & ComboBox"
      label.FontSize = 16
      label.Margin = Thickness(10)
      
      check = CheckBox()
      check.Content = "CheckBox"
      check.Margin = Thickness(10)
      check.FontSize = 16
      check.IsChecked = True
      def action(s, e):
         checked = check.IsChecked
         self.label.Content = "CheckBox IsChecked = %s" % checked
      check.Checked += action
      check.Unchecked += action
      
      combo = ComboBox()
      for entry in ("A ComboBox", "An Item", "The Next One", "Another"):
         item = ComboBoxItem()
         item.Content = entry
         item.FontSize = 16
         combo.Items.Add(item)
      combo.SelectedIndex = 0
      combo.Height = 26
      def action(s, e):
         selected = combo.SelectedIndex
         self.label.Content = "ComboBox SelectedIndex = %s" % selected
      combo.SelectionChanged += action
      combo.FontSize = 16
      combo.Margin = Thickness(10)
      
      panel.Children.Add(label)
      panel.Children.Add(combo)
      panel.Children.Add(check)
      SetGridChild(grid, panel, 0, 1, "ComboBox & CheckBox")
      
      
   def createImage(self, grid):
      image = Image()
      bi = BitmapImage()
      bi.BeginInit()
      image_uri = os.path.join(os.path.dirname(__file__), 'image.jpg')
      bi.UriSource = Uri(image_uri, UriKind.RelativeOrAbsolute)
      bi.EndInit()
      image.Source = bi
      SetGridChild(grid, image, 1, 1, "Image")
      
      
   def createExpander(self, grid):
      expander = Expander()
      expander.Header = "An Expander Control"
      expander.IsExpanded = True
      contents = StackPanel()
      textblock = TextBlock(FontSize=16,
                            Text="\r\nSome content for the expander..."
                                 "\r\nJust some text you know...\r\n")
      contents.Children.Add(textblock)
      button = Button()
      button.Content = 'Push Me'
      button.FontSize = 24
      button.BitmapEffect = DropShadowBitmapEffect()
      button.Margin = Thickness(10)
      def action(s, e):
         self.label.Content = "Button in Expander pressed"
      button.Click += action
      contents.Children.Add(button)
      
      expander.Content = contents
      SetGridChild(grid, expander, 2, 1, "Expander")
      
   
   def createInkCanvas(self, grid):
      panel = StackPanel()
      label = Label(FontSize=16, Content="An InkCanvas", Margin=Thickness(10))
      canvas = InkCanvas()
      canvas.Width = 150
      canvas.Height = 150
      canvas.Background = Brushes.DarkSlateBlue
   
      ink = DrawingAttributes()
      ink.Color = Colors.SpringGreen
      ink.Height = 2
      ink.Width = 2
      ink.FitToCurve = False
      canvas.DefaultDrawingAttributes = ink
      panel.Children.Add(label)
      panel.Children.Add(canvas)
      SetGridChild(grid, panel, 0, 2, "InkCanvas")
      
      
   def createScrollViewer(self, grid):
      scroll = ScrollViewer()
      scroll.Height = 200
      scroll.HorizontalScrollBarVisibility = ScrollBarVisibility.Auto
      scroll.HorizontalAlignment = HorizontalAlignment.Stretch
      scroll.VerticalAlignment = VerticalAlignment.Stretch
      panel = StackPanel()
      text = TextBlock()
      text.TextWrapping = TextWrapping.Wrap
      text.Margin = Thickness(0, 0, 0, 20)
      text.Text = "A ScrollViewer.\r\n\r\nScrollbars appear as and when they are needed...\r\n"
      
      rect = Rectangle()
      rect.Fill = GetLinearGradientBrush()
      rect.Width = 500
      rect.Height = 500
      
      panel.Children.Add(text)
      panel.Children.Add(rect)
                  
      scroll.Content = panel;
      SetGridChild(grid, scroll, 1, 2, "ScrollViewer")
      
      
   def createTextBlockAndHyperlink(self, grid):
      textblock = TextBlock()
      textblock.TextWrapping = TextWrapping.Wrap
      textblock.Background = Brushes.AntiqueWhite
      textblock.TextAlignment = TextAlignment.Center 
      textblock.Inlines.Add(Bold(Run("TextBlock")))
      textblock.Inlines.Add(Run(" is designed to be "))
      textblock.Inlines.Add(Italic(Run("lightweight")))
      textblock.Inlines.Add(Run(", and is geared specifically at integrating "))
      textblock.Inlines.Add(Italic(Run("small")))
      textblock.Inlines.Add(Run(" portions of flow content into a UI. "))
      
      link = Hyperlink(Run("A Hyperlink - Click Me"))
      def action(s, e):
         self.label.Content = "Hyperlink Clicked"
      link.Click += action
      textblock.Inlines.Add(link)
      SetGridChild(grid, textblock, 2, 2, "TextBlock")
      
      
window = ControlsExample()

app = Application()
app.Run(window)
