using System;
using System.IO;
using System.Reflection;

namespace BasicEmbedding
{
    class Program
    {
        static void Main()
        {
            string source = GetSourceCode();
            Engine engine = new Engine(source);

            engine.SetVariable("variable", "Hello World!");

            bool result = engine.Execute();
            if (!result)
            {
                Console.WriteLine("Executing Python code failed!");
            }
            else
            {
                object variable;
                bool success = engine.TryGetVariable("variable", out variable);
                if (success)
                {
                    Console.WriteLine("\"variable\" = {0}", variable);
                }
                else
                {
                    Console.WriteLine("Fetching the result \"variable\" failed");
                }
            }

            Console.WriteLine("Press any key to exit.");
            Console.ReadLine();
        }

        static string GetSourceCode()
        {
            Assembly assembly = Assembly.GetExecutingAssembly();
            Stream stream = assembly.GetManifestResourceStream("BasicEmbedding.source_code.py");
            StreamReader textStreamReader = new StreamReader(stream);
            return textStreamReader.ReadToEnd();
        }
    }
}
