import loadassemblies

from main.mainform import MainForm
from System.IO import Path
from System.Windows.Forms import Application


executablePath = __file__
if executablePath is None:
    executablePath = Application.ExecutablePath
executableDirectory = Path.GetDirectoryName(executablePath)

Application.EnableVisualStyles()
Application.Run(MainForm(executableDirectory))
