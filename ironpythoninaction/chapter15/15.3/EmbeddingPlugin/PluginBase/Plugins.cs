using System;
using System.Collections.Generic;
using System.Text;
using System.Windows.Forms;

namespace Plugins
{
    public class PluginBase
    {
        private string _name;
        public string Name
        {
            get { return _name; }
        }

        public PluginBase(string name)
        { _name = name; }

        virtual public void Execute(TextBox textbox)
        { }
    }
}
