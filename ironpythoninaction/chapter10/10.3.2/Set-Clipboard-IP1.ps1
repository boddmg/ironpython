$full_path = Resolve-Path $cur_dir 'IronPython.dll'
[reflection.assembly]::LoadFrom($full_path)

$global:engine = New-Object  IronPython.Hosting.PythonEngine 

$global:ClipCode = @'
import clr 
clr.AddReference ("System.Windows.Forms")
from System.Windows.Forms import Clipboard
from System.Threading import (
    ApartmentState, Thread, 
    ThreadStart
)
def thread_proc():
     Clipboard.SetText(text)

t = Thread(ThreadStart(thread_proc))
t.ApartmentState = ApartmentState.STA
t.Start()
'@

$engine.Globals.Add("text",'')

Function global:Set-Clipboard ($Text){
  $engine.Globals["text"] = $Text
  $engine.Execute($ClipCode)
}
