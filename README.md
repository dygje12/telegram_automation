# Telegram Automation Bot

## Pendahuluan

Aplikasi ini adalah bot otomatisasi Telegram yang dirancang untuk mengirim pesan teks ke grup menggunakan akun pengguna tunggal (userbot). Fokus utama aplikasi ini adalah stabilitas, penanganan error yang robust, dan kepatuhan terhadap praktik anti-pemblokiran untuk meminimalkan risiko akun.

## Fitur Utama

- **Autentikasi Aman:** Menggunakan API MTProto untuk login via nomor HP + OTP, dengan dukungan Two-Factor Authentication (2FA).
- **Pengiriman Pesan Otomatis:** Mengirim pesan teks secara acak dari channel sumber ke grup target.
- **Delay Adaptif:** Menerapkan delay acak antar pesan (5-10 detik) dan antar siklus (1.1-1.3 jam) untuk mengurangi risiko pemblokiran oleh Telegram.
- **Sumber Pesan Dinamis:** Pesan diambil secara acak dari channel Telegram spesifik (`@message_source`).
- **Daftar Grup Target Dinamis:** Daftar grup target diambil dari channel Telegram spesifik (`@group_list`). Aplikasi akan mengirim pesan ke SEMUA grup yang tidak di-blacklist dalam satu siklus.
- **Manajemen Blacklist Cerdas:**
    - **Blokir Permanen:** Untuk error fatal yang membuat pengiriman tidak mungkin (misal: `ChatForbidden`, `ChatIdInvalid`, `UserBlocked`, `PeerIdInvalid`, `ChatWriteForbiddenError`, `UserBannedInChannelError`). Entitas yang diblokir permanen tidak akan dicoba lagi di siklus berikutnya.
    - **Blokir Sementara:** Untuk `SlowModeWait` (dilewati untuk siklus saat ini) dan `FloodWait` (dengan pembersihan otomatis setelah masa blokir berakhir).
- **Konfigurasi Fleksibel:** Semua kredensial, channel, dan parameter delay dapat dikonfigurasi melalui `config.json`.
- **Log Aktivitas Komprehensif:** Mencatat semua aktivitas dengan detail timestamp, grup tujuan, status pesan (sukses/gagal), dan error spesifik ke `activity.log` dalam format teks biasa yang mudah dibaca.

## Persyaratan Sistem

- Python 3.8 atau lebih tinggi.
- Koneksi internet stabil.

## Instalasi & Setup

1.  **Unduh Proyek:**
    Unduh semua file proyek ke direktori lokal Anda. Anda bisa mendapatkan paket lengkap (termasuk tutorial instalasi VPS) dalam format `.zip`.

2.  **Instal Dependensi:**
    Buka terminal di direktori proyek Anda dan jalankan perintah berikut untuk menginstal semua dependensi Python yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Konfigurasi `config.json`:**
    Buka file `config.json` dan isi detail konfigurasi Anda. Ini adalah langkah **sangat penting**.

    **PENTING: KEAMANAN KREDENSIAL**
    File `config.json` berisi informasi sensitif (API ID dan API Hash). Untuk alasan keamanan, **JANGAN PERNAH MENGUNGGAH `config.json` yang berisi kredensial asli Anda ke repositori publik seperti GitHub.**

    **Rekomendasi:**
    *   Untuk pengembangan lokal, Anda bisa menggunakan `config.json` dengan kredensial Anda.
    *   Untuk deployment di lingkungan produksi (misalnya VPS), sangat disarankan untuk menggunakan **variabel lingkungan (environment variables)** untuk `API_ID` dan `API_HASH`.
    *   Jika Anda tetap ingin menyertakan `config.json` di repositori (misalnya untuk tujuan dokumentasi), buatlah salinan `config.json.example` dengan nilai placeholder dan tambahkan `config.json` ke file `.gitignore` Anda.

    **Detail Konfigurasi:**
    -   `telegram.api_id`: API ID Anda dari [my.telegram.org](https://my.telegram.org/).
    -   `telegram.api_hash`: API Hash Anda dari [my.telegram.org](https://my.telegram.org/).
    -   `telegram.message_source_channel`: ID numerik atau username channel Telegram tempat pesan akan diambil. Contoh: `-1001234567890` atau `@your_message_channel`.
    -   `telegram.group_list_channel`: ID numerik atau username channel Telegram yang berisi daftar grup target. Setiap baris dalam pesan di channel ini akan dianggap sebagai entitas grup. Contoh: `-1001987654321` atau `@your_group_list_channel`.
    -   `delays.min_delay_message`: Delay minimum antar pesan dalam detik (misal: 5).
    -   `delays.max_delay_message`: Delay maksimum antar pesan dalam detik (misal: 10).
    -   `delays.min_delay_cycle`: Delay minimum antar siklus dalam jam (misal: 1.1).
    -   `delays.max_delay_cycle`: Delay maksimum antar siklus dalam jam (misal: 1.3).

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

4.  **File `.gitignore`:**
    Pastikan Anda memiliki file `.gitignore` di root proyek Anda untuk mengecualikan file-file sensitif dan tidak perlu dari kontrol versi. Ini sangat penting untuk mencegah pengunggahan kredensial dan file sesi.

    **Isi `.gitignore` yang Direkomendasikan:**
    ```
    # Python
    __pycache__/
    *.pyc
    *.pyo
    *.pyd
    .Python/

    # Specific to this project
    *.session  # Penting: Mencegah file sesi Telegram terunggah
    activity.log
    *.zip

    # Mypy cache
    .mypy_cache/

    # Ruff cache
    .ruff_cache/
    
    # Configuration file with sensitive data (jika Anda tidak menggunakan variabel lingkungan)
    config.json
    ```

5.  **Catatan tentang `blacklist.json` dan `activity.log`:**
    File `blacklist.json` dan `activity.log` akan dibuat secara otomatis oleh aplikasi jika belum ada. Anda tidak perlu membuatnya secara manual.

## Cara Menjalankan Aplikasi (Lokal)

1.  Pastikan Anda telah menyelesaikan langkah-langkah instalasi dan setup di atas.
2.  Buka terminal di direktori proyek.
3.  Jalankan aplikasi dengan perintah:
    ```bash
    python3 main.py
    ```
    *(Gunakan `python3.11 main.py` jika Anda ingin spesifik ke Python 3.11)*

4.  Pada saat pertama kali dijalankan, aplikasi akan meminta nomor telepon, kode OTP, dan kata sandi 2FA (jika diaktifkan) untuk login ke akun Telegram Anda. Ikuti instruksi di terminal.
5.  Setelah login berhasil, aplikasi akan mulai beroperasi secara otomatis sesuai dengan konfigurasi.

## Log Aktivitas

Semua aktivitas aplikasi akan dicatat dalam file `activity.log` di direktori proyek. Format log adalah teks biasa dengan detail timestamp, status, group ID (jika ada), pesan, dan error (jika ada). Contoh:

```
[2025-07-10 09:52:06] [INFO] Aplikasi dimulai
[2025-07-10 09:52:17] [SUCCESS] [Group ID: 2147469311] Pesan berhasil dikirim
[2025-07-10 09:52:34] [FAILED] [Group ID: 2651902880] Gagal mengirim pesan: You can't write in this chat (Error: You can't write in this chat (caused by SendMessageRequest))
```

## Catatan Penting

-   **Userbot:** Aplikasi ini beroperasi sebagai userbot (menggunakan akun pengguna tunggal), bukan bot API. Penggunaan userbot harus dilakukan dengan hati-hati dan mematuhi Ketentuan Layanan Telegram untuk menghindari pemblokiran akun.
-   **Format Channel Grup:** Pastikan setiap entri grup di `group_list_channel` adalah ID numerik grup (misal: `-1001234567890`), username publik (misal: `@publicgroup`), atau tautan undangan (misal: `https://t.me/joinchat/ABCDEFGH`). Setiap entri harus berada pada baris terpisah dalam pesan di channel ini. Aplikasi akan mencoba mengurai setiap baris secara individual.
-   **Stabilitas & Anti-Ban:** Aplikasi ini dirancang dengan delay acak dan penanganan error untuk meminimalkan risiko pemblokiran. Namun, tidak ada jaminan 100% anti-ban. Penggunaan yang berlebihan atau tidak wajar dapat tetap menyebabkan pemblokiran.

## Pemecahan Masalah (Troubleshooting)

-   **`telethon.errors.rpcerrorlist.AuthKeyUnregisteredError` atau masalah login lainnya:** Pastikan `api_id` dan `api_hash` Anda benar dan Anda memasukkan nomor telepon, OTP, dan 2FA dengan tepat.
-   **`telethon.errors.rpcerrorlist.ChannelInvalidError` atau `telethon.errors.rpcerrorlist.UsernameInvalidError`:** Pastikan ID atau username channel sumber pesan dan channel grup target sudah benar dan akun Anda memiliki akses ke channel tersebut.
-   **`Gagal mendapatkan entitas dari [link/ID]: [error]`:** Ini berarti aplikasi tidak dapat mengidentifikasi entitas grup dari entri yang diberikan. Periksa kembali format entri di `group_list_channel` Anda.
-   **`You can't write in this chat`:** Akun Anda tidak memiliki izin untuk mengirim pesan di grup tersebut. Grup ini akan ditambahkan ke blacklist permanen.
-   **`FloodWaitError`:** Anda mengirim pesan terlalu cepat. Aplikasi akan menambahkan grup ke blacklist sementara dan menunggu sebelum mencoba lagi.
-   **`SlowModeWaitError`:** Grup memiliki mode lambat aktif. Aplikasi akan melewati grup ini untuk siklus saat ini.

Jika Anda mengalami masalah lain, periksa file `activity.log` untuk detail error dan hubungi pengembang (saya) dengan log tersebut.



