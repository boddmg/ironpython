using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Text;

namespace Evaluator
{
    class Program
    {
        static void Main(string[] args)
        {
            IronPythonEvaluator evaluator = new IronPythonEvaluator();
            Application.Run(evaluator);
        }
    }
}
