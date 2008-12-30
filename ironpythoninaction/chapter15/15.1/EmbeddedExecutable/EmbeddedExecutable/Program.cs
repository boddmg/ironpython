/* Copyright (c) 2008 Michael Foord.
 * http://wwww.ironpythoninaction.com/
 */

using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;

using IronPython;
using IronPython.Hosting;
using IronPython.Runtime;
using IronPython.Runtime.Exceptions;

using Microsoft.Scripting;
using Microsoft.Scripting.Hosting;


namespace EmbeddedExecutable
{
    class Program
    {
        static int Main(string[] args)
        {
            string filename = "program.py";
            string path = Assembly.GetExecutingAssembly().Location;
            string rootDir = Directory.GetParent(path).FullName;

            ArrayList argsList = new ArrayList(args);
            argsList.Insert(0, filename);

            return RunPythonFile(rootDir, argsList);
        }

        public static int RunPythonFile(string rootDir, ArrayList args)
        {
            string programPath = Path.Combine(rootDir, (string)args[0]);
            Dictionary<string, object> options = new Dictionary<string, object>();
            options["Debug"] = true;
            ScriptEngine engine = Python.CreateEngine(options);

            List argList = new List();
            argList.extend(args);
            ScriptScope sys = Python.GetSysModule(engine);
            sys.SetVariable("argv", argList);

            string[] paths = SetupPaths(engine, rootDir);
            engine.SetSearchPaths(paths);

            try
            {
                ScriptSource source = engine.CreateScriptSourceFromFile(programPath);
                int result = source.ExecuteProgram();
                return result;
            }
            catch (Exception e)
            {
                ExceptionOperations es = engine.GetService<ExceptionOperations>();
                Console.Write(es.FormatException(e));
                return 1;
            }
 
        }

        public static string[] SetupPaths(ScriptEngine engine, string rootDir)
        {

            List<string> paths = new List<string>();
            paths.Add(rootDir);

            string path = Environment.GetEnvironmentVariable("IRONPYTHONPATH");
            if (path != null && path.Length > 0)
            {
                string[] items = path.Split(';');
                foreach (string p in items)
                {
                    if (p.Length > 0)
                    {
                        paths.Add(p);
                    }
                }
            }
            return paths.ToArray();
        }
    }
}

