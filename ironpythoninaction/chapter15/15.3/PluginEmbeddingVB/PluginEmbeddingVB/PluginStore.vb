Imports Plugins


Public Class PluginStore

    Private Shared _plugins As List(Of PluginBase) = New List(Of PluginBase)()

    Friend Shared ReadOnly Property Plugins() As List(Of PluginBase)
        Get
            Return _plugins
        End Get
    End Property

    Public Shared Sub AddPlugin(ByVal plugin As PluginBase)
        _plugins.Add(plugin)
    End Sub
End Class
