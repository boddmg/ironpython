from Plugins import PluginBase
from EmbeddingPlugin import PluginStore

print "Loading Plugin 2"

class Plugin(PluginBase):

	def Execute(self, textbox):
		textbox.Text += "Plugin 2 called\r\n"
		
plugin = Plugin("Plugin 2")

PluginStore.AddPlugin(plugin)