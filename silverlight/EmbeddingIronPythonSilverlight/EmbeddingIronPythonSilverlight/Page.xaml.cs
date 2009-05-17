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

            ScriptRuntimeSetup setup = Python.CreateRuntimeSetup(null);
            setup.HostType = typeof(Microsoft.Scripting.Silverlight.BrowserScriptHost);
            setup.Options["SearchPaths"] = new string[] { string.Empty };

            ScriptRuntime runtime = new ScriptRuntime(setup);
            ScriptEngine pe = Python.GetEngine(runtime);

            // load platform assemblies so you don't need to call LoadAssembly in script code.
            foreach (string name in new string[] { "mscorlib", "System", "System.Windows", "System.Windows.Browser", "System.Net" })
            {
                runtime.LoadAssembly(runtime.Host.PlatformAdaptationLayer.LoadAssembly(name));
            }


            ScriptScope scope = pe.CreateScope();
            ScriptSource source = pe.CreateScriptSourceFromString(code, SourceCodeKind.Statements);
            source.Execute(scope);

            Func<string, string> func = scope.GetVariable<Func<string, string>>("function");

            string result = func("hello world!");
            textblock.Text = result;
        }
    }
}
