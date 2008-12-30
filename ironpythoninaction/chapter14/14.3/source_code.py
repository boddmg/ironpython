csharp_source = """
using System;
using System.Text;
using System.Runtime.InteropServices;

namespace WindowUtils
{
    public class WindowUtils
    {

        [DllImport("user32.dll")]
        public static extern bool IsWindowVisible(IntPtr hWnd);

        [DllImport("user32.dll")]
        public static extern IntPtr GetTopWindow(IntPtr hWnd);

        [DllImport("user32.dll")]
        public static extern IntPtr GetWindow(IntPtr hWnd, uint wCmd);

        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetWindowTextLength(IntPtr hWnd);

        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetWindowText(IntPtr hWnd, [Out] StringBuilder lpString, int nMaxCount);

        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetClassName(IntPtr hWnd, [Out] StringBuilder lpString, int nMaxCount);

    }
}
"""

# No default namespace so here we add an explicit namespac
vb_source = """
Imports System
Imports System.Text
Imports System.Runtime.InteropServices
	
Namespace WindowUtils
	
	Public Class WindowUtils
	
	    <DllImport("user32.dll")> Public Shared Function IsWindowVisible(ByVal hWnd As IntPtr) As Boolean
	    End Function
	
	    <DllImport("user32.dll")> Public Shared Function GetTopWindow(ByVal hWnd As IntPtr) As IntPtr
	    End Function
	
	    <DllImport("user32.dll")> Public Shared Function GetWindow(ByVal hWnd As IntPtr, ByVal wCmd As UInteger) As IntPtr
	    End Function
	
	    <DllImport("user32.dll", SetLastError:=True, CharSet:=CharSet.Auto)> Public Shared Function GetWindowTextLength(ByVal hWnd As IntPtr) As Integer
	    End Function
	
	    <DllImport("user32.dll", SetLastError:=True, CharSet:=CharSet.Auto)> Public Shared Function GetWindowText(ByVal hWnd As IntPtr, ByVal lpString As StringBuilder, ByVal nMaxCount As Integer) As Integer
	    End Function
	
	    <DllImport("user32.dll", SetLastError:=True, CharSet:=CharSet.Auto)> Public Shared Function GetClassName(ByVal hWnd As IntPtr, ByVal lpString As StringBuilder, ByVal nMaxCount As Integer) As Integer
	    End Function
	
	End Class
End Namespace
"""