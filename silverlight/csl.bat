set sl=C:\Program Files\Microsoft Silverlight\2.0.30226.2
set csc=C:\Windows\Microsoft.NET\Framework\v2.0.50727\csc.exe

%csc% /out:OnKeyPress.dll /t:library /nostdlib+ /noconfig /r:"%sl%\mscorlib.dll" /r:"%sl%\System.dll" /r:"%sl%\System.Core.dll" /r:"%sl%\System.Net.dll" /r:"%sl%\System.Windows.Browser.dll" *.cs

pause