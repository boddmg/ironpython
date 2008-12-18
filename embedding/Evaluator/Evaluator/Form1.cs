using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Evaluator
{
    public partial class IronPythonEvaluator : Form
    {
        private Engine engine;
        public IronPythonEvaluator()
        {
            InitializeComponent();
            engine = new Engine();
            engine.set_button(button);

            code.Text = @"import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import *

print x
x = 'Something else'

def hello(s, e):
    MessageBox.Show(x)
    button.Click -= hello

button.Click += hello";
        }

        private void execute_Click(object sender, EventArgs e)
        {
            result.Text = engine.evaluate(value_of_x.Text, code.Text);
        }
    }
}
