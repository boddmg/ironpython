'This assembly has a root namespace called 'PythonExtension'
Imports System
Imports System.Collections

Public Delegate Function Callback(ByVal input As Integer) As Integer

Public Class PythonClass
    Implements IEnumerable

    Private _callback As Callback
    Private _value As Integer

    Public Sub New(ByVal value As Integer, ByVal callback As Callback)
        Me._value = value
        Me._callback = callback
    End Sub

    Public Overrides Function ToString() As String
        Return String.Format("PythonClass<{0}>", Me._value)
    End Function

    Public Shared Operator +(ByVal a As PythonClass, ByVal b As PythonClass) As PythonClass
        Dim value As Integer
        value = a._value + b._value
        Return New PythonClass(value, a._callback)
    End Operator

    Public Function GetEnumerator() As IEnumerator Implements IEnumerable.GetEnumerator
        Dim i As Integer
        Dim list As New List(Of Integer)
        For i = Me._value To 0 Step -1
            If (i Mod 2 = 0) Then
                list.Add(Me._callback(i))
            End If
        Next i
        Return list.GetEnumerator()
    End Function

    Default Public Property Item(ByVal index As Object) As Object
        Get
            Console.WriteLine("Indexed with {0}", index)
            Return index
        End Get
        Set(ByVal value As Object)
            Console.WriteLine("Index {0} set to {1}", index, value)
        End Set
    End Property

End Class




