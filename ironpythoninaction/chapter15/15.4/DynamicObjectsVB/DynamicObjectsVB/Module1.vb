Imports Microsoft
Imports Microsoft.Scripting
Imports Microsoft.Scripting.Hosting
Imports Microsoft.Scripting.Hosting.Providers
Imports Microsoft.Scripting.Runtime
Imports IronPython.Hosting
Imports IronPython.Runtime
Imports IronPython.Modules
Imports IronPython.Runtime.Types

Module DynamicObjects

    Dim runtime As ScriptRuntime
    Dim engine As ScriptEngine
    Dim scope As ScriptScope

    Sub Main()
        engine = Python.CreateEngine()
        runtime = engine.Runtime
        scope = runtime.CreateScope()

        Expressions()
        Lambda()
        PythonTypes()
        ObjectOperations()
        BuiltinFunctions()
        BuiltinModules()

        Console.WriteLine("Press any key to exit.")
        Console.ReadLine()
    End Sub

    Sub Expressions()
        Dim code As String = "1 + 2 + 3 + 4"

        Dim source As ScriptSource
        source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Expression)
        Dim result As Integer = source.Execute(Of Integer)(scope)

        Console.WriteLine("1 + 2 + 3 + 4 = {0}", result)

    End Sub

    Sub Lambda()
        Dim code As String = "lambda x, y: x * y"

        Dim source As ScriptSource
        Dim lambda As Func(Of Integer, Integer, Integer)
        source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Expression)
        lambda = source.Execute(Of Func(Of Integer, Integer, Integer))(scope)

        Dim result As Integer = lambda(9, 8)

        Console.WriteLine("9 * 8 = {0}", result)
    End Sub

    Sub PythonTypes()
        Dim code As String = "('hello', 'world')"
        Dim source As ScriptSource
        source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Expression)

        Dim tuple As PythonTuple
        tuple = source.Execute(Of PythonTuple)(scope)
        Console.WriteLine("tuple[0], tuple[1] = {0}, {1}", tuple(0), tuple(1))
    End Sub

    Sub ObjectOperations()
        Dim ops As ObjectOperations = engine.Operations

        Dim code As String = "class Something(object):" & vbCrLf & _
        "    def method(self, value):" & vbCrLf & _
        "        return value + 1"

        Dim source As ScriptSource = engine.CreateScriptSourceFromString(code, SourceCodeKind.Statements)
        source.Execute(scope)

        Dim klass As Object = scope.GetVariable("Something")
        Dim instance As Object = ops.Call(klass)
        Dim method As Object = ops.GetMember(instance, "method")

        Dim result As Integer = ops.Call(method, 99)

        Console.WriteLine("99 + 1 = {0}", result)
    End Sub

    Sub BuiltinFunctions()
        Dim ops As ObjectOperations = engine.Operations

        Dim code As String = "class Something(object):" & vbCrLf & _
        "    def method(self, value):" & vbCrLf & _
        "        return value + 1" & vbCrLf & _
        "" & vbCrLf & _
        "class SomethingElse(object):" & vbCrLf & _
        "    pass"

        Dim source As ScriptSource = engine.CreateScriptSourceFromString(code, SourceCodeKind.Statements)
        source.Execute(scope)

        Dim klass As PythonType = scope.GetVariable(Of PythonType)("Something")
        Dim klass2 As PythonType = scope.GetVariable(Of PythonType)("SomethingElse")
        Dim instance As Object = ops.Call(klass)

        Dim isinstance As Boolean = Builtin.isinstance(instance, klass)
        Dim isinstance2 As Boolean = Builtin.isinstance(instance, klass2)
        Dim issubclass As Boolean = Builtin.issubclass(klass, GetType(Object))
        Dim issubclass2 As Boolean = Builtin.issubclass(klass, klass2)

        Console.WriteLine("isinstance(instance, Something) = {0}", isinstance)
        Console.WriteLine("isinstance(instance, SomethingElse) = {0}", isinstance2)
        Console.WriteLine("issubclass(Something, object) = {0}", issubclass)
        Console.WriteLine("issubclass(Something, SomethingElse) = {0}", issubclass2)
    End Sub

    Sub BuiltinModules()
        Dim code As String = "{'name': 'Michael Foord', 'Age': 21, 'Profession': 'Software Development'}"

        Dim ops As ObjectOperations = engine.Operations

        Dim source As ScriptSource = engine.CreateScriptSourceFromString(code, SourceCodeKind.Expression)
        Dim dict As Object = source.Execute(scope)

        Dim language As LanguageContext = HostingHelpers.GetLanguageContext(engine)
        Dim co As CodeContext = New CodeContext(New Scope(), language)

        Dim cereal As String = PythonPickle.dumps(co, dict, 0, Nothing)
        Dim dict2 As Object = PythonPickle.loads(co, cereal)

        Dim result As Boolean = ops.Equal(dict, dict2)

        Console.WriteLine("original and unmarshalled dictionaries equal = {0}", result)
    End Sub

End Module
