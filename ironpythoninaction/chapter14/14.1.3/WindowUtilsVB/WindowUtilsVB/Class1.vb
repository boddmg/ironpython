Imports System
Imports System.Text
Imports System.Runtime.InteropServices

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
