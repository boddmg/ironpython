# Copyright (c) 2007-8 Michael Foord.
# All Rights Reserved
#

import clr
clr.AddReference("Scriptable, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null")

from Scriptable import (
    Scriptable, ScriptableForString, 
    ScriptableEvent, ScriptableEventArgs
)

from System import EventHandler
from System.Windows import Application, DependencyObject
from System.Windows.Browser import HtmlPage
from System.Windows.Controls import StackPanel, Canvas, OpenFileDialog, TextBlock
from System.Windows.Media import Colors, SolidColorBrush

import examples

import sys
from button import Button


class Writer(object):
    def __init__(self):
        self.stdout = ''
        
    def write(self, text):
        self.stdout += text
        HtmlPage.Document.debugging.value = self.stdout


output_writer = Writer()
sys.stdout = output_writer
print 'Mini Web-IDE started'

ignore_next_execute = False


def StackTraceFromCurrentException():
    traceback = sys.exc_info()[2]
    stackTrace = []
    while traceback is not None:
        frame = traceback.tb_frame
        lineno = traceback.tb_lineno
        code = frame.f_code
        filename = code.co_filename
        name = code.co_name
        stackTrace.append((filename, lineno, name))
        traceback = traceback.tb_next
    sys.exc_clear()
    return stackTrace


def formatLine(lineInfo):
    fileName, lineNo, name = lineInfo
    line = '  File "%s", line %s' % (fileName, lineNo)
    if name != "<module>":
        line += ", in %s" % (name,)
    return line


def executeCode(code):
    global ignore_next_execute
    if ignore_next_execute:
        ignore_next_execute = False
        return
    
    if not code:
        print 'No code to execute.'
        return
    
    code = code.replace('\r\n', '\n') + '\n'
    context = {'__name__': '__main__', 'root': root}
    try:
        exec code in context
    except Exception, e:
        print
        print "Traceback (most recent call last):"
        for line in StackTraceFromCurrentException():
            print formatLine(line)
        print e.__class__.__name__ + ": " + str(e)
        print


class CodeChange(ScriptableForString):
    def _method(self, code):
        output_writer.stdout = ''
        print "Executing Python code."
        executeCode(code)
        return ''

codeChange = CodeChange()


class Load(Scriptable):
    def _method(self):
        dialog = OpenFileDialog()
        dialog.Filter = "Python files (*.py)|*.py|All files (*.*)|*.*"
        if dialog.ShowDialog() == True:
            return dialog.File.OpenText().ReadToEnd()
        return ''


setCode = ScriptableEvent()
load = Load()


def SetExample(name):
    global ignore_next_execute
    ignore_next_execute = True
    args = ScriptableEventArgs()
    args.code = getattr(examples, name)
    setCode.OnEvent(args)


class RefreshExamples(Scriptable):
    def _method(self):
        root.Children.Clear()
        main = StackPanel()
        
        t = TextBlock(Text=" Examples ")
        t.FontSize = 32
        t.Foreground = SolidColorBrush(Colors.Magenta)
        main.Children.Add(t)
    
        b = Button('Browser DOM')
        b.Click += lambda: SetExample('browserDOM')
        main.Children.Add(b)
        
        b = Button('HTML Events')
        b.Click += lambda: SetExample('inputEvents')
        main.Children.Add(b)
    
        b = Button('Video Player')
        b.Click += lambda: SetExample('videoExample')
        main.Children.Add(b)
    
        b = Button('Open File Dialog')
        b.Click += lambda: SetExample('openFileDialog')
        main.Children.Add(b)
    
        b = Button('Local Storage')
        b.Click += lambda: SetExample('isolatedStorageFile')
        main.Children.Add(b)
    
        b = Button('Loading XAML')
        b.Click += lambda: SetExample('loadingXaml')
        main.Children.Add(b)
    
        b = Button('Using Controls')
        b.Click += lambda: SetExample('controls')
        main.Children.Add(b)
    
        b = Button('WebClient')
        b.Click += lambda: SetExample('webClient')
        main.Children.Add(b)
    
        b = Button('Threading')
        b.Click += lambda: SetExample('threading')
        main.Children.Add(b)
    
        b = Button('Read from a File')
        b.Click += lambda: SetExample('openFile')
        main.Children.Add(b)
    
        b = Button('Setting Position')
        b.Click += lambda: SetExample('position')
        main.Children.Add(b)
    
        b = Button('Animation')
        b.Click += lambda: SetExample('animation')
        main.Children.Add(b)
                
        root.Children.Add(main)


refresh = RefreshExamples()

HtmlPage.RegisterScriptableObject("codeChange", codeChange)
HtmlPage.RegisterScriptableObject("refresh", refresh)
HtmlPage.RegisterScriptableObject("load", load)
HtmlPage.RegisterScriptableObject("setCode", setCode)

# Default example
HtmlPage.Document.code.value = examples.browserDOM

root = Canvas()
refresh._method()

Application.Current.RootVisual = root

