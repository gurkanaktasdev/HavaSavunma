using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Windows.Forms;
using System.Diagnostics;
using Accord.Video;
using Accord.Video.DirectShow;



namespace görüntüDeneme
{
    public partial class Form1 : Form
    {
        private FilterInfoCollection videoDevices;   // Ana Kamera için
        private VideoCaptureDevice videoSource;      // Ana Kamera için
        private Process procesSade;  //kamera normal açıldığındaki görüntü aktarımı için ilgili process
        private Thread receiveThread;
        private UdpClient udpClient;
        private bool receiving = true;
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            label1.Text = "pythondan UDP ile Görüntü AKtarımı Denemesi";
            baseCounter(); // sayıcı işlmelerin eş zamanlı yapııp yapılmadığının kontrolü

        }
        private void StartReceiving()       // udp nesnesi ile farklı thread de veri alıyor.
        {
            if (udpClient == null)
            {
                udpClient = new UdpClient(5005);  // Başlat
            }
            receiveThread = new Thread(ReceiveImage);
            receiveThread.IsBackground = true;
            receiveThread.Start();
        }

        private void ReceiveImage()     // udp den frame almaamıza yarar.
        {
            IPEndPoint remoteEP = new IPEndPoint(IPAddress.Any, 0);

            while (receiving && udpClient != null )
            {
                try
                {
                    byte[] data = udpClient.Receive(ref remoteEP);
                    using (var ms = new MemoryStream(data))
                    {
                        Image img = Image.FromStream(ms);
                        pictureBox1.Invoke(new Action(() =>
                        {
                            pictureBox1.Image = img;
                        }));
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Hata: " + ex.Message);
                }
            }
        }
        
        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            receiving = false;
            udpClient?.Close();
            receiveThread?.Join();
            base.OnFormClosing(e);
        }

        private bool isReceivingStarted = false;
        private void button1_Click(object sender, EventArgs e)
        {
            
            if (!string.IsNullOrEmpty(textBox1.Text))   // eğer açı değerleri girilmediyse Görev i başlatmaz
            {
                pythonKameraBaslat();
            }
            else
            {
                MessageBox.Show("Lütfen AÇı Değerlerini Giriniz");
            }

        }
        private void pythonKameraBaslat()   // python üzerinden gelen kamera verilerini picturebox a aktarırız.
        {
            if (videoSource != null && videoSource.IsRunning)
            {
                AnaKamerayıKapat();
            }


            if (!isReceivingStarted)
            {
                StartReceiving();
                isReceivingStarted = true;
            }
            try
            {
                string pythonExePath = @"C:\Python\Python313\python.exe";
                string pythonScriptPath = @"C:\Users\aktas\Desktop\ComputerVision\havasavunma.py";

                ProcessStartInfo psi = new ProcessStartInfo
                {
                    FileName = pythonExePath,
                    Arguments = $"\"{pythonScriptPath}\"",
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = false,
                    RedirectStandardError = false,
                };

                procesSade = new Process();
                procesSade.StartInfo = psi;
                procesSade.Start();
                using (StreamWriter sw = procesSade.StandardInput)
                {
                    if (sw.BaseStream.CanWrite)
                    {
                        sw.WriteLine(textBox1.Text); // TextBox’taki veriyi gönder
                        sw.WriteLine("quit");       // Python tarafında çıkış için bir sinyal örneği
                        
                    }
                }

                MessageBox.Show("Python dosyası çalıştırıldı.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Python başlatılamadı: " + ex.Message);
            }
        }
        private void baseCounter()
        {
            Thread updateThread = new Thread(UpdateCounter);
            updateThread.IsBackground = true;  // Arka planda çalışacak
            updateThread.Start();
        }
        private void UpdateCounter()
        {
            int i = 0;
            while (true)
            {
                i++;
                // UI thread'ine erişim sağlamak için Invoke kullanıyoruz
                label2.Invoke(new Action(() => {
                    label2.Text = i.ToString();
                }));

                // Performansı artırmak için biraz gecikme ekleyebiliriz
                Thread.Sleep(100);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Kapat();    // ilgili görev kamerası(python üzerinden yayın yapılan) kapatılıyor
            KameraAyarla(); // ana kamera açılıyor
            
        }

        private void Kapat()       // ilgili udp nesnesi,thread ve process i kapatmaya yarar     
        {
            receiving = false;
            udpClient?.Close();
            udpClient = null;
            receiveThread = null;

            if (procesSade != null && !procesSade.HasExited)
            {
                procesSade.Kill(); // veya sinyalle düzgün kapatma
                procesSade.Dispose();
                procesSade = null;
            }

            pictureBox1.Image.Dispose();
            pictureBox1.Image = null;

            isReceivingStarted = false;
            receiving = true;
        }
        private void button3_Click(object sender, EventArgs e) // Normal Kamera açma
        {
            KameraAyarla();
        }
        private void KameraAyarla() // winforms üzerinden kameraya erişir.
        {
            if (videoSource == null || !videoSource.IsRunning)
            {
                // Kamera listesini al
                videoDevices = new FilterInfoCollection(FilterCategory.VideoInputDevice);

                if (videoDevices.Count == 0)
                {
                    MessageBox.Show("Herhangi bir kamera bulunamadı.");
                    return;
                }

                // İlk kamerayı seç
                videoSource = new VideoCaptureDevice(videoDevices[0].MonikerString);
                videoSource.NewFrame += Video_NewFrame;
                videoSource.Start();
            }
            else
            {
                MessageBox.Show("Kamera zaten çalışıyor.");
            }
        }
        private void Video_NewFrame(object sender, NewFrameEventArgs eventArgs) // doğrudan kameraya erişip yazdırırız.
        {
            Bitmap frame = (Bitmap)eventArgs.Frame.Clone();

            pictureBox1.Invoke((MethodInvoker)delegate
            {
                pictureBox1.Image?.Dispose(); // belleği temizle
                pictureBox1.Image = frame;
            });
        }
        private void AnaKamerayıKapat()     // doğrudan erişdiğimiz kamerayı kapatmamamıza yarar.
        {
            if (videoSource != null && videoSource.IsRunning)
            {
                videoSource.SignalToStop();
                videoSource.WaitForStop();
                videoSource = null;

                // İsteğe bağlı: Ekranı temizle
                pictureBox1.Image?.Dispose();
                pictureBox1.Image = null;
            }
        }
    }
}
