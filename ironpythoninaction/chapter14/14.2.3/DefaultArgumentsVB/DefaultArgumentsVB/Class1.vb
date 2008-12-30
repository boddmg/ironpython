Public Class Example
    Public Shared Sub DefaultValues(ByVal string1 As String, _
                                    Optional ByVal string2 As String = "default", _
                                    Optional ByVal string3 As String = "another")
        Console.WriteLine("First argument = " + string1)
        Console.WriteLine("Second argument = " + string2)
        Console.WriteLine("Third argument = " + string3)
    End Sub

    Public Shared Sub MultipleArguments(ByVal ParamArray args() As Object)
        Dim len As Integer = args.Count
        Console.WriteLine("You passed in {0} arguments", len)
        For i As Integer = 0 To UBound(args, 1)
            Dim arg As Object = args(i)
            Console.WriteLine("Argument {0} is {1}", i, arg)
        Next
    End Sub
End Class
