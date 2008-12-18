using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Text;
using System.Reflection;
using System.Windows.Forms;

using System.Collections.ObjectModel;
using IronPython.Hosting;
using Microsoft.Scripting;
using Microsoft.Scripting.Hosting;

namespace ScriptedTurtle
{
    public partial class TheTurtle : Form
    {
        // The drawing surface is the canvas on which the
        // turtle draws.
        private Graphics drawingSurface = null;
        private Turtle turtle = null;

        // We save the image of the turtle's tracks just
        // before we draw the turtle icon.  That way, when
        // the turtle moves, we don't have to worry about erasing
        // the icon.
        Image savedImage = null;
        
        ScriptEngine engine;
        ScriptScope scope;

        public TheTurtle()
        {
            InitializeComponent();
            InitializeCustom();
        }

        private void InitializeCustom()
        {
            InitializeCanvas();

            this.tabControl.Focus();
            
            engine = Python.CreateEngine();
            scope = engine.CreateScope();

            ScriptRuntime runtime = engine.Runtime;
            runtime.LoadAssembly(typeof(String).Assembly);
            runtime.LoadAssembly(typeof(Uri).Assembly);
            InitializeExamples();
        }

        // Make our form look a little more presentable when
        // we resize it.
        private void MonadHost_ResizeEnd(object sender, EventArgs e)
        {
            InitializeCanvas();
        }

        // This brings our application back to a clean state.
        // We create a fresh new canvas the same size as the current
        // form, create a new turtle to reference that canvas,
        // and draw the turtle.
        private void InitializeCanvas()
        {
            this.pictureBox.Image = 
                new Bitmap(pictureBox.Width, pictureBox.Height);
            drawingSurface = Graphics.FromImage(this.pictureBox.Image);
            drawingSurface.SmoothingMode = 
                System.Drawing.Drawing2D.SmoothingMode.HighQuality;

            turtle = new Turtle(drawingSurface);
            turtle.Reset();
            
            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
        }

        // The following methods are pretty similar.  We
        // first draw our saved image to the canvas (the one without
        // the turtle icon,) have the turtle draw (or do) whatever
        // it was told to do, save the resulting image, draw
        // the turtle icon, and finally refresh the view of
        // the canvas.
        private void penUp_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.PenUp();

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void penDown_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.PenDown();

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void clear_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            InitializeCanvas();

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void forward10_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.Forward(10);

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void forward1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.Forward(1);

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void left1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.Left(1);

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void left10_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.Left(10);

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void right1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.Right(1);

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void right10_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.Right(10);

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void backward1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.Backward(1);

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void backward10_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            turtle.Backward(10);

            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }

        private void run_Click(object sender, EventArgs e)
        {
            drawingSurface.DrawImage(savedImage, 0, 0);

            scope.SetVariable("turtle", turtle);
            string code = scriptText.Text;
            try
            {
                ScriptSource source = engine.CreateScriptSourceFromString(code, SourceCodeKind.Statements);
                source.Execute(scope);
            }
            catch (Exception ex)
            {
                ExceptionOperations eo;
                eo = engine.GetService<ExceptionOperations>();
                string error = eo.FormatException(ex);
        
                MessageBox.Show(error, "There was an Error", 
                                MessageBoxButtons.OK, 
                                MessageBoxIcon.Error);
                return;
            }
            
            savedImage = new Bitmap(this.pictureBox.Image);
            turtle.Draw();
            this.pictureBox.Refresh();
        }


        private void InitializeExamples()
        {
            string rootDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            string examplesDir = Path.Combine(rootDir, "Examples");
            List<String> examplesData = new List<String>();

            foreach (string path in Directory.GetFiles(examplesDir))
            {
                string name = Path.GetFileNameWithoutExtension(path);
                string data = File.ReadAllText(path);
                examples.Items.Add(name);
                examplesData.Add(data);

            }

            examples.SelectedIndexChanged += delegate(object sender, EventArgs e)
            {
                scriptText.Text = examplesData[examples.SelectedIndex];
            };
        }
    }
}