# Tutorial Instalasi dan Otomatisasi Telegram di VPS (Ubuntu/systemd)

Tutorial ini akan memandu Anda langkah demi langkah untuk menginstal dan menjalankan aplikasi otomatisasi Telegram Anda di Virtual Private Server (VPS) berbasis Ubuntu, serta mengkonfigurasinya agar berjalan secara otomatis menggunakan `systemd`.

**Asumsi:**
*   Anda sudah memiliki VPS Ubuntu (atau distribusi Linux lain yang menggunakan `systemd`).
*   Anda sudah login ke VPS Anda melalui SSH sebagai pengguna dengan hak `sudo`.
*   Anda telah mengunduh file `telegram_automation_final.zip` ke komputer lokal Anda.

## Langkah 1: Unggah File Proyek ke VPS

Unggah file `telegram_automation_final.zip` ke direktori home pengguna Anda di VPS (misalnya `/home/ubuntu/`). Anda bisa menggunakan `scp` atau `sftp`.

Contoh menggunakan `scp` dari terminal lokal Anda:
```bash
scp /path/to/your/telegram_automation_final.zip username@your_vps_ip:/home/username/
```
*(Ganti `/path/to/your/` dengan lokasi file di komputer lokal Anda, `username` dengan username VPS Anda, dan `your_vps_ip` dengan alamat IP VPS Anda.)*

## Langkah 2: Persiapan di VPS

Login ke VPS Anda melalui SSH dan ikuti langkah-langkah berikut:

1.  **Buat Direktori Proyek dan Pindah ke Sana:**
    Buat direktori baru untuk proyek Anda (misalnya `/home/ubuntu/telegram_automation/`) dan masuk ke dalamnya. Ini adalah lokasi yang direkomendasikan untuk aplikasi Anda.
    ```bash
    mkdir -p /home/ubuntu/telegram_automation
    cd /home/ubuntu/telegram_automation
    ```

2.  **Ekstrak File Zip:**
    Ekstrak isi file zip yang telah Anda unggah ke direktori ini.
    ```bash
    unzip /home/ubuntu/telegram_automation_final.zip
    ```
    *(Catatan: Sesuaikan path `/home/ubuntu/telegram_automation_final.zip` jika Anda mengunggahnya ke lokasi lain.)*

3.  **Instal Dependensi Python:**
    Pastikan `pip` terinstal, lalu instal pustaka yang diperlukan oleh aplikasi. Perbarui daftar paket dan instal `python3-pip` jika belum ada.
    ```bash
    sudo apt update
    sudo apt install python3-pip -y
    pip install -r requirements.txt
    ```

## Langkah 3: Konfigurasi Aplikasi

1.  **Edit `config.json`:**
    Ini adalah langkah **sangat penting**. Anda harus mengedit file `config.json` di direktori `/home/ubuntu/telegram_automation/` dengan `api_id`, `api_hash`, `message_source_channel`, dan `group_list_channel` Anda. Anda bisa menggunakan editor teks seperti `nano` atau `vim`.
    ```bash
    nano /home/ubuntu/telegram_automation/config.json
    ```
    **PENTING: KEAMANAN KREDENSIAL**
    File `config.json` berisi informasi sensitif (API ID dan API Hash). Untuk alasan keamanan, **JANGAN PERNAH MENGUNGGAH `config.json` yang berisi kredensial asli Anda ke repositori publik seperti GitHub.**

    **Rekomendasi:**
    *   Untuk pengembangan lokal, Anda bisa menggunakan `config.json` dengan kredensial Anda.
    *   Untuk deployment di lingkungan produksi (misalnya VPS), sangat disarankan untuk menggunakan **variabel lingkungan (environment variables)** untuk `API_ID` dan `API_HASH`.
    *   Jika Anda tetap ingin menyertakan `config.json` di repositori (misalnya untuk tujuan dokumentasi), buatlah salinan `config.json.example` dengan nilai placeholder dan tambahkan `config.json` ke file `.gitignore` Anda.

    Isi `config.json` harus terlihat seperti ini (ganti nilai placeholder dengan informasi Anda):
    ```json
    {
        "telegram": {
            "api_id": 1234567,           // Ganti dengan API ID Anda dari my.telegram.org
            "api_hash": "your_api_hash_here", // Ganti dengan API Hash Anda dari my.telegram.org
            "message_source_channel": "https://t.me/your_source_channel_username_or_id", // Ganti dengan username atau ID channel sumber Anda
            "group_list_channel": "https://t.me/your_group_list_channel_username_or_id"   // Ganti dengan username atau ID channel daftar grup Anda
        },
        "delays": {
            "min_delay_message": 5,
            "max_delay_message": 10,
            "min_delay_cycle": 1.1,
            "max_delay_cycle": 1.3
        }
    }
    ```
    Simpan perubahan dan keluar dari editor (`Ctrl+X`, `Y`, `Enter` untuk `nano`).

2.  **Catatan tentang `blacklist.json` dan `activity.log`:**
    File `blacklist.json` dan `activity.log` akan dibuat secara otomatis oleh aplikasi jika belum ada. Anda tidak perlu membuatnya secara manual.

## Langkah 4: Konfigurasi systemd Service

File `telegram_automation.service` sudah disertakan dalam zip. File ini akan mengkonfigurasi aplikasi Anda sebagai layanan `systemd`.

1.  **Pindahkan File Layanan systemd:**
    Salin file `telegram_automation.service` yang sudah diekstrak ke direktori `systemd`.
    ```bash
    sudo cp /home/ubuntu/telegram_automation/telegram_automation.service /etc/systemd/system/
    ```

2.  **Muat Ulang Daemon systemd:**
    Beri tahu `systemd` untuk membaca konfigurasi layanan yang baru.
    ```bash
    sudo systemctl daemon-reload
    ```

3.  **Aktifkan Layanan:**
    Aktifkan layanan agar secara otomatis dimulai setiap kali VPS boot. Ini memastikan aplikasi Anda akan berjalan kembali setelah restart VPS.
    ```bash
    sudo systemctl enable telegram_automation.service
    ```

4.  **Mulai Layanan:**
    Mulai aplikasi Anda sebagai layanan `systemd` sekarang.
    ```bash
    sudo systemctl start telegram_automation.service
    ```

## Langkah 5: Verifikasi (Opsional tapi Direkomendasikan)

1.  **Periksa Status Layanan:**
    Periksa apakah layanan berjalan dengan benar.
    ```bash
    sudo systemctl status telegram_automation.service
    ```
    Anda akan melihat output yang menunjukkan `active (running)` jika semuanya berhasil. Jika ada masalah, lanjutkan ke langkah berikutnya.

2.  **Lihat Log Layanan:**
    Jika layanan tidak berjalan atau Anda ingin melihat output aplikasi secara real-time, gunakan perintah ini:
    ```bash
    sudo journalctl -u telegram_automation.service -f
    ```
    Tekan `Ctrl+C` untuk keluar dari tampilan log.

Setelah semua langkah ini selesai, aplikasi otomatisasi Telegram Anda akan berjalan di latar belakang VPS Anda, dan akan secara otomatis dimulai ulang jika VPS di-restart atau jika aplikasi mengalami crash.

