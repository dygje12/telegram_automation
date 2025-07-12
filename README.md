# Panduan Penggunaan Telegram Automation

Selamat datang di panduan penggunaan Telegram Automation. Proyek ini dirancang untuk membantu Anda mengotomatisasi interaksi tertentu di Telegram. Panduan ini akan memandu Anda melalui proses instalasi dan konfigurasi di Virtual Private Server (VPS), memastikan aplikasi berjalan secara terus-menerus.

## 1. Persyaratan

Sebelum memulai, pastikan Anda memiliki hal-hal berikut:

*   **Akses ke VPS:** Akses ke Virtual Private Server (VPS) dengan kemampuan untuk menginstal perangkat lunak dan menjalankan perintah terminal.
*   **Sistem Operasi Berbasis Linux:** VPS Anda harus menjalankan sistem operasi berbasis Linux (misalnya, Ubuntu, Debian, CentOS, dll.).
*   **Pengetahuan Dasar Linux:** Pemahaman dasar tentang perintah terminal Linux.
*   **Nomor Telepon Telegram:** Nomor telepon yang belum terdaftar di Telegram atau nomor yang ingin Anda gunakan untuk bot otomatisasi ini.
*   **API ID dan API Hash Telegram:** Anda bisa mendapatkannya dari [my.telegram.org](https://my.telegram.org/). Login dengan nomor telepon Anda, lalu klik 'API development tools'. Catat `App api_id` dan `App api_hash` Anda.

## 2. Persiapan VPS Anda

### 2.1. Koneksi ke VPS Anda

Sambungkan ke VPS Anda menggunakan SSH. Anda akan memerlukan kredensial login (username dan password, atau file kunci SSH) yang disediakan oleh penyedia VPS Anda.

```bash
ssh username@your-vps-public-ip
```

Pastikan untuk mengganti `username` dengan username SSH Anda dan `your-vps-public-ip` dengan alamat IP publik VPS Anda.

### 2.2. Perbarui Sistem

Setelah terhubung, selalu disarankan untuk memperbarui daftar paket dan meng-upgrade paket yang terinstal. Perintah ini mungkin sedikit berbeda tergantung pada distribusi Linux Anda (contoh untuk Debian/Ubuntu):

```bash
sudo apt update
```

```bash
sudo apt upgrade -y
```

Untuk distribusi berbasis Red Hat (misalnya CentOS, Fedora), Anda mungkin menggunakan `yum` atau `dnf`:

```bash
sudo yum update -y
```

```bash
sudo dnf update -y
```

### 2.3. Instal Python dan Pip

Telegram Automation membutuhkan Python 3 dan pip. Pastikan keduanya terinstal di VPS Anda. Perintah instalasi mungkin bervariasi tergantung pada distribusi Linux Anda.

Untuk Debian/Ubuntu:

```bash
sudo apt install python3 python3-pip -y
```

Untuk CentOS/Fedora:

```bash
sudo yum install python3 python3-pip -y
```

```bash
sudo dnf install python3 python3-pip -y
```

## 3. Instalasi Telegram Automation

### 3.1. Kloning Repositori

Navigasi ke direktori home Anda dan kloning repositori Telegram Automation:

```bash
cd ~/
```

```bash
git clone https://github.com/dygje12/telegram_automation.git
```

Ini akan membuat direktori baru bernama `telegram_automation` di direktori home Anda.

### 3.2. Buat dan Aktifkan Virtual Environment (venv)

Sangat disarankan untuk menggunakan virtual environment untuk mengelola dependensi proyek agar tidak bentrok dengan paket sistem. Pertama, instal modul `venv` jika belum ada:

Untuk Debian/Ubuntu:

```bash
sudo apt install python3-venv -y
```

Untuk CentOS/Fedora:

```bash
sudo yum install python3-virtualenv -y
```

```bash
sudo dnf install python3-virtualenv -y
```

Kemudian, buat virtual environment di dalam direktori proyek dan aktifkan:

```bash
cd telegram_automation
```

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

Setelah diaktifkan, Anda akan melihat `(venv)` di awal prompt terminal Anda, menunjukkan bahwa Anda berada di dalam virtual environment.

### 3.3. Instal Dependensi Python

Sekarang, instal semua dependensi Python yang diperlukan menggunakan `pip` di dalam virtual environment yang aktif:

```bash
pip install -r requirements.txt
```

### 3.4. Konfigurasi `config.json`

File `config.json` adalah tempat Anda mengatur parameter penting untuk otomatisasi. Buka file ini menggunakan editor teks seperti `nano`:

```bash
nano config.json
```

Anda perlu mengisi detail berikut:

*   `telegram.api_id`: API ID yang Anda dapatkan dari [my.telegram.org](https://my.telegram.org/).
*   `telegram.api_hash`: API Hash yang Anda dapatkan dari [my.telegram.org](https://my.telegram.org/).
*   `telegram.message_source_channel`: ID numerik atau username channel Telegram tempat pesan akan diambil. Contoh: `-1001234567890` atau `@your_message_channel`.
*   `telegram.group_list_channel`: ID numerik atau username channel Telegram yang berisi daftar grup target. Setiap baris dalam pesan di channel ini akan dianggap sebagai entitas grup. Contoh: `-1001987654321` atau `@your_group_list_channel`.
*   `delays.min_delay_message`: Delay minimum antar pesan dalam detik (misal: 5).
*   `delays.max_delay_message`: Delay maksimum antar pesan dalam detik (misal: 10).
*   `delays.min_delay_cycle`: Delay minimum antar siklus dalam jam (misal: 1.1).
*   `delays.max_delay_cycle`: Delay maksimum antar siklus dalam jam (misal: 1.3).

**Contoh `config.json` (dengan nilai placeholder):**

```json
{
    "telegram": {
        "api_id": 1234567,           // Ganti dengan API ID Anda dari my.telegram.org
        "api_hash": "your_api_hash_here", // Ganti dengan API Hash Anda dari my.telegram.org
        "message_source_channel": "https://t.me/your_source_channel_username_or_id",
        "group_list_channel": "https://t.me/your_group_list_channel_username_or_id"
    },
    "delays": {
        "min_delay_message": 5,
        "max_delay_message": 10,
        "min_delay_cycle": 1.1,
        "max_delay_cycle": 1.3
    }
}
```

Setelah selesai mengedit, simpan file dengan menekan `Ctrl+X`, lalu `Y`, dan `Enter`.

### 3.5. Login Telegram Pertama Kali

Saat pertama kali menjalankan aplikasi, Anda perlu login ke akun Telegram Anda. Ini akan membuat file sesi yang diperlukan. Pastikan Anda masih berada di dalam virtual environment yang aktif, lalu jalankan `main.py` secara manual untuk proses ini:

```bash
python main.py
```

Aplikasi akan meminta nomor telepon Anda, kode OTP yang dikirim ke Telegram Anda, dan kata sandi 2FA (jika diaktifkan). Ikuti instruksi di terminal. Setelah berhasil login, aplikasi akan mulai berjalan. Anda bisa menghentikannya dengan `Ctrl+C` karena kita akan menjalankannya sebagai layanan.

## 4. Menjalankan Otomatisasi Secara Terus-menerus (Systemd Service)

Untuk memastikan Telegram Automation berjalan di latar belakang dan otomatis dimulai ulang jika terjadi masalah atau setelah reboot VPS, kita akan mengaturnya sebagai layanan `systemd`. Ini adalah metode umum untuk sistem berbasis Linux yang menggunakan `systemd` (seperti Ubuntu, Debian, CentOS 7+, dll.).

### 4.1. Salin File Layanan

File `telegram_automation.service` sudah disediakan di repositori dengan konfigurasi yang benar untuk virtual environment. Anda perlu menyalinnya ke direktori `systemd`:

```bash
sudo cp ~/telegram_automation/telegram_automation.service /etc/systemd/system/
```

### 4.2. Muat Ulang Systemd dan Aktifkan Layanan

Setelah menyalin file, muat ulang `systemd` untuk mengenali layanan baru, lalu aktifkan dan mulai layanan:

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl enable telegram_automation.service
```

```bash
sudo systemctl start telegram_automation.service
```

### 4.3. Verifikasi Status Layanan

Anda dapat memeriksa status layanan untuk memastikan bahwa itu berjalan dengan benar:

```bash
sudo systemctl status telegram_automation.service
```

Anda akan melihat output yang menunjukkan status `active (running)` jika semuanya berhasil.

## 5. Memantau Aktivitas

Semua aktivitas aplikasi akan dicatat dalam file `activity.log` di direktori proyek (`~/telegram_automation/activity.log`). Anda dapat memantaunya secara real-time menggunakan perintah `tail`:

```bash
tail -f ~/telegram_automation/activity.log
```

Tekan `Ctrl+C` untuk keluar dari `tail`.

## 6. Pemecahan Masalah Umum

*   **Error Login:** Pastikan `api_id` dan `api_hash` Anda benar. Periksa koneksi internet VPS Anda.
*   **Grup Tidak Ditemukan:** Pastikan format `group_list_channel` dan entitas grup di dalamnya sudah benar (ID numerik atau username).
*   **Batasan Pesan (Flood Wait):** Aplikasi ini dirancang dengan penundaan untuk meminimalkan risiko ini, tetapi jika terjadi, aplikasi akan menunggu dan mencoba lagi. Hindari mengubah nilai `delays` terlalu rendah.

Jika Anda mengalami masalah lain, periksa `activity.log` untuk detail lebih lanjut.

---

