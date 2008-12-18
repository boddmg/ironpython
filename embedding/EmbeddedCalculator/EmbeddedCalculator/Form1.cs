using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace EmbeddedCalculator
{
    public partial class Calculator : Form
    {
        private Engine engine;

        public Calculator()
        {
            InitializeComponent();
            engine = new Engine();
        }


        private void equals_Click(object sender, EventArgs e)
        {
            display.Text = engine.calculate(display.Text);
        }

        private void clear_Click(object sender, EventArgs e)
        {
            display.Text = "";
        }

        private void eight_Click(object sender, EventArgs e)
        {

            display.Text += "8";
        }

        private void seven_Click(object sender, EventArgs e)
        {

            display.Text += "7";
        }

        private void zero_Click(object sender, EventArgs e)
        {
            display.Text += "0";
        }

        private void point_Click(object sender, EventArgs e)
        {
            display.Text += ".";
        }

        private void plus_Click(object sender, EventArgs e)
        {
            display.Text += "+";
        }

        private void minus_Click(object sender, EventArgs e)
        {
            display.Text += "-";
        }

        private void times_Click(object sender, EventArgs e)
        {
            display.Text += "*";
        }

        private void divide_Click(object sender, EventArgs e)
        {
            display.Text += "/";
        }

        private void one_Click(object sender, EventArgs e)
        {
            display.Text += "1";
        }

        private void two_Click(object sender, EventArgs e)
        {
            display.Text += "2";
        }

        private void three_Click(object sender, EventArgs e)
        {
            display.Text += "3";
        }

        private void four_Click(object sender, EventArgs e)
        {
            display.Text += "4";
        }

        private void five_Click(object sender, EventArgs e)
        {
            display.Text += "5";
        }

        private void six_Click(object sender, EventArgs e)
        {
            display.Text += "6";
        }

        private void nine_Click(object sender, EventArgs e)
        {
            display.Text += "9";
        }
    }
}
