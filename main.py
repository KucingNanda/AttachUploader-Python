import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import ftplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import threading
import datetime

class AutoSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AttachUploader - Python Final Project")
        self.root.geometry("600x650")
        
        # Variabel untuk menyimpan path file
        self.file_path = tk.StringVar()
        
        # --- UI LAYOUT ---
        self.create_widgets()

    def create_widgets(self):
        # 1. Bagian Pilih File
        frame_source = tk.LabelFrame(self.root, text="1. Pilih Dokumen (Source)", padx=10, pady=10)
        frame_source.pack(fill="x", padx=10, pady=5)
        
        tk.Entry(frame_source, textvariable=self.file_path, width=50).pack(side="left", padx=5)
        tk.Button(frame_source, text="Pilih File (PDF/Doc/Lainnya)", command=self.browse_file).pack(side="left")

        # 2. Konfigurasi FTP Server
        frame_ftp = tk.LabelFrame(self.root, text="2. Konfigurasi FTP Server (Arsip)", padx=10, pady=10)
        frame_ftp.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_ftp, text="FTP Host:").grid(row=0, column=0, sticky="w")
        self.ftp_host = tk.Entry(frame_ftp)
        self.ftp_host.insert(0, "ftp.dlptest.com") 
        self.ftp_host.grid(row=0, column=1, sticky="ew", padx=5)

        tk.Label(frame_ftp, text="Port:").grid(row=0, column=2, sticky="w")
        self.ftp_port = tk.Entry(frame_ftp, width=10)
        self.ftp_port.insert(0, "21") 
        self.ftp_port.grid(row=0, column=3, sticky="ew", padx=5)

        tk.Label(frame_ftp, text="Username:").grid(row=1, column=0, sticky="w")
        self.ftp_user = tk.Entry(frame_ftp)
        self.ftp_user.insert(0, "dlpuser")
        self.ftp_user.grid(row=1, column=1, sticky="ew", padx=5)

        tk.Label(frame_ftp, text="Password:").grid(row=1, column=2, sticky="w")
        self.ftp_pass = tk.Entry(frame_ftp, show="*")
        self.ftp_pass.insert(0, "YOUR_FTP_PASSWORD_HERE")
        self.ftp_pass.grid(row=1, column=3, sticky="ew", padx=5)

        # 3. Konfigurasi Notifikasi Email (SMTP)
        frame_email = tk.LabelFrame(self.root, text="3. Konfigurasi Email & Lampiran", padx=10, pady=10)
        frame_email.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_email, text="SMTP Server:").grid(row=0, column=0, sticky="w")
        self.smtp_host = tk.Entry(frame_email)
        self.smtp_host.insert(0, "smtp.gmail.com") 
        self.smtp_host.grid(row=0, column=1, sticky="ew", padx=5)

        tk.Label(frame_email, text="Port:").grid(row=0, column=2, sticky="w")
        self.smtp_port = tk.Entry(frame_email, width=10)
        self.smtp_port.insert(0, "587") 
        self.smtp_port.grid(row=0, column=3, sticky="ew", padx=5)

        tk.Label(frame_email, text="Email Pengirim:").grid(row=1, column=0, sticky="w")
        self.email_sender = tk.Entry(frame_email, width=30)
        self.email_sender.insert(0, "YOUR_EMAIL") 
        self.email_sender.grid(row=1, column=1, columnspan=3, sticky="w", padx=5)

        tk.Label(frame_email, text="Password Email:").grid(row=2, column=0, sticky="w")
        self.email_pass = tk.Entry(frame_email, show="*", width=30)
        self.email_pass.insert(0, "YOUR_GMAIL_APP_PASSWORD_HERE")
        self.email_pass.grid(row=2, column=1, columnspan=3, sticky="w", padx=5)
        
        tk.Label(frame_email, text="Email Penerima:").grid(row=3, column=0, sticky="w")
        self.email_receiver = tk.Entry(frame_email, width=30)
        self.email_receiver.insert(0, "EMAIL_RECEIVER") 
        self.email_receiver.grid(row=3, column=1, columnspan=3, sticky="w", padx=5)

        # 4. Action & Log
        self.btn_start = tk.Button(self.root, text="UPLOAD KE FTP & KIRIM EMAIL + LAMPIRAN", bg="#E91E63", fg="white", font=("Arial", 11, "bold"), command=self.start_thread)
        self.btn_start.pack(fill="x", padx=20, pady=15)

        self.log_area = scrolledtext.ScrolledText(self.root, height=12, state='disabled')
        self.log_area.pack(fill="both", expand=True, padx=10, pady=5)

    # --- FUNGSI LOGIKA ---
    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def browse_file(self):
        file_selected = filedialog.askopenfilename(
            title="Pilih File Dokumen",
            filetypes=[("Dokumen", "*.pdf *.docx *.doc *.txt *.jpg *.png"), ("All Files", "*.*")]
        )
        if file_selected:
            self.file_path.set(file_selected)
            self.log(f"File terpilih: {file_selected}")

    def start_thread(self):
        if not self.file_path.get():
            messagebox.showwarning("Peringatan", "Silakan pilih file terlebih dahulu!")
            return
        
        self.btn_start.config(state="disabled", text="Sedang Memproses...")
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        try:
            full_path = self.file_path.get()
            
            if not os.path.exists(full_path):
                raise Exception("File tidak ditemukan!")
            filename = os.path.basename(full_path)
            self.log("--- MULAI PROSES ---")
            
            # 1. UPLOAD FTP
            try:
                self.log(f"Mengupload arsip ke FTP...")
                self.upload_to_ftp(full_path, filename)
                self.log("Upload FTP berhasil (Arsip Tersimpan).")
            except Exception as e_ftp:
                self.log(f"Warning: FTP Upload gagal ({str(e_ftp)}), melanjutkan email...")

            # 2. KIRIM EMAIL DENGAN LAMPIRAN
            self.log("Menyiapkan email dengan lampiran...")
            self.send_email_with_attachment(filename, full_path)
            self.log("Email dengan lampiran terkirim.")
            
            self.log("--- PROSES SELESAI ---")
            messagebox.showinfo("Sukses", "File Terkirim (FTP & Email Attachment)!")

        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan:\n{str(e)}")
        
        finally:
            self.btn_start.config(state="normal", text="UPLOAD KE FTP & KIRIM EMAIL + LAMPIRAN")

    def upload_to_ftp(self, local_path, remote_filename):
        host = self.ftp_host.get()
        port = int(self.ftp_port.get())
        user = self.ftp_user.get()
        passwd = self.ftp_pass.get()

        ftp = ftplib.FTP()
        ftp.connect(host, port)
        ftp.login(user, passwd)
        
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_filename}', f)
        
        ftp.quit()

    def send_email_with_attachment(self, filename, file_path):
        smtp_server = self.smtp_host.get()
        smtp_port = int(self.smtp_port.get())
        sender_email = self.email_sender.get()
        sender_pass = self.email_pass.get()
        receiver_email = self.email_receiver.get()

        # Setup Email Multipart
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"[Dokumen] File Masuk: {filename}"

        body = f"""
        Halo,
        
        Berikut adalah file dokumen yang Anda minta.
        File ini juga telah diarsipkan secara otomatis ke server FTP kami.
        
        Detail:
        - Nama File: {filename}
        - Waktu Kirim: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        Silakan unduh lampiran di bawah ini.
        
        Terima kasih.
        AutoSync Sender.
        """
        msg.attach(MIMEText(body, 'plain'))

        # --- LOGIKA LAMPIRAN (ATTACHMENT) ---
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        msg.attach(part)

        # Kirim Email
        server = smtplib.SMTP(smtp_server, smtp_port)
        if smtp_port == 587:
            server.starttls()
            server.login(sender_email, sender_pass)
        
        server.send_message(msg)
        server.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoSyncApp(root)
    root.mainloop()