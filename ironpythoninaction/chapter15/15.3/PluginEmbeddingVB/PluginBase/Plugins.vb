Imports System.Windows.Forms

Public Class PluginBase
    Private _name As String
    Public ReadOnly Property Name() As String
        Get
            Return _name
        End Get
    End Property

    Public Sub New(ByVal name As String)
        _name = name
    End Sub

    Public Overridable Sub Execute(ByVal textbox As TextBox)
    End Sub
End Class
