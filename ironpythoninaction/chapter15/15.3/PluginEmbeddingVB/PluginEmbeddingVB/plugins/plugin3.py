from Plugins import PluginBase
from EmbeddingPlugin import PluginStore

print "Loading Plugin 3"

class Plugin(PluginBase):

	def Execute(self, textbox):
		raise Exception("boom!")
		
plugin = Plugin("Plugin 3")

PluginStore.AddPlugin(plugin)
