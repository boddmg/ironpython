Imports System.IO
Imports System.Reflection

Module BasicEmbedding

    Sub Main()
        Dim source As String
        Dim engine As Engine

        source = GetSourceCode()
        engine = New Engine(source)

        engine.SetVariable("variable", "Hello World!")

        Dim result As Boolean = engine.Execute()
        If (Not result) Then
            Console.WriteLine("Executing Python code failed!")
        Else

            Dim variable As Object = Nothing
            Dim success As Boolean
            success = engine.TryGetVariable("variable", variable)
            If (success) Then
                Console.WriteLine("""variable"" = {0}", variable)
            Else
                Console.WriteLine("Fetching the the result ""variable"" failed")
            End If
        End If


        Console.WriteLine("Press any key to exit.")
        Console.ReadLine()
    End Sub

    Function GetSourceCode() As String
        Dim _assembly As Assembly
        Dim _stream As Stream
        Dim textStreamReader As StreamReader

        _assembly = Assembly.GetExecutingAssembly()
        _stream = _assembly.GetManifestResourceStream("BasicEmbedding.source_code.py")
        textStreamReader = New StreamReader(_stream)
        Return textStreamReader.ReadToEnd()
    End Function

End Module
