using System;
using System.IO;
using System.Reflection;

using IronPython.Hosting;
using IronPython.Runtime;
using Microsoft.Scripting;
using Microsoft.Scripting.Runtime;
using Microsoft.Scripting.Hosting;
using Microsoft.Scripting.Hosting.Providers;

namespace BasicEmbedding
{
    public class Engine
    {
        ScriptEngine _engine;
        ScriptRuntime _runtime;
        CompiledCode _code;
        ScriptScope _scope;

        public Engine(string source)
        {
            _engine = Python.CreateEngine();
            _runtime = _engine.Runtime;

            AddAssemblies();
            PublishModule();
            _scope = _engine.CreateScope();
            _scope.SetVariable("__name__", "__main__");

            Scope _main = HostingHelpers.GetScope(_scope);
            _runtime.Globals.SetVariable("__main__", _main);

            ScriptSource _script = _engine.CreateScriptSourceFromString(source, SourceCodeKind.Statements);
            _code = _script.Compile();
        }

        public bool Execute()
        {
            try
            {
                _code.Execute(_scope);
                return true;
            }
            catch (Exception e)
            {
                ExceptionOperations es = _engine.GetService<ExceptionOperations>();
                Console.Write(es.FormatException(e));
                return false;
            }

        }

        public void SetVariable(string name, object value)
        {
            _scope.SetVariable(name, value);
        }

        public bool TryGetVariable(string name, out object result)
        {
            return _scope.TryGetVariable(name, out result);
        }

        public void AddAssemblies()
        {
            string fullPath = Assembly.GetExecutingAssembly().Location;
            string rootDir = Directory.GetParent(fullPath).FullName;
            string libraryPath = Path.Combine(rootDir, "ClassLibrary.dll");

            Assembly assembly = Assembly.LoadFile(libraryPath);
            _runtime.LoadAssembly(assembly);

            _runtime.LoadAssembly(typeof(String).Assembly);
            _runtime.LoadAssembly(typeof(Uri).Assembly);
        }

        public void PublishModule()
        {
            ScriptScope inner = _engine.CreateScope();
            inner.SetVariable("HelloWorld", "Some string...");
            inner.SetVariable("answer", 42);

            Scope module = HostingHelpers.GetScope(inner);

            _runtime.Globals.SetVariable("Example", module);
        }

    }
}
