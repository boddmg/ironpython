Imports System.Collections.Generic
Imports System.Reflection
Imports System.IO

Imports Microsoft.Scripting
Imports Microsoft.Scripting.Hosting
Imports IronPython.Runtime
Imports IronPython.Hosting

Module Module1

    Function Main(ByVal args As String()) As Integer
        Dim filename As String
        Dim path As String
        Dim rootDir As String
        Dim argsList As ArrayList

        filename = "program.py"
        path = Assembly.GetExecutingAssembly().Location
        rootDir = Directory.GetParent(path).FullName

        argsList = New ArrayList(args)
        argsList.Insert(0, filename)

        Return RunPythonFile(rootDir, argsList)
    End Function

    Public Function RunPythonFile(ByVal rootDir As String, ByVal args As ArrayList) As Integer
        Dim programPath As String
        Dim engine As ScriptEngine
        Dim sys As ScriptScope
        Dim options As Dictionary(Of String, Object)
        Dim argList As List
        Dim paths As String()
        Dim source As ScriptSource
        Dim result As Integer

        programPath = Path.Combine(rootDir, args(0))
        options = New Dictionary(Of String, Object)
        options("Debug") = True
        engine = Python.CreateEngine(options)

        argList = New List()
        argList.extend(args)
        sys = Python.GetSysModule(engine)
        sys.SetVariable("argv", argList)

        paths = SetupPaths(engine, rootDir)
        engine.SetSearchPaths(paths)
        Try
            source = engine.CreateScriptSourceFromFile(programPath)
            result = source.ExecuteProgram()
            Return result
        Catch e As Exception
            Dim eo As ExceptionOperations = engine.GetService(Of ExceptionOperations)()
            Console.Write(eo.FormatException(e))
            Return 1
        End Try
    End Function


    Public Function SetupPaths(ByVal engine As ScriptEngine, ByVal rootDir As String) As String()
        Dim paths As List(Of String)
        Dim path As String
        Dim items As String()

        paths = New List(Of String)()
        paths.Add(rootDir)

        path = Environment.GetEnvironmentVariable("IRONPYTHONPATH")
        If path <> Nothing AndAlso path.Length > 0 Then
            items = path.Split(";"c)
            For Each p As String In items
                If p.Length > 0 Then
                    paths.Add(p)
                End If
            Next
        End If
        Return paths.ToArray()
    End Function
End Module
