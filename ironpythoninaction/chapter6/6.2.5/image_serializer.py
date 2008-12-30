import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Runtime.Serialization')

from System.Drawing import Bitmap
from System.Drawing.Imaging import ImageFormat
from System.IO import Directory, FileStream, Path
from System.Runtime.Serialization.Formatters.Binary import BinaryFormatter


path = 'icons'
FileStream("MyFile.bin", FileMode.Create, FileAccess.Write, FileShare.None);

FileStream("MyFile.bin", FileMode.Open, FileAccess.Read, FileShare.Read)
image = formatter.Deserialize(stream)
