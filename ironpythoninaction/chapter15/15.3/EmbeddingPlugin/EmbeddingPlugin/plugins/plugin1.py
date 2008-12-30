from Plugins import PluginBase
from EmbeddingPlugin import PluginStore

print "Loading Plugin 1"

class Plugin(PluginBase):

	def Execute(self, textbox):
		textbox.Text += "Plugin 1 called\r\n"
		
plugin = Plugin("Plugin 1")

PluginStore.AddPlugin(plugin)