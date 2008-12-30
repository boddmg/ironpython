using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

using Plugins;

namespace EmbeddingPlugin
{
    internal partial class EmbeddedPluginUI : Form
    {

        public EmbeddedPluginUI()
        {
            InitializeComponent();

            Engine engine = new Engine(textBox);

            int index = 0;
            foreach (PluginBase plugin in engine.Plugins)
            {
                ToolStripButton button = new ToolStripButton();
                button.ToolTipText = plugin.Name;
                button.Text = plugin.Name;

                int pluginIndex = index;
                button.Click += delegate { engine.ExecutePluginAtIndex(pluginIndex); };

                pluginToolStrip.Items.Add(button);
                index++;
            }
        }
    }
}
