Imports System.IO
Imports System.Reflection

Imports IronPython.Hosting
Imports IronPython.Runtime
Imports Microsoft.Scripting
Imports Microsoft.Scripting.Runtime
Imports Microsoft.Scripting.Hosting
Imports Microsoft.Scripting.Hosting.Providers

Public Class Engine
    Dim _engine As ScriptEngine
    Dim _runtime As ScriptRuntime
    Dim _code As CompiledCode
    Dim _scope As ScriptScope

    Public Sub New(ByVal source As String)
        _engine = Python.CreateEngine()
        _runtime = _engine.Runtime

        AddAssemblies()
        PublishModule()
        _scope = _engine.CreateScope()
        _scope.SetVariable("__name__", "__main__")

        Dim _main As Scope
        _main = HostingHelpers.GetScope(_scope)
        _runtime.Globals.SetVariable("__main__", _main)

        Dim _script As ScriptSource
        _script = _engine.CreateScriptSourceFromString(source, SourceCodeKind.Statements)
        _code = _script.Compile()
    End Sub

    Public Function Execute() As Boolean
        Try
            _code.Execute(_scope)
            Return True
        Catch ex As Exception
            Dim eo As ExceptionOperations = _engine.GetService(Of ExceptionOperations)()
            Console.Write(eo.FormatException(ex))
            Return False
        End Try
    End Function

    Public Sub SetVariable(ByVal name As String, ByVal value As Object)
        _scope.SetVariable(name, value)
    End Sub

    Public Function TryGetVariable(ByVal name As String, ByRef result As Object) As Boolean
        Return _scope.TryGetVariable(name, result)
    End Function

    Public Sub AddAssemblies()
        Dim _assembly As Assembly
        Dim libraryPath As String

        Dim fullPath As String = Assembly.GetExecutingAssembly().Location
        Dim rootDir As String = Directory.GetParent(fullPath).FullName

        libraryPath = Path.Combine(rootDir, "ClassLibrary.dll")

        _assembly = Assembly.LoadFile(libraryPath)
        _runtime.LoadAssembly(_assembly)

        _runtime.LoadAssembly(GetType(String).Assembly)
        _runtime.LoadAssembly(GetType(Uri).Assembly)
    End Sub

    Public Sub PublishModule()
        Dim _module As Scope
        Dim inner As ScriptScope

        inner = _engine.CreateScope()
        inner.SetVariable("HelloWorld", "Some string...")
        inner.SetVariable("answer", 42)

        _module = HostingHelpers.GetScope(inner)

        _runtime.Globals.SetVariable("Example", _module)
    End Sub

End Class
