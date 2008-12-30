<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class EmbeddedPluginVB
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.pluginToolStrip = New System.Windows.Forms.ToolStrip
        Me.textBox = New System.Windows.Forms.TextBox
        Me.SuspendLayout()
        '
        'pluginToolStrip
        '
        Me.pluginToolStrip.GripStyle = System.Windows.Forms.ToolStripGripStyle.Hidden
        Me.pluginToolStrip.Location = New System.Drawing.Point(0, 0)
        Me.pluginToolStrip.Name = "pluginToolStrip"
        Me.pluginToolStrip.Size = New System.Drawing.Size(284, 25)
        Me.pluginToolStrip.TabIndex = 0
        Me.pluginToolStrip.Text = "ToolStrip1"
        '
        'textBox
        '
        Me.textBox.BackColor = System.Drawing.SystemColors.Window
        Me.textBox.Location = New System.Drawing.Point(8, 46)
        Me.textBox.Multiline = True
        Me.textBox.Name = "textBox"
        Me.textBox.ReadOnly = True
        Me.textBox.Size = New System.Drawing.Size(264, 210)
        Me.textBox.TabIndex = 1
        '
        'EmbeddedPluginVB
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(284, 264)
        Me.Controls.Add(Me.textBox)
        Me.Controls.Add(Me.pluginToolStrip)
        Me.Name = "EmbeddedPluginVB"
        Me.Text = "IronPython Plugins"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Public WithEvents pluginToolStrip As System.Windows.Forms.ToolStrip
    Public WithEvents textBox As System.Windows.Forms.TextBox

End Class
