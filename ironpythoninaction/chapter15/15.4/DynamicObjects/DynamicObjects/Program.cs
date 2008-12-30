using System;
using System.Collections.Generic;
using System.Text;

using Microsoft;
using Microsoft.Scripting;
using Microsoft.Scripting.Hosting;
using Microsoft.Scripting.Hosting.Providers;
using Microsoft.Scripting.Runtime;
using IronPython.Hosting;
using IronPython.Runtime;
using IronPython.Modules;
using IronPython.Runtime.Types;

namespace DynamicObjects
{
    class Program
    {
        static ScriptRuntime runtime;
        static ScriptEngine engine;
        static ScriptScope scope;

        static void Main(string[] args)
        {
            engine = Python.CreateEngine();
            runtime = engine.Runtime;
            scope = runtime.CreateScope();

            Expressions();
            Lambda();
            PythonTypes();
            ObjectOperations();
            BuiltinFunctions();
            BuiltinModules();

            Console.WriteLine("Press any key to exit.");
            Console.ReadLine();
        }

        static void Expressions()
        {
            string code = "1 + 2 + 3 + 4";

            ScriptSource source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Expression);
            int result = source.Execute<int>(scope);
            Console.WriteLine("1 + 2 + 3 + 4 = {0}", result);
        }

        static void Lambda()
        {
            string code = "lambda x, y: x * y";

            ScriptSource source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Expression);
            Func<int, int, int> lambda = source.Execute<Func<int, int, int>>(scope);

            int result = lambda(9, 8);

            Console.WriteLine("9 * 8 = {0}", result);
        }

        static void PythonTypes()
        {
            string code = "('hello', 'world')";
            ScriptSource source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Expression);
            
            PythonTuple tuple = source.Execute<PythonTuple>(scope);
            Console.WriteLine("tuple[0], tuple[1] = {0}, {1}", tuple[0], tuple[1]);
            
        }

        static void ObjectOperations()
        {
            ObjectOperations ops = engine.Operations;

            string code = @"
class Something(object):
    def method(self, value):
        return value + 1
";
            ScriptSource source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Statements);
            source.Execute(scope);

            object klass = scope.GetVariable("Something");
            object instance = ops.Call(klass);
            object method = ops.GetMember(instance, "method");

            int result = (int)ops.Call(method, 99);

            Console.WriteLine("99 + 1 = {0}", result);
        }

        static void BuiltinFunctions()
        {
            ObjectOperations ops = engine.Operations;

            string code = @"
class Something(object):
    def method(self, value):
        return value + 1

class SomethingElse(object):
    pass
";
            ScriptSource source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Statements);
            source.Execute(scope);

            PythonType klass = scope.GetVariable<PythonType>("Something");
            PythonType klass2 = scope.GetVariable<PythonType>("SomethingElse");
            object instance = ops.Call(klass);

            bool isinstance = Builtin.isinstance(instance, klass);
            bool isinstance2 = Builtin.isinstance(instance, klass2);
            bool issubclass = Builtin.issubclass(klass, typeof(object));
            bool issubclass2 = Builtin.issubclass(klass, klass2);

            Console.WriteLine("isinstance(instance, Something) = {0}", isinstance);
            Console.WriteLine("isinstance(instance, SomethingElse) = {0}", isinstance2);
            Console.WriteLine("issubclass(Something, object) = {0}", issubclass);
            Console.WriteLine("issubclass(Something, SomethingElse) = {0}", issubclass2);
        }

        static void BuiltinModules()
        {
            string code = "{'name': 'Michael Foord', 'Age': 21, 'Profession': 'Software Development'}";

            ObjectOperations ops = engine.Operations;

            ScriptSource source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Expression);
            object dict = source.Execute(scope);

            LanguageContext language = HostingHelpers.GetLanguageContext(engine);
            CodeContext context = new CodeContext(new Scope(), language);
            string cereal = (string)PythonPickle.dumps(context, dict, 0, null);
            object dict2 = PythonPickle.loads(context, cereal);

            bool result = ops.Equal(dict, dict2);

            Console.WriteLine("original and unmarshalled dictionaries equal = {0}", result);
        }
    }
}
