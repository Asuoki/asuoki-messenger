//
// HSD - Successful
// HASD - ERROR
//

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Diagnostics;
using System.ComponentModel;
using System.IO;
using System.Drawing;
using System.Collections;
using Microsoft.Win32;
using System.Timers;
using System.Collections.ObjectModel;


namespace Asuoki_App
{
    public static class GlobalVar
    {
        public static string PasswordGlobal = "";
    }

    public partial class MainWindow : Window
    {
        static List<string> chat = new List<string>();
        static List<string> diconnectChatList = new List<string>();
        static List<Process> processList = new List<Process>();
        static string[] data = File.ReadAllLines("./asuoki-data/allContact.db");
        ObservableCollection<string> dataUser = new ObservableCollection<string>(data);
        ObservableCollection<string> activeChat = new ObservableCollection<string>();
        public string fileName; 
        public string nameChat;
        public string nameProcess;
        public string nameActiveChat;
        public static System.Timers.Timer aTimer;
        Random rnd = new Random();
        public int count = 0;
        public string password_string = "";
        //Process http_server_process;

        public MainWindow()
        {
            InitializeComponent();
            listChat.ItemsSource = dataUser;
            activeChatListBox.ItemsSource = activeChat;
        }

        void connectButton(object sender, RoutedEventArgs e)
        {
            DateTime now = DateTime.Now;
            DateTime Task1 = new DateTime(10);
            logo_connect.Visibility = Visibility.Hidden; 
            

            Active.Visibility = Visibility.Visible;
            activeChatGrid.Visibility = Visibility.Hidden;
            startHttp(); 
            //loaderPage.Visibility = Visibility.Visible;
            //Task.Delay(5000).Wait();
            //loaderPage.Visibility = Visibility.Hidden;
            logo_connect.Visibility = Visibility.Visible;
            loaderPage.Visibility = Visibility.Hidden;
        }
        void startHttp()
        {
            nameActiveChat = listChat.SelectedItem.ToString();
            int port = rnd.Next(8000, 9000);
            string command = "";
            if(password_string == "asuoki")
            {
                command = $"python ./py/start_chat.py {nameActiveChat} {port} {3}";
            } 
            else
            {
                command = $"python ./py/start_chat.py {nameActiveChat} {port} {2}";
            }
            ProcessStartInfo name_process = new ProcessStartInfo("cmd.exe", "/C" + command); 
            /*name_process.WindowStyle = ProcessWindowStyle.Hidden;
            name_process.RedirectStandardOutput = true;
            name_process.UseShellExecute = false;
            name_process.CreateNoWindow = true;*/
            Process new_pocess = Process.Start(name_process);

            try
            {
                diconnectChatList.Insert(count, listChat.SelectedItem.ToString());
                
            }
            catch (Exception e)
            {
                Trace.WriteLine("HASD (error diconnectChatList)");
            }

            try
            {
                processList.Insert(count, new_pocess);
                count++;
                activeChat.Insert(0, nameProcess);
            }
            catch (Exception e)
            {
                Trace.WriteLine("HASD (error processList)");
            }
        }
        void hideLoaderPage(Object source, RoutedEventArgs e)
        {
            logo_connect.Visibility = Visibility.Visible;
            loaderPage.Visibility = Visibility.Hidden;
        }
        private void activeChatListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            try
            {
                //nameActiveChat = activeChatListBox.SelectedItem.ToString();
            }
            catch
            {
                activeChatGrid.Visibility = Visibility.Hidden;
                selectChatGrid.Visibility = Visibility.Visible;
                Active.Visibility = Visibility.Visible;
                disconnectButt.Visibility = Visibility.Hidden;
            }
            disconnectButt.Visibility = Visibility.Visible;
        }
        void disconnectButton(object sender, RoutedEventArgs e)
        {
            string kill_process = activeChatListBox.SelectedItem.ToString();
            for (int i = 0; i < count; i++)
            {
                if(diconnectChatList[i]== kill_process)
                {
                    activeChatListBox.UnselectAll();
                    processList[i].Kill();
                    Trace.WriteLine("HSD Good Kill");
                    activeChat.Remove(kill_process);
                   
                }
            }
        }
        void showActiveChat(object sender, RoutedEventArgs e)
        {
            activeChatGrid.Visibility = Visibility.Visible;
            selectChatGrid.Visibility = Visibility.Hidden;
            Active.Visibility = Visibility.Hidden;
            createNewChatGrid.Visibility = Visibility.Hidden;
            logo_connect.Visibility = Visibility.Hidden;
        }
        void disableActiveChatGrid(object sender, RoutedEventArgs e)
        {
            activeChatGrid.Visibility = Visibility.Hidden;
            selectChatGrid.Visibility = Visibility.Visible;
            Active.Visibility = Visibility.Visible;
            disconnectButt.Visibility = Visibility.Hidden;
        }
        void create_newButton(object sender, RoutedEventArgs e)
        {
            selectChatGrid.Visibility = Visibility.Hidden;
            createNewChatGrid.Visibility = Visibility.Visible;
            logo_connect.Visibility = Visibility.Hidden;
            activeChatGrid.Visibility = Visibility.Hidden;
            Active.Visibility = Visibility.Visible;
        }
        private void ListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            nameProcess = listChat.SelectedItem.ToString(); 
            createNewChatGrid.Visibility = Visibility.Hidden;
            selectChatGrid.Visibility = Visibility.Hidden;
            logo_connect.Visibility = Visibility.Visible;
            Active.Visibility = Visibility.Visible;
            activeChatGrid.Visibility = Visibility.Hidden;
        }

        private void selectFileClick(object sender, RoutedEventArgs e) 
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            if (openFileDialog.ShowDialog() == true)
                fileName = openFileDialog.FileName;
            Console.WriteLine(openFileDialog.FileName);

        }
        private void createNewChatButton(object sender, RoutedEventArgs e)
        {
            int port = rnd.Next(9000, 10000);
            var nameFolder = nameInput.Text; 
            string command = $"python ./py/create_new_chat.py {fileName} {nameFolder} {port} {password_string}";
            ProcessStartInfo createNewChat = new ProcessStartInfo("cmd.exe", "/C" + command);
            createNewChat.WindowStyle = ProcessWindowStyle.Hidden;
            createNewChat.RedirectStandardOutput = true;
            createNewChat.UseShellExecute = false;
            createNewChat.CreateNoWindow = true;
            System.Diagnostics.Process.Start(createNewChat);
            dataUser.Insert(0, nameFolder); 
            activeChatGrid.Visibility = Visibility.Hidden;
        }
        

        private void exitApp(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private void max_min(object sender, RoutedEventArgs e)
        {
            /*
            switch (WindowState)
            {
                case (WindowState.Maximized):
                    WindowState = WindowState.Normal;
                    break;
                     
                case (WindowState.Normal):
                    WindowState = WindowState.Maximized;
                    break;
            }*/
        }

        private void svernut(object sender, RoutedEventArgs e)
        {
            WindowState = WindowState.Minimized;
        }

        private void peredvigat(object sender, MouseButtonEventArgs e)
        {
            if (e.ClickCount == 2)
                max_min(sender, e);

            if (e.ChangedButton == MouseButton.Left)
            {
                DragMove();
            }
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {

        }

        void showSettings(object sender, RoutedEventArgs e)
        {
            openSettingGrid.Visibility = Visibility.Hidden;
            blurEffect.Visibility = Visibility.Visible;
            Setings.Visibility = Visibility.Visible;
            selectChatGrid.Visibility = Visibility.Hidden;
            selectChatGrid.Visibility = Visibility.Hidden;
            Active.Visibility = Visibility.Visible;
            createNewChatGrid.Visibility = Visibility.Hidden;
            logo_connect.Visibility = Visibility.Hidden;
            activeChatGrid.Visibility = Visibility.Hidden;
        }
        void closeSettings(object sender, RoutedEventArgs e)
        {
            openSettingGrid.Visibility = Visibility.Visible;
            blurEffect.Visibility = Visibility.Hidden;
            Setings.Visibility = Visibility.Hidden;
            selectChatGrid.Visibility = Visibility.Visible;
        }
        void closeNewChatGrid(object sender, RoutedEventArgs e)
        {
            selectChatGrid.Visibility = Visibility.Visible;
            createNewChatGrid.Visibility = Visibility.Hidden;
            activeChatGrid.Visibility = Visibility.Hidden;
            Active.Visibility = Visibility.Visible;
        }

        // ----------------- Settings button ----------------- //

        void newRsaKeyClick(object sender, RoutedEventArgs e)
        {
            string command = $"python ./py/create_new_rsa_key.py"; 
            ProcessStartInfo create_new_rsa_key = new ProcessStartInfo("cmd.exe", "/C" + command);
            create_new_rsa_key.WindowStyle = ProcessWindowStyle.Hidden;
            create_new_rsa_key.RedirectStandardOutput = true;
            create_new_rsa_key.UseShellExecute = false;
            create_new_rsa_key.CreateNoWindow = true;
            System.Diagnostics.Process.Start(create_new_rsa_key);
        }
        void newAddressClick(object sender, RoutedEventArgs e)
        {

            string command = $"node ./js/create_new_address.js {password_string}";
            ProcessStartInfo newAddressClick = new ProcessStartInfo("cmd.exe", "/C" + command);
            newAddressClick.WindowStyle = ProcessWindowStyle.Hidden;
            newAddressClick.RedirectStandardOutput = true;
            newAddressClick.UseShellExecute = false;
            newAddressClick.CreateNoWindow = true;
            System.Diagnostics.Process.Start(newAddressClick);
        }
        void newQrCodeClick(object sender, RoutedEventArgs e)
        {
            string command = $"python ./py/create_new_qr.py";
            ProcessStartInfo newQrCode = new ProcessStartInfo("cmd.exe", "/C" + command);
            newQrCode.WindowStyle = ProcessWindowStyle.Hidden;
            newQrCode.RedirectStandardOutput = true;
            newQrCode.UseShellExecute = false;
            newQrCode.CreateNoWindow = true;
            System.Diagnostics.Process.Start(newQrCode);
        }
        void showQrClick(object sender, RoutedEventArgs e)
        {

        }
        void showLocalFilesClick(object sender, RoutedEventArgs e)
        {
            string command = $"explorer .\\asuoki-data"; 
            ProcessStartInfo showLocalFiles = new ProcessStartInfo("cmd.exe", "/C" + command);
            showLocalFiles.WindowStyle = ProcessWindowStyle.Hidden;
            showLocalFiles.RedirectStandardOutput = true;
            showLocalFiles.UseShellExecute = false;
            showLocalFiles.CreateNoWindow = true;
            System.Diagnostics.Process.Start(showLocalFiles);
            
        }
        void clearCacheClick(object sender, RoutedEventArgs e)
        {
            string command = $"python ./py/clear_cache.py";
            ProcessStartInfo clearCacheClick = new ProcessStartInfo("cmd.exe", "/C" + command);
            clearCacheClick.WindowStyle = ProcessWindowStyle.Hidden;
            clearCacheClick.RedirectStandardOutput = true;
            clearCacheClick.UseShellExecute = false;
            clearCacheClick.CreateNoWindow = true;
            System.Diagnostics.Process.Start(clearCacheClick);
        }

        void delete_all_chats_Click(object sender, RoutedEventArgs e)
        {
            string command = $"python ./py/delete_all_chats.py";
            ProcessStartInfo clearCacheClick = new ProcessStartInfo("cmd.exe", "/C" + command);
            clearCacheClick.WindowStyle = ProcessWindowStyle.Hidden;
            clearCacheClick.RedirectStandardOutput = true;
            clearCacheClick.UseShellExecute = false;
            clearCacheClick.CreateNoWindow = true;
            //System.Diagnostics.Process.Start(clearCacheClick);
        }

        private void EnterButtonClick(object sender, RoutedEventArgs e)
        {
            if(password_box.Text.Length != 0)
            {
                password_string = password_box.Text;
                password.Visibility = Visibility.Hidden;
            }
        }
    }
}
