# Dokumentasi Aplikasi Otomatisasi Telegram

## Pendahuluan

Aplikasi ini dirancang untuk mengotomatisasi pengiriman pesan teks ke grup Telegram menggunakan akun pengguna tunggal. Aplikasi ini fokus pada stabilitas, penanganan error, dan kepatuhan terhadap praktik anti-pemblokiran.

## Fitur Utama

- **Autentikasi & Sesi:** Menggunakan API MTProto untuk login via nomor HP + OTP, dengan dukungan 2FA.
- **Pengiriman Pesan Otomatis:** Mengirim pesan teks secara acak dari channel sumber ke grup target.
- **Delay Acak:** Menerapkan delay acak antar pesan (5-10 detik) dan antar siklus (1.1-1.3 jam) untuk mengurangi risiko pemblokiran.
- **Sumber Pesan Dinamis:** Pesan diambil secara acak dari channel Telegram spesifik (`@message_source`).
- **Daftar Grup Target Dinamis:** Daftar grup target diambil dari channel Telegram spesifik (`@group_list`). Aplikasi akan mengirim pesan ke SEMUA grup yang tidak di-blacklist dalam satu siklus.
- **Manajemen Blacklist:**
    - **Blokir Permanen:** Untuk error yang membuat pengiriman tidak mungkin (misal: `ChatForbidden`, `ChatIdInvalid`, `UserBlocked`, `PeerIdInvalid`, `ChatWriteForbiddenError`, `UserBannedInChannelError`).
    - **Blokir Sementara:** Untuk `SlowModeWait` (dilewati) dan `FloodWait` (dengan pembersihan otomatis setelah masa blokir berakhir).
- **File Konfigurasi:** Semua kredensial, channel, dan parameter delay dapat dikonfigurasi melalui `config.json`.
- **Log Aktivitas:** Mencatat aktivitas dengan detail timestamp, grup tujuan, status pesan (sukses/gagal), dan error spesifik ke `activity.log` dalam format teks biasa yang mudah dibaca.

## Persyaratan Sistem

- Python 3.8 atau lebih tinggi.
- Koneksi internet stabil.

## Instalasi & Setup

1.  **Clone atau Unduh Proyek:**
    Unduh semua file proyek ke direktori lokal Anda.

2.  **Instal Dependensi:**
    Buka terminal di direktori proyek dan jalankan perintah berikut:
    ```bash
    pip install telethon
    ```

3.  **Konfigurasi `config.json`:**
    Buka file `config.json` dan isi detail berikut:
    -   `telegram.api_id`: API ID Anda dari [my.telegram.org](https://my.telegram.org/).
    -   `telegram.api_hash`: API Hash Anda dari [my.telegram.org](https://my.telegram.org/).
    -   `telegram.message_source_channel`: ID numerik atau username channel Telegram tempat pesan akan diambil. Contoh: `-1001234567890` atau `@your_message_channel`.
    -   `telegram.group_list_channel`: ID numerik atau username channel Telegram yang berisi daftar grup target. Setiap baris dalam pesan di channel ini akan dianggap sebagai entitas grup. Contoh: `-1001987654321` atau `@your_group_list_channel`.
    -   `delays.min_delay_message`: Delay minimum antar pesan dalam detik (misal: 5).
    -   `delays.max_delay_message`: Delay maksimum antar pesan dalam detik (misal: 10).
    -   `delays.min_delay_cycle`: Delay minimum antar siklus dalam jam (misal: 1.1).
    -   `delays.max_delay_cycle`: Delay maksimum antar siklus dalam jam (misal: 1.3).

    **Contoh `config.json`:**
    ```json
    {
        "telegram": {
            "api_id": 21507942,
            "api_hash": "399fae9734796b25b068050f5f03b698",
            "message_source_channel": -1002779817596,
            "group_list_channel": -1002790437700
        },
        "delays": {
            "min_delay_message": 5,
            "max_delay_message": 10,
            "min_delay_cycle": 1.1,
            "max_delay_cycle": 1.3
        }
    }
    ```

## Cara Menjalankan Aplikasi

1.  Pastikan Anda telah menyelesaikan langkah-langkah instalasi dan setup di atas.
2.  Buka terminal di direktori proyek.
3.  Jalankan aplikasi dengan perintah:
    ```bash
    python3.11 main.py
    ```
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

