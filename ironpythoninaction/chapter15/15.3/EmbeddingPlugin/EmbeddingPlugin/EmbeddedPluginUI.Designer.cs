namespace EmbeddingPlugin
{
    partial class EmbeddedPluginUI
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pluginToolStrip = new System.Windows.Forms.ToolStrip();
            this.textBox = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // pluginToolStrip
            // 
            this.pluginToolStrip.GripStyle = System.Windows.Forms.ToolStripGripStyle.Hidden;
            this.pluginToolStrip.Location = new System.Drawing.Point(0, 0);
            this.pluginToolStrip.Name = "pluginToolStrip";
            this.pluginToolStrip.Size = new System.Drawing.Size(217, 25);
            this.pluginToolStrip.TabIndex = 0;
            this.pluginToolStrip.Text = "pluginToolStrip";
            // 
            // textBox
            // 
            this.textBox.BackColor = System.Drawing.SystemColors.Window;
            this.textBox.Location = new System.Drawing.Point(11, 40);
            this.textBox.Multiline = true;
            this.textBox.Name = "textBox";
            this.textBox.ReadOnly = true;
            this.textBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBox.Size = new System.Drawing.Size(194, 160);
            this.textBox.TabIndex = 1;
            // 
            // EmbeddedPluginUI
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(217, 212);
            this.Controls.Add(this.textBox);
            this.Controls.Add(this.pluginToolStrip);
            this.Name = "EmbeddedPluginUI";
            this.Text = "IronPython Plugins";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        public System.Windows.Forms.ToolStrip pluginToolStrip;
        public System.Windows.Forms.TextBox textBox;
    }
}

