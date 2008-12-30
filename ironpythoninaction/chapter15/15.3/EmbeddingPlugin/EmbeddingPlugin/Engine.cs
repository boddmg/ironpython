using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Text;
using System.Windows.Forms;

using IronPython.Hosting;
using IronPython.Runtime;
using IronPython.Runtime.Exceptions;
using Microsoft.Scripting;
using Microsoft.Scripting.Runtime;
using Microsoft.Scripting.Hosting;

using Plugins;


namespace EmbeddingPlugin
{
    internal class PythonStream: MemoryStream
    {
        TextBox _output;
        public PythonStream(TextBox textbox)
        {
            _output = textbox;
        }

        public override void Write(byte[] buffer, int offset, int count)
        {
            _output.AppendText(Encoding.UTF8.GetString(buffer, offset, count));
        }
    }

    internal class Engine
    {
        ScriptEngine _engine;
        ScriptRuntime _runtime;
        TextBox _box;

        public List<PluginBase> Plugins
        {
            get { return PluginStore.Plugins; }
        }


        public Engine(TextBox textbox)
        {
            _engine = Python.CreateEngine();
            _runtime = _engine.Runtime;
            _box = textbox;

            SetStreams();
            string rootDir = AddAssemblies();
            LoadPlugins(rootDir);
        }

        public void SetStreams()
        {
            PythonStream stream = new PythonStream(_box);
            _runtime.IO.SetOutput(stream, Encoding.UTF8);
            _runtime.IO.SetErrorOutput(stream, Encoding.UTF8);
        }

        public string AddAssemblies()
        {
            Assembly mainAssembly = Assembly.GetExecutingAssembly();

            string rootDir = Directory.GetParent(mainAssembly.Location).FullName;
            string pluginsPath = Path.Combine(rootDir, "Plugins.dll");

            Assembly pluginsAssembly = Assembly.LoadFile(pluginsPath);

            _runtime.LoadAssembly(mainAssembly);
            _runtime.LoadAssembly(pluginsAssembly);
            _runtime.LoadAssembly(typeof(String).Assembly);
            _runtime.LoadAssembly(typeof(Uri).Assembly);

            return rootDir;
        }

        public void LoadPlugins(string rootDir)
        {
            string pluginsDir = Path.Combine(rootDir, "plugins");
            foreach (string path in Directory.GetFiles(pluginsDir))
            {
                if (path.ToLower().EndsWith(".py"))
                {
                    CreatePlugin(path);
                }
            }
        }

        public void CreatePlugin(string path)
        {
            try
            {
                ScriptSource script = _engine.CreateScriptSourceFromFile(path);
                CompiledCode code = script.Compile();
                ScriptScope scope = _engine.CreateScope();
                script.Execute(scope);
            }
            catch (SyntaxErrorException e)
            {
                string msg = "Syntax error in \"{0}\"";
                ShowError(msg, Path.GetFileName(path), e);
            }
            catch (SystemExitException e)
            {
                string msg = "SystemExit in \"{0}\"";
                ShowError(msg, Path.GetFileName(path), e);
            }

            catch (Exception e)
            {
                string msg = "Error loading plugin \"{0}\"";
                ShowError(msg, Path.GetFileName(path), e);
            }
        }

        public void ShowError(string title, string name, Exception e)
        {
            string caption = String.Format(title, name);
            ExceptionOperations eo = _engine.GetService<ExceptionOperations>();
            string error = eo.FormatException(e);
            MessageBox.Show(error, caption, MessageBoxButtons.OK, MessageBoxIcon.Error);

        }

        public void ExecutePluginAtIndex(int index)
        {
            PluginBase plugin = Plugins[index];

            try
            {
                plugin.Execute(_box);
            }
            catch (Exception e)
            {
                string msg = "Error executing plugin \"{0}\"";
                ShowError(msg, plugin.Name, e);
            }
        }
    }
}
