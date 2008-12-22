using System;
using System.Collections.Generic;
using System.Text;

using IronPython;
using IronPython.Hosting;
using Microsoft.Scripting;
using Microsoft.Scripting.Hosting;


namespace EmbeddedCalculator
{
    public class Engine
    {
        private ScriptEngine engine;
        private ScriptScope scope;

        public Engine()
        {
            Dictionary<String,Object> options = new Dictionary<string,object>();
            options["DivisionOptions"] = PythonDivisionOptions.New;
            engine = Python.CreateEngine(options);
            scope = engine.CreateScope();

        }

        public string calculate(string input)
        {
            try
            {
                ScriptSource source = engine.CreateScriptSourceFromString(input, SourceCodeKind.Expression);
                object result = source.Execute(scope);
                return result.ToString();
            }
            catch
            {
                return "Error";
            }
        }

    }
}
