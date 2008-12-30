import clr
clr.AddReference('System.Drawing')

from System.Drawing import Bitmap, Icon
from System.IO import Directory, File, Path
from System.Runtime.Serialization.Formatters.Binary import BinaryFormatter


formatter = BinaryFormatter()
iconDirectory = Path.Combine(Directory.GetCurrentDirectory(), 'icons')

exception = 'copy_clipboard_16.ico'
for filePath in Directory.GetFiles(iconDirectory):
    if not (filePath.endswith('.ico') or filePath.endswith('.gif')):
        continue
    filename = Path.GetFileName(filePath)
    namePart = Path.GetFileNameWithoutExtension(filename)
    outPath = Path.Combine(iconDirectory, namePart + '.dat')
    
    if filename == exception:
        image = Icon(filePath)
    else:
        image = Bitmap(filePath)
        
    stream = File.Create(outPath)
    formatter.Serialize(stream, image)
    stream.Close()
