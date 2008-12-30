using System;
using System.Collections.Generic;
using System.Text;
using Plugins;
using System.Windows.Forms;

namespace EmbeddingPlugin
{

    public class PluginStore
    {
        private static List<PluginBase> _plugins = new List<PluginBase>();

        internal static List<PluginBase> Plugins
        {
            get { return _plugins; }
        }

        public static void AddPlugin(PluginBase plugin)
        { _plugins.Add(plugin); }

    }

}
