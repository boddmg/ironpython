Imports System.IO
Imports System.Reflection
Imports System.Text

Imports IronPython.Hosting
Imports IronPython.Runtime
Imports IronPython.Runtime.Exceptions
Imports Microsoft.Scripting
Imports Microsoft.Scripting.Runtime
Imports Microsoft.Scripting.Hosting

Imports Plugins

Friend Class PythonStream
    Inherits MemoryStream

    Dim _output As TextBox

    Public Sub New(ByVal textbox As TextBox)
        _output = textbox
    End Sub

    Public Overrides Sub Write(ByVal buffer As Byte(), ByVal offset As Integer, ByVal count As Integer)
        _output.AppendText(Encoding.UTF8.GetString(buffer, offset, count))
    End Sub
End Class

Friend Class Engine
    Dim _engine As ScriptEngine
    Dim _runtime As ScriptRuntime
    Dim _box As TextBox

    Public ReadOnly Property Plugins() As List(Of PluginBase)
        Get
            Return PluginStore.Plugins
        End Get
    End Property

    Public Sub New(ByVal textbox As TextBox)
        _engine = Python.CreateEngine()
        _runtime = _engine.Runtime

        _box = textbox

        SetStreams()
        Dim rootDir As String = AddAssemblies()
        LoadPlugins(rootDir)
    End Sub

    Public Sub SetStreams()
        Dim stream As PythonStream = New PythonStream(_box)
        _runtime.IO.SetOutput(stream, Encoding.UTF8)
        _runtime.IO.SetErrorOutput(stream, Encoding.UTF8)
    End Sub

    Public Function AddAssemblies() As String
        Dim mainAssembly As Assembly = Assembly.GetExecutingAssembly()

        Dim rootDir As String = Directory.GetParent(mainAssembly.Location).FullName
        Dim pluginsPath As String = Path.Combine(rootDir, "Plugins.dll")

        Dim pluginsAssembly As Assembly = Assembly.LoadFile(pluginsPath)

        _runtime.LoadAssembly(mainAssembly)
        _runtime.LoadAssembly(pluginsAssembly)
        _runtime.LoadAssembly(GetType(String).Assembly)
        _runtime.LoadAssembly(GetType(Uri).Assembly)

        Return rootDir
    End Function

    Public Sub LoadPlugins(ByVal rootDir As String)
        Dim pluginsDir As String = Path.Combine(rootDir, "plugins")
        For Each path As String In Directory.GetFiles(pluginsDir)
            If path.ToLower().EndsWith(".py") Then
                CreatePlugin(path)
            End If
        Next
    End Sub

    Public Sub CreatePlugin(ByVal path As String)
        Try
            Dim script As ScriptSource = _engine.CreateScriptSourceFromFile(path)
            Dim code As CompiledCode = script.Compile()
            Dim scope As ScriptScope = _engine.CreateScope()
            script.Execute(scope)
        Catch e As SyntaxErrorException
            Dim msg As String = "Syntax error in ""{0}"""
            ShowError(msg, System.IO.Path.GetFileName(path), e)
        Catch e As SystemExitException
            Dim msg As String = "SystemExit in ""{0}"""
            ShowError(msg, System.IO.Path.GetFileName(path), e)
        Catch e As Exception
            Dim msg As String = "Error loading plugin ""{0}"""
            ShowError(msg, System.IO.Path.GetFileName(path), e)
        End Try
    End Sub

    Public Sub ShowError(ByVal title As String, ByVal name As String, ByVal e As Exception)
        Dim caption As String = String.Format(title, name)
        Dim eo As ExceptionOperations = _engine.GetService(Of ExceptionOperations)()
        Dim traceback As String = eo.FormatException(e)
        MessageBox.Show(traceback, caption, MessageBoxButtons.OK, MessageBoxIcon.Error)
    End Sub

    Public Sub ExecutePluginAtIndex(ByVal index As Integer)
        Dim plugin As PluginBase = Plugins(index)

        Try
            plugin.Execute(_box)
        Catch e As Exception
            Dim msg As String = "Error executing plugin ""{0}"""
            ShowError(msg, plugin.Name, e)
        End Try
    End Sub
End Class
