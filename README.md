AttachUploader (Python Final Project)

AttachUploader adalah aplikasi desktop berbasis Python yang dirancang untuk mengirimkan file dokumen (PDF, Docx, dll) secara otomatis ke server FTP sebagai arsip cadangan, sekaligus mengirimkan notifikasi dan file tersebut sebagai lampiran (attachment) langsung melalui Email (SMTP).

Proyek ini dibuat untuk memenuhi Tugas Besar mata kuliah Network Programming.

📸 Tampilan Aplikasi

(Nanti...)

🚀 Fitur Utama
1. Dual Protocol Handling: Mengintegrasikan protokol FTP (File Transfer Protocol) dan SMTP (Simple Mail Transfer Protocol) dalam satu klik.

2. Smart Attachment: Dokumen tidak hanya disimpan di server, tetapi langsung dilampirkan pada email sehingga penerima bisa mengunduhnya tanpa login ke FTP.

3. Fault Tolerance (Fail-Safe): Aplikasi didesain tangguh; jika server FTP sedang down atau timeout, aplikasi akan mencatat warning tetapi tetap melanjutkan pengiriman email agar dokumen penting tetap sampai ke tujuan.

4. GUI User Friendly: Dibangun menggunakan tkinter dengan antarmuka yang bersih dan log aktivitas real-time.

5. Multi-threading: Proses berjalan di latar belakang (background thread) untuk mencegah aplikasi freeze saat mengupload file besar.

🛠️ Teknologi yang Digunakan
- Python 3.x

- GUI: tkinter (Built-in)

- Network: ftplib, smtplib

- System: os, threading

- Email: email.mime

📦 Cara Menjalankan

Pastikan Python 3 sudah terinstall.

Clone repository ini atau download file main.py.

Jalankan aplikasi:

python main.py


Konfigurasi di Aplikasi:

FTP Configuration: Masukkan Host (misal: dlptest.com), User, dan Password.

SMTP Configuration: Masukkan Email Pengirim (Gmail) dan App Password (Wajib 2FA aktif, bukan password login biasa).

Pilih file dokumen, lalu klik tombol "Jalankan AttachUploader".

⚠️ Catatan Keamanan

Kode ini menggunakan konfigurasi default untuk server tes publik (dlptest.com) dan Gmail. Demi keamanan, password pada source code telah disensor (YOUR_PASSWORD_HERE). Silakan isi dengan kredensial Anda sendiri saat menjalankan aplikasi.


Created by: Nanda Septiana Ramadhani (714240033)
