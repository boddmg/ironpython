import clr
from generate import Generate

from source_code import csharp_source as source
#from source_code import vb_source as source

# To use the VB source, pass in the argument 'csharp=False'
assembly = Generate(source, 'WindowUtils', inMemory=True)
clr.AddReference(assembly)

from WindowUtils import WindowUtils


from System import IntPtr
from System.Text import StringBuilder

GW_HWNDNEXT = 2
def GetTopWindowTitle():
    handle = WindowUtils.GetTopWindow(IntPtr.Zero)
    while handle != IntPtr.Zero:
        if not _ExcludeWindow(handle):
            break
        handle = WindowUtils.GetWindow(handle, GW_HWNDNEXT)

    if handle != IntPtr.Zero:
			return GetWindowText(handle)
    return ''

excludes = 'button', 'tooltip', 'sysshadow', 'shell_traywnd'
def _ExcludeWindow(handle):
    if not WindowUtils.IsWindowVisible(handle):
        return True
        
    class_name = GetWindowClassName(handle)
    for entry in excludes:
        if entry in class_name.lower():
            return True
    return False


def GetWindowClassName(hWnd):
    length = 255
    sb = StringBuilder(length + 1)
    WindowUtils.GetClassName(hWnd, sb, sb.Capacity)
    return sb.ToString()


def GetWindowText(hWnd):
    length = WindowUtils.GetWindowTextLength(hWnd)
    sb = StringBuilder(length + 1)
    WindowUtils.GetWindowText(hWnd, sb, sb.Capacity)
    return sb.ToString()
