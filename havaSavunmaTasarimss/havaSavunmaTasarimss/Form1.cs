using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace havaSavunmaTasarimss
{
    public partial class Form1 : Form
    {
        int i = 0;
        public Form1()
        {
            InitializeComponent();
          

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            i++;
            if (i % 2 != 0)
            {
                button2.Text = "OF";
                button2.BackColor = Color.Red;
            }
            else { button2.Text = "ON";
                button2.BackColor= Color.GreenYellow;
            }


        }
    }
}
