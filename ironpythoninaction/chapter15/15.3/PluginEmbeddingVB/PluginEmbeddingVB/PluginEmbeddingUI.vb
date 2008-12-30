Imports Plugins

Friend Class EmbeddedPluginVB

    Public Sub New()
        InitializeComponent()

        Dim engine As Engine = New Engine(textBox)

        Dim index As Integer = 0
        For Each plugin As PluginBase In engine.Plugins

            Dim button As ToolStripButton = New ToolStripButton()
            button.ToolTipText = plugin.Name
            button.Text = plugin.Name

            Dim handler As ButtonHandler = New ButtonHandler(engine, index, button)
            pluginToolStrip.Items.Add(button)
            index += 1
        Next

    End Sub

End Class

Friend Class ButtonHandler
    Dim _engine As Engine
    Dim _index As Integer

    Public Sub New(ByVal engine As Engine, ByVal index As Integer, ByVal button As ToolStripButton)
        _engine = engine
        _index = index

        AddHandler button.Click, AddressOf ClickHandler
    End Sub

    Public Sub ClickHandler(ByVal sender As Object, ByVal e As EventArgs)
        _engine.ExecutePluginAtIndex(_index)
    End Sub

End Class
