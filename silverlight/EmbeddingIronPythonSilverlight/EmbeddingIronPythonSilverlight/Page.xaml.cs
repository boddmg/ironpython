using System;
using System.Windows.Controls;
using IronPython;
using IronPython.Hosting;
using Microsoft.Scripting;
using Microsoft.Scripting.Hosting;

namespace EmbeddingIronPythonSilverlight
{

    public partial class Page : UserControl
    {
        public Page()
        {
            InitializeComponent();
            string code = @"
def function(string):
    return string.upper()";
            ScriptEngine pe = Python.CreateEngine();
            ScriptScope scope = pe.CreateScope();
            ScriptSource source = pe.CreateScriptSourceFromString(code, SourceCodeKind.Statements);
            source.Execute(scope);

            Func<string, string> func = scope.GetVariable<Func<string, string>>("function");

            string result = func("hello world!");
            textblock.Text = result;
        }
    }
}
