Imports System
Imports System.Collections.Generic
Imports System.Text
Imports System.Runtime.CompilerServices

Public Class DynamicObject

    Private _error As String = "'DynamicObject' has no attribute '{0}'"
    Private _instance_dict As New Dictionary(Of String, Object)
    Public ReadOnly Property container() As Dictionary(Of String, Object)
        Get
            Return _instance_dict
        End Get
    End Property

    <SpecialName()> Public Function GetBoundMember(ByVal name As String) As Object
        If Not _instance_dict.ContainsKey(name) Then
            Dim msg As String = String.Format(_error, name)
            Throw New System.MissingMemberException(msg)
        End If
        Return _instance_dict.Item(name)
    End Function

    <SpecialName()> Public Sub SetMemberAfter(ByVal name As String, ByVal value As Object)
        _instance_dict.Add(name, value)
    End Sub

    <SpecialName()> Public Sub DeleteMember(ByVal name As String)
        If Not _instance_dict.ContainsKey(name) Then
            Dim msg As String = String.Format(_error, name)
            Throw New System.MissingMemberException(msg)
        End If
        _instance_dict.Remove(name)
    End Sub

End Class
