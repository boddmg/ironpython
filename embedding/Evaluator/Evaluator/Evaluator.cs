using System;
using System.Collections.Generic;
using System.Text;
using IronPython.Hosting;
using IronPython.Runtime;
using Microsoft.Scripting;
using Microsoft.Scripting.Hosting;


namespace Evaluator
{
    public class Engine
    {
        private object button;
        private ScriptEngine engine;
        private ScriptScope scope;

        public Engine()
        {
            engine = Python.CreateEngine();
            scope = engine.CreateScope();
        }

        public void set_button(object from_form)
        {
            button = from_form;
        }

        public string evaluate(string x, string code) 
        {
            scope.SetVariable("x", x);
            scope.SetVariable("button", button);

            try
            {
                ScriptSource source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Statements);
                source.Execute(scope);
            }
            catch (Exception ex)
            {
                return "Error executing code: " + ex.ToString();
            }

            if (!scope.ContainsVariable("x"))
            {
                return "x was deleted";
            }
            string result = scope.GetVariable<object>("x").ToString();
            return result;
        }
    }
}
