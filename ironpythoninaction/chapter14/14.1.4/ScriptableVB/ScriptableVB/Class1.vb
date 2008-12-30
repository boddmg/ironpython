Imports System
Imports System.Windows.Browser

<ScriptableType()> _
Public Class Scriptable
    Public Function method(ByVal value As String) As String
        Return real(value)
    End Function
    <ScriptableMember()> _
    Public Overridable Function real(ByVal value As String) As String
        Return "override me"
    End Function
End Class