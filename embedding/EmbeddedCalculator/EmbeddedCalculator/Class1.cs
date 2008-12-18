using System;
using System.Collections.Generic;
using System.Text;
using IronPython.Hosting;
using IronPython.Runtime;
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
            engine = ScriptRuntime.Create().GetEngine("py");
            // An alternative would be engine = PythonEngine.CurrentEngine

            scope = engine.CreateScope();

            ((IronPython.PythonEngineOptions)engine.Options).DivisionOptions = IronPython.PythonDivisionOptions.New;

        }

        public string calculate(string input)
        {
            try
            {
                ScriptSource source = engine.CreateScriptSourceFromString(input, SourceCodeKind.Expression);
                return source.Execute(scope).ToString();
            }
            catch (Exception ex)
            {
                return "Error";
            }
        }

    }
}
